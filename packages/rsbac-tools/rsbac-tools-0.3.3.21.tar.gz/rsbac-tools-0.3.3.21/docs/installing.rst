.. _`Installation`:

Installation
============

rsbactools works with python version 3.3.

rsbactools works on Linux with RSBAC version 1.4.8

.. note::
  
  - above versions only tested other may work also
  - Python 2 support is droped on v0.3

.. _`get-rsbactools`:

1. `clone repository`_
2. `download archive`_
3. `Package Manager`_

.. _`clone repository`: 

1. clone repository
------------------- 

Install::

  hg clone https://igraltist@bitbucket.org/igraltist/rsbac-tools
  cd rsbac-tools 
  python setup.py install or pip install .

Upgrade::

  pip install --upgrade .

.. _`download archive`:

2. download archive
-------------------

Install::

  wget https://bitbucket.org/igraltist/rsbac-tools/get/tip.tar.bz2 
  # for alternative archive use zip or gz as suffix
  tar xvjf tip.tar.bz2
  cd rsbac-tools
  pip install .

  

.. _pip:

3. pip
------

Install:: 

  pip install rsbac-tools

Upgrade::
        
  pip install --upgrade rsbac-tools

.. _`Package Manager`:

4. Package Manager
------------------

At moment only an ebuild for the Gentoo is available.
        
Add keyword in /etc/portage/package.keywords::

  app-admin/rsbac-tools ~amd64

On Gentoo::

  emerge -av rsbac-tools
