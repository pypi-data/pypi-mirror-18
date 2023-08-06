=========================================
Consistent versioning for NatCap Projects
=========================================

This package provides a consistent versioning scheme for projects of the
Natural Capital Project (http://naturalcapitalproject.org).  The versioning
string currently provided is PEP440-compliant, and is supported for both git
and mercurial repositories.  Mercurial source archives (created by the
``hg archive`` command) are also supported.

.. contents::
    :local:

Versioning Scheme
=================

How a version string is formatted: ::

    If we are at a tag:
        version = {tag}
    else:
        version = {tag}.post{N}+r{nodeid|short}

    If there are no tags:
        {tag} = 'null'


Examples:

 * **Version string** = ``3.4.5``

   * Meaning: This version of this tool was built from the tag ``3.4.5``.

   * You can update to this revision by calling ``hg update -r 3.4.5``

 * **Version string =** ``3.4.5.post35+r788a29c99234``

   * Meaning: This version of this tool was built from a revision where:

     * The latest tag was ``3.4.5``

     * The latest commit on this branch is ``35`` commits beyond the latest tag.

     * The latest commit has a shortened node ID of ``788a29c99234``

   * You can update to this revision by calling ``hg update -r 788a29c99234``



Installation
============

**Via pip:** ``pip install natcap.versioner``

**Via setup.py:** ``python setup.py install``

.. note ::
    If you install ``natcap.versioner`` via pip or via setup.py, dependencies
    should install automatically.


Dependencies
============

Note that ``natcap.versioner`` requires setuptools and ``six``.


Usage In Your Project
=====================

To use this project, you'll need to edit two files within your own project:
``setup.py`` and ``__init__.py``.


Usage in setup.py
-----------------

Adding these lines to your ``setup.py`` allows the DVCS information to be
fetched from ``git`` or ``hg`` and recorded in the package metadata.
Additionally, the version will be recorded to the file you indicate with
the ``natcap_version`` keyword.

::

    from setuptools import setup

    setup(
        name='example_project',
        ...
        natcap_version='example_project/version.py',
        setup_requires=['natcap.versioner>=0.4.2']
    )


Usage in __init__.py
--------------------

Adding these lines to your package's ``__init__.py`` file will allow the package
version to be fetched from the package metadata.

::

    # Let's assume your package name is still 'example_project'
    import natcap.versioner
    __version__ = natcap.versioner.get_version('example_project')

Support
=======

If something doesn't work, it's probably broken!
Please submit an issue via the issue tracker, send James an email
or stop by if you're in the office and I'll try to fix it!

You can also file an issue in our `issue tracker <https://bitbucket.org/jdouglass/versioner/issues>`_.

Tests
=====

To run the suite of tests: ::

    $ nosetests test/*.py

Note that ``hg`` and ``git`` must be available as executables on the command-line.

Development
===========

The ``natcap.versioner`` source tree is located at https://bitbucket.org/jdouglass/versioner




0.5.0
=====
* Added python 3.x support.  Installation now requires ``six``.
* Added testing via bitbucket pipelines.

0.4.2
=====
* Correcting an issue when using the ``natcap_version`` distutils keyword where
  the distutils version attribute was being improperly set.

0.4.1
=====
* Removing the need to import natcap.versioner within ``setup.py``.
* ``natcap.versioner`` now uses its own functionality to generate its version
  string.
* Removing ``pyyaml`` from setup.py's ``install_requires``.  This will prevent
  pyyaml from being installed, despite the fact that ``pyyaml`` is no longer
  used by ``natcap.versioner``.
* Git, Hg, and Hg archive repositories can now be referred to by a subdirectory
  within the repo itself.

0.4.0
=====
* Removing dependency on ``pyyaml``.
* Adding ``__version__`` attribute to ``natcap.versioner``.

0.3.3
=====
* Tests now have full coverage of the package.
* Git repositories without branches are now correctly handled.
* Errors encountered in calls to ``hg`` and ``git`` command-line applications
  will cause ``subprocess.CalledProcessError`` to be raised.

0.3.2
=====
* Setting setuptools ``zip_safe=True``.  After a review of the module, it
  appears that no functionality within ``natcap.versioner`` requires access to
  resources within the package via the filesystem.

0.3.1
=====
* Restoring support for installation as egg (0.3.0 lacked this).
* Minor stylistic changes for PEP8 and PEP257

0.3.0
=====
* Adding support for git.
* Added tests for core versioning functionality.

0.2.4
=====
* Allowing get_version() to allow fallback to SCM only when allowed by user
  input.  Defaults to only allowing fallback in non-frozen environments (e.g. a
  source tree).  ``natcap.versioner.VersionNotFound`` will be raised if the version
  string cannot be loaded normally or SCM is disallowed.
* If a version string cannot be parsed by vcs_version(),
  ``natcap.versioner.VersionNotFound`` will optionally be raised.

0.2.3
=====
* Turning setuptools zip_safe flag to False.  When this and natcap.invest have their zip_safe
  flags all as False, the packages happily install side-by-side as individual eggs.

0.2.2
=====
* Fixes an issue where a development version is returned when the user is at a tag.  The 
  version is now correctly reported as just the tag.

0.2.1
=====
* Version files are now properly imported.  This fixes an issue with users unable to fetch
  version strings from within frozen environments that are outside of a source tree.

0.2.0
=====
* API Change: version is now parsed from setup.py using ``natcap.versioner.parse_version()``.
* Allowing the version to be correctly fetched from PKG-INFO from egg/distribution metadata even when the package has not already been built.

0.1.4
=====
* Attempting to get the utils module to import correctly.

0.1.3
=====
* Allowing version string to be written to a package file.

0.1.2
=====
* Default version scheme is dvcs-based post-release now. but can also do a pre-release.

0.1.1
=====
* Fixes installation issues where certain files needed for setup.py were missing from the source distribution.

0.1.0
=====
* Initial public release.


