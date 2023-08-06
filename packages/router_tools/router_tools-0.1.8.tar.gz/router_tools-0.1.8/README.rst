router\_tools
=============

|Latest PyPI version| |Latest Travis CI build status| |Documentation
Status|

Simple tools for router maintain.

Usage
=====

Installation
============

Requirements
------------

Development Guide
=================

Development env setup - bootstrap
---------------------------------

::

    virtualenv .env
    . .env/bin/activate
    pip install -U pip
    cat <<EOF > .env/pip.conf
    [list]
    format=columns
    EOF
    pip install -U virtualenvwrapper
    pip install -U pytest-cov
    pip install -U tox
    pip install -U Sphinx
    pip install -U recommonmark
    pip freeze > requirements.txt
    sphinx-quickstart

    git flow init
    git push -u origin develop

Development env setup - new machine
-----------------------------------

::

    . .env/bin/activate
    pip install -r requirements.txt --use-mirrors

Relase
------

::

    make all
    make release

Licence
=======

.. |Latest PyPI version| image:: https://img.shields.io/pypi/v/router_tools.svg
   :target: https://pypi.python.org/pypi/router_tools
.. |Latest Travis CI build status| image:: https://travis-ci.org/renweibo/router_tools.png
   :target: https://travis-ci.org/renweibo/router_tools
.. |Documentation Status| image:: https://readthedocs.org/projects/router-tools/badge/?version=latest
   :target: http://router-tools.readthedocs.io/en/latest/?badge=latest
