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

Simple example which displays Ejabberd status
(assuming that XML-RPC runs on `127.0.0.1` and port `4560`)::

    from ejabberdctl import ejabberdctl

    host = 'example.com'
    username = 'admin'
    password = 'admin'

    ejabberdctl = ejabberdctl(host, username, password)
    print ejabberdctl.status()


The same example with custom setting of XML-RPC host::

    from ejabberdctl import ejabberdctl

    host = 'example.com'
    username = 'admin'
    password = 'admin'

    ejabberdctl = ejabberdctl(host, username, password,
                              protocol='https', server='example.com', port=4560,
                              admin=True, verbose=True)
    print ejabberdctl.status()


Host vs Server
^^^^^^^^^^^^^^

`host` is the domain served by Ejabberd
(ie. one of your `hosts` defined in `ejabberd.yml`).

`server` is the server IP where Ejabberd runs the XML-RPC module.
Typically it is configured to run on `127.0.0.1` (`localhost`) on port `4560`.


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
