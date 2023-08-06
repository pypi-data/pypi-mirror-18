``libvcs`` - abstraction layer for vcs, powers `vcspull`_.

|pypi| |docs| |build-status| |coverage| |license|

Install::

   $ pip install libvcs

Open up python::

   $ python

.. code-block:: python

   >>> from libvcs.shortcuts import create_repo_from_pip_url, create_repo

   # repo is an object representation of a vcs repository.
   >>> r = create_repo(url='https://www.github.com/tony/myrepo',
   ...                 vcs='git',
   ...                 repo_dir='/tmp/repo')

   # or via pip-style URL
   >>> r = create_repo_from_pip_url(
   ...         pip_url='git+https://www.github.com/tony/myrepo',
   ...         repo_dir='/tmp/repo')

   # it may or may not be checked out/cloned on the system yet
   >>> r.update_repo()
   |myrepo| (git)  Repo directory for myrepo (git) does not exist @ /tmp/myrepo
   |myrepo| (git)  Cloning.
   |myrepo| (git)  git clone https://www.github.com/tony/myrepo /tmp/myrepo
   Cloning into '/tmp/myrepo'...
   Checking connectivity... done.
   |myrepo| (git)  git fetch
   |myrepo| (git)  git pull
   Already up-to-date.

Donations
---------

Your donations fund development of new features, testing and support.
Your money will go directly to maintenance and development of the project.
If you are an individual, feel free to give whatever feels right for the
value you get out of the project.

See donation options at https://git-pull.com/support.html.

More information 
----------------

==============  ==========================================================
Python support  Python 2.7, >= 3.3, pypy
VCS supported   git(1), svn(1), hg(1)
Source          https://github.com/tony/libvcs
Docs            http://libvcs.rtfd.org
Changelog       http://libvcs.readthedocs.io/en/latest/history.html
API             http://libvcs.readthedocs.io/en/latest/api.html
Issues          https://github.com/tony/libvcs/issues
Travis          http://travis-ci.org/tony/libvcs
Test Coverage   https://codecov.io/gh/tony/libvcs
pypi            https://pypi.python.org/pypi/libvcs
Open Hub        https://www.openhub.net/p/libvcs
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/tony/libvcs.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/tony/libvcs.git libvcs
                    $ cd ./libvcs
                    $ virtualenv .venv
                    $ source .venv/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ py.test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: http://libvcs.readthedocs.io/en/latest/
.. _API: http://libvcs.readthedocs.io/en/latest/api.html
.. _pip: http://www.pip-installer.org/en/latest/
.. _vcspull: http://www.github.com/tony/vcspull/

.. |pypi| image:: https://img.shields.io/pypi/v/libvcs.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/libvcs

.. |build-status| image:: https://img.shields.io/travis/tony/libvcs.svg
   :alt: Build Status
   :target: https://travis-ci.org/tony/libvcs

.. |coverage| image:: https://codecov.io/gh/tony/libvcs/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/tony/libvcs
    
.. |license| image:: https://img.shields.io/github/license/tony/libvcs.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/libvcs/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/libvcs/
