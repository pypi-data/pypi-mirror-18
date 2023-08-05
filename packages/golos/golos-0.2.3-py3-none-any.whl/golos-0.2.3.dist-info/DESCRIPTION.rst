Python Library for Golos
========================

Python 3 library for Golos!

Installation
------------

Install with `pip`:

    $ sudo apt-get install libffi-dev libssl-dev python-dev
    $ pip3 install golos

Manual installation:

    $ git clone https://github.com/GolosChain/python-goloslib
    $ cd python-goloslib
    $ python3 setup.py install --user

Upgrade
-------

    $ pip install --user --upgrade

Additional dependencies
-----------------------

`golosapi.golosasyncclient`:
 * `asyncio==3.4.3`
 * `pyyaml==3.11`

Documentation
-------------

Thanks to readthedocs.io, the documentation can be viewed
[online](http://python-goloslib.readthedocs.io/en/latest/)

Documentation is written with the help of sphinx and can be compile to
html with:

    cd docs
    make html


