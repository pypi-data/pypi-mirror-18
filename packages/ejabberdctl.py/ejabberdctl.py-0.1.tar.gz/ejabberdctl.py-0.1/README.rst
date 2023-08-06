README
======

`ejabberdctl.py` provides Python client for Ejabberd XML-RPC Administration API.


Installation
------------

::

    pip install ejabberdctl.py

::

    git clone https://gitlab.com/markuz/ejabberdctl.py.git ejabberdctlpy
    cd ejabberdctlpy
    python setup.py install


Usage
-----

::

    from ejabberdctl import ejabberdctl

    server = 'example.com'
    username = 'admin'
    password = 'admin'

    ejabberdctl = ejabberdctl(server, username, password)
    print ejabberdctl.status()


Tests
-----

::

    from ejabberdctl.tests import ejabberdctl_tests

    SERVER = 'example.com'
    USERNAME = 'admin'
    PASSWORD = 'admin'
    tests = ejabberdctl_tests(SERVER, USERNAME, PASSWORD)
    tests.run_all()


Coverage
--------

Number of Ejabberd XML-RPC Administration API commands in ``ejabberdctl.py``::

    egrep "def " ejabberdctl.py|grep -v "def __init__\|def ctl"|wc -l
    126


Implementation
^^^^^^^^^^^^^^

Number of implemented commands::

    egrep "def " ejabberdctl.py|grep -v "def __init__\|def ctl\|TODO"|wc -l
    72

Number of commands to implement::

    egrep "def " ejabberdctl.py|grep -v "def __init__\|def ctl"|grep TODO|wc -l
    54


Tests
^^^^^

Number of tests in the testing suite::

    egrep "def " tests.py|grep -v "def __init__\|def run_all\|TODO"|wc -l
    31

Number of tests to implement::

    egrep "def " tests.py|grep -v "def __init__\|def run_all"|grep TODO|wc -l
    95


Contributing
------------

If you wish to help out with the project, please see `todo.txt` for a list of tasks that need doing.
