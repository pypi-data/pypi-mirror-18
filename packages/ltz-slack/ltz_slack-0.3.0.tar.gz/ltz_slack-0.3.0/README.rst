lt-slack
===================

lt-slack is a python package that provieds an interface to slack listed offically on `api.slack.com`_.

built on `lt-slack`_.

|pypi| |build-status| |coverage| |docs| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/lt-slack.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/lt-slack
.. |build-status| image:: https://img.shields.io/travis/jongoks/lt-slack.svg
   :alt: Build Status
   :target: https://travis-ci.org/jongoks/lt-slack
.. |coverage| image:: https://codecov.io/gh/jongoks/lt-slack/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/jongoks/lt-slack
.. |docs| image:: https://readthedocs.org/projects/lt-slack/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/lt-slack/
.. |license| image:: https://img.shields.io/github/license/tony/lt-slack.svg
    :alt: License 
.. _api.slack.com: https://api.slack.com
.. _lt-slack: https://github.com/jongoks/lt-slack


Installation
-------------------
Install via `pip`_

.. code-block:: sh

    $ pip install lt-slack


Install from source:

.. code-block:: sh

    $ git clone git://github.com/jongoks/lt-slack.git
    $ cd lt-slack
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
