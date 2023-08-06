#!/usr/bin/env python2.7

from nagios import BaseCheckCommand

try:
    from requests import HTTPError
    import requests
    requests_installed = True
except ImportError:
    requests_installed = False

try:
    from sumologic import SumoLogic
    sumo_installed = True
except ImportError:
    sumo_installed = False

from optparse import OptionParser
import time
import datetime
import cookielib
import fcntl
import signal
import errno
import json
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        pass

    original_handler = signal.signal(signal.SIGALRM, timeout_handler)

    try:
        signal.alarm(seconds)
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)

class retry(object):

    def __init__(self, retries=3):
        self.retries = retries

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def execute(self, f, *f_args):
        err = None
        while(self.retries > 0):
            try:
                return f(*f_args)
            except requests.exceptions.HTTPError as e:
                if e.errno == 429:
                    err = e
                    self.retries -= 1
                    back_off = 10/self.retries if self.retries != 0 else 10
                    time.sleep(back_off)
                else:
                    raise e
        raise err

class JsonParsingError(ValueError):
    def __init__(self, msg, body):
        super(JsonParsingError, self).__init__("Message: %s, body: %s" %(msg, body))

class CustomSumoLogic(SumoLogic):
    def __init__(self, accessId, accessKey, endpoint=None, cookieFile='cookies.txt', flockFile='sumologic_api.lock'):
        self.session = requests.Session()
        self.session.auth = (accessId, accessKey)
        self.session.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        cj = cookielib.FileCookieJar(cookieFile)
        self.session.cookies = cj
        self.flockFile = file(flockFile, 'w')
        if endpoint is None:
            self.endpoint = self._get_endpoint()
        else:
            self.endpoint = endpoint

    def _flock_acquire(self):
        with timeout(5):
            try:
                fcntl.flock(self.flockFile.fileno(), fcntl.LOCK_EX)
            except IOError as e:
                if e.errno != errno.EINTR:
                    raise e

    def _flock_release(self):
        with timeout(5):
            try:
                fcntl.flock(self.flockFile.fileno(), fcntl.LOCK_UN)
            except IOError as e:
                if e.errno != errno.EINTR:
                    raise e

    def get(self, method, params=None, retries=10):
        self._flock_acquire()
        with retry(retries) as retry_if_rate_limit:
            r = retry_if_rate_limit.execute(super(self.__class__, self).get, method, params)
        self._flock_release()
        return r

    def put(self, method, params, headers=None, retries=10):
        with retry(tries) as retry_if_rate_limit:
            r = retry_if_rate_limit.execute(super(self.__class__, self).put, method, params, headers)
        return r

    def post(self, method, params, headers=None, retries=10):
        with retry(retries) as retry_if_rate_limit:
            r = retry_if_rate_limit.execute(super(self.__class__, self).post, method, params, headers)
        return r

    def collectors(self, limit=None, offset=None):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/collectors', params)
        try:
            return json.loads(r.text)['collectors']
        except ValueError as value_error:
            raise JsonParsingError(value_error.message, r.text)

    def create_source(self, collector_id, source):
        r = self.post('/collectors/' + str(collector_id) + '/sources', source)
        return r.text

    def sources(self, collector_id, limit=None, offset=None):
        params = {'limit': limit, 'offset': offset}
        r = self.get('/collectors/' + str(collector_id) + '/sources', params)
        try:
            return json.loads(r.text)['sources']
        except ValueError as value_error:
            raise JsonParsingError(value_error.message, r.text)

    def _get_endpoint(self):
        self._flock_acquire()
        with retry(10) as retry_if_rate_limit:
            r = retry_if_rate_limit.execute(super(self.__class__, self)._get_endpoint)
        self._flock_release()
        return r

class CollectorLastMessageCheckCommand(BaseCheckCommand):
    def __init__(self, **kwargs):
        # Exit early if prereqs are not installed
        self.prerequites_test()

        # Invoke parent class's constructor
        self.__class__.__bases__[0].__init__(self,\
                parser=OptionParser(usage='%prog [options] COLLECTOR_NAME', version="%prog 1.0"))

        # Constructor for CollectorLastMessage
        self.add_options()
        params      = kwargs
        opts, args  = self.parse_args()

        self.access_id      = params.get('access_id') or opts.access_id
        self.secret_key     = params.get('secret_key') or opts.secret_key
        self.collector_name = params.get('collector_name') or args[0]

        self.warning        = int(opts.warning)
        self.critical       = int(opts.critical)

        # Instantiating the session will not raise if there are invalid credentials
        self.session        = CustomSumoLogic(self.access_id, self.secret_key, cookieFile='/tmp/cookie_jar.txt')

    def add_options(self):
        self.parser.add_option('-a', '--access-id',
                                dest='access_id',
                                action='store',
                                help='Sets the SumoLogic API access ID to use for queries.',
                                metavar='ACCESS_ID')
        self.parser.add_option('-s', '--secret-key',
                                dest='secret_key',
                                action='store',
                                help='sets the SumoLogic API secret key to use for queries.',
                                metavar='SECRET_KEY')

    def prerequites_test(self):
        if not requests_installed:
            self.usage(3,
                        msg='Unable to import requests. Ensure the "requests" package is installed. To install: `pip install requests`')

        if not sumo_installed:
            self.usage(3, 
                        msg='Unable to import sumologic-sdk. Ensure the "sumologic-sdk" package is installed. To install: `pip install sumologic-sdk`')

    def check(self):
        try:
            if not self.collector_alive():
                self.status = "CRITICAL: %s is not alive" % self.collector_name
                self.perf_data = "alive=0;1;1;;"
                self.exit(exit_code=2)
                return None

            time_now = int(time.time())
            time_diff = time_now - self.last_message_time()
        except HTTPError as e:
            self.status = "API Error: %s" % e.message
            self.exit(exit_code=3)
        except AssertionError as e:
            self.status = "Check Error: %s" % e.message
            self.exit(exit_code=3)
        except ValueError as e:
            self.status = "API Error: Hit rate-limit maximum"
            self.exit(exit_code=3)
        except IOError as e:
            self.status = "Exception: %s" % e.message
            self.exit(exit_code=3)

        if time_diff >= self.critical:
            self.status = "CRITICAL: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=2)
        elif time_diff >= self.warning:
            self.status = "WARNING: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=1)
        else:
            self.status = "OK: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=0)

        return None

    def collector_alive(self):
        collectors = self.session.collectors()
        assert len(collectors) > 0, "No collectors"
        for collector in collectors:
            if 'name' in collector and collector['name'] == self.collector_name:
                return collector.get('alive')
        return False

    def last_message_time(self):
        time_now = datetime.datetime.now()
        time_now_iso = time_now.isoformat().split('.')[0]
        time_twelve_hours_ago = (time_now - datetime.timedelta(hours=12)).isoformat().split('.')[0]

        search_res = self.session.search('_collector=%s | limit 1' % self.collector_name, fromTime=time_twelve_hours_ago, toTime=time_now_iso, timeZone='PST')

        assert len(search_res) > 0, "No messages"
        last_message = search_res[0]
        assert type(last_message) == dict, "Unreadable search result"
        return int(last_message.get('_messagetime')) / 1000
