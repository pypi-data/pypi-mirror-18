cloudpassage-halo-python-sdk
============================

Python SDK for CloudPassage Halo API
------------------------------------

.. image:: https://readthedocs.org/projects/cloudpassage-halo-python-sdk/badge/?version=latest

Branch: master

.. image:: https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/badges/gpa.svg
   :target: https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk
   :alt: Code Climate

.. image:: https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/badges/coverage.svg
   :target: https://codeclimate.com/github/cloudpassage/cloudpassage-halo-python-sdk/coverage
   :alt: Test Coverage

.. image:: https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk.svg?branch=master
   :target: https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk

Branch: develop

.. image:: https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk.svg?branch=develop
   :target: https://travis-ci.org/cloudpassage/cloudpassage-halo-python-sdk


Installation
------------

Requirements:

* requests
* pyaml


Install from pip with ``pip install cloudpassage``.  If you want to make
modifications to the SDK you can install it in editable mode by downloading
the source from this github repo, navigating to the top directory within the
archive and running ``pip install -e .`` (note the . at the end).

Quick Start
-----------

Here's the premise: you store your session configuration information (API
credentials, proxy settings, etc) in the cloudpassage.HaloSession object.
This object gets passed into the various class methods which allow you
to interact with the CloudPassage Halo API.

Practical example:
We'll print a list of all servers in our account:

::

    import cloudpassage

    api_key = MY_HALO_API_KEY
    api_secret = MY_API_SECRET
    session = cloudpassage.HaloSession(api_key, api_secret)
    server = cloudpassage.Server(session)

    list_of_servers = server.list_all()
    for s in list_of_servers:
        print "ID: %s   Name: %s" % (s["id"], s["hostname"])



Docs
====

Where to download
-----------------
Documentation can be found at
http://cloudpassage-halo-python-sdk.readthedocs.io/en/latest/?badge=latest

Building documentation
----------------------

1. Clone the repository locally
1. Navigate to ``cloudpassage-halo-python-sdk/docs``
1. run ``sphinx-build -b pdf source build/pdf``
1. Docs will be located at ``cloudpassage-halo-python-sdk/docs/build/pdf/CloudPassage_Python_SDK_$VERSION.pdf``


Testing
=======
Important locations for testing
-------------------------------

  tests/configs: You'll find a file here called portal.yaml.  Copy it to
  portal.yaml.local and complete the information inside with your API key and
  secret.  the .gitignore settings will keep you from checking in your creds
  if you put them in the .local file.  This file (portal.yaml.local) is
  referenced directly by all tests requiring interaction with the API.

  tests/policies: These are Halo policies, used primarily for integration
  tests.

  tests/tests: This is where you'll find the actual tests.


Environmental Requirements
--------------------------

  You'll need to have a CloudPassage Halo account available for running the
  tests, as many are integration-focused.  These are the things you need to have
  (at the very least) to get a clean testing run:

  * Servers:
      * Have at least one active Linux and active Windows server.
      * One deactivated server of any type.
  * Policies:
      * One firewall policy
      * One alert profile
      * One Linux CSM policy
      * One Linux FIM policy
      * One Windows FIM policy
      * One LIDS policy
  * Scans:
      * CSM (Failed scan)
      * FIM (active baseline and successful scan)
      * One CVE exception
  * Events:
      * One event produced by a Windows server.
  * Server Group:
      * Using the default group is fine.
      * Assign the policies mentioned above to the group.
      * Run FIM baselines against the Linux and Windows servers.
      * Kick off a CSM scan if it doesn't happen automatically


Running tests
--------------

 Navigate to tests/ and run ``py.test ./integration ./unit ./style``
 to run the entire test suite.  You can remove any of these if you
 want to focus on a particular section.  For instance, to run only
 the unit and style tests, you would use ``py.test ./unit ./style``.

 If you've got the coverage module installed,
 ``py.test --cov=cloudpassage ./integration ./unit ./style``
 will show statement test coverage.
