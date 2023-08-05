ltz_slack
===================

ltz_slack is a python package that provieds an interface to slack listed offically on `api.slack.com`_.

built on `ltz_slack`_.

|pypi| |build-status| |coverage| |docs| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/ltz_slack.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/ltz_slack
.. |build-status| image:: https://img.shields.io/travis/jongoks/ltz_slack.svg
   :alt: Build Status
   :target: https://travis-ci.org/jongoks/ltz_slack
.. |coverage| image:: https://codecov.io/gh/jongoks/ltz_slack/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/jongoks/ltz_slack
.. |docs| image:: https://readthedocs.org/projects/ltz_slack/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/ltz_slack/
.. |license| image:: https://img.shields.io/github/license/tony/ltz_slack.svg
    :alt: License 
.. _api.slack.com: https://api.slack.com
.. _ltz_slack: https://github.com/jongoks/ltz_slack


Installation
-------------------
Install via `pip`_

.. code-block:: sh

    $ pip install ltz_slack


Install from source:

.. code-block:: sh

    $ git clone git://github.com/jongoks/ltz_slack.git
    $ cd ltz_slack
    $ python setup.py install

.. _pip: https://pip.pypa.io/en/latest/)


Getting Started
-------------------
You need to get your Slack token from `api.slack.com`_.

.. code-block:: python

    import slack
    import slack.chat
    slack.api_token = 'your_token'
    slack.chat.post_message('#eng', 'Hello slackers!', username='mybot')

    import slack.users
    slack.users.list()


Available Methods
-------------------
All methods in `a preview release of Slack API`_ are available.

.. _a preview release of Slack API: https://api.slack.com
