Omada Nagios Python Framework
==============================

This project aims to make managing large-scale Nagios installation(s) simplier.

See `the wiki page <https://wiki.omadahealth.net>`_ for more information.

Features
---------

Implemented
^^^^^^^^^^^^

* Nagios Primatives

    * `BaseCheckCommand` - check command primative

* SumoLogic Check Commands

    * `CollectorLastMessageCheckCommand` - check command which reports last message time for a SumoLogic collector

Tentative
^^^^^^^^^^

Contributing
-------------

Please read the below before getting started. It is preferrable to fork this repository and make pull requests in order to merge new features or bug fixes.

Set Up Workspace
^^^^^^^^^^^^^^^^^

Setup a `virtualenv` within the repository::

    virtualenv .

Install the package::

    pip install -e .[dev,test]

Run the test suite to verify the workspace setup::

    python -m pytest -v test/


Issue Tracker
^^^^^^^^^^^^^^^

All issues for this project (feature request, bug report, etc.) should be made in the Github issues tracker.

Package mantainers will create stories in `PivotalTracker <https://www.pivotaltracker.com/n/projects/940348>`_ to address these issues and track progress. There is no public access to this tracker project. To get read access, send an email to `platform@omadahealth.com <mailto:platform+nagios@omadahealth.com>`_.

Get Help
^^^^^^^^^

Slack: https://omada.slack.com/messages/platform/
Google Group: https://groups.google.com/a/omadahealth.com/forum/#!forum/platform
Email: platform+nagios@omadahealth.com


