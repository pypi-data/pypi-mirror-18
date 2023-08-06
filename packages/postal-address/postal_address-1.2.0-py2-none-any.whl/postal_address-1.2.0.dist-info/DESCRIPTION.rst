Postal Address
==============

Python module to parse, normalize and render postal addresses.

Stable release: |release| |license| |dependencies| |popularity|

Development: |build| |quality| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/postal-address.svg?style=flat
    :target: https://pypi.python.org/pypi/postal-address
    :alt: Last release
.. |license| image:: https://img.shields.io/pypi/l/postal-address.svg?style=flat
    :target: http://opensource.org/licenses/BSD-2-Clause
    :alt: Software license
.. |popularity| image:: https://img.shields.io/pypi/dm/postal-address.svg?style=flat
    :target: https://pypi.python.org/pypi/postal-address#downloads
    :alt: Popularity
.. |dependencies| image:: https://img.shields.io/requires/github/scaleway/postal-address/master.svg?style=flat
    :target: https://requires.io/github/scaleway/postal-address/requirements/?branch=master
    :alt: Requirements freshness
.. |build| image:: https://img.shields.io/travis/scaleway/postal-address/develop.svg?style=flat
    :target: https://travis-ci.org/scaleway/postal-address
    :alt: Unit-tests status
.. |coverage| image:: https://codecov.io/github/scaleway/postal-address/coverage.svg?branch=develop
    :target: https://codecov.io/github/scaleway/postal-address?branch=develop
    :alt: Coverage Status
.. |quality| image:: https://img.shields.io/scrutinizer/g/scaleway/postal-address.svg?style=flat
    :target: https://scrutinizer-ci.com/g/scaleway/postal-address/?branch=develop
    :alt: Code Quality


Motivation
----------

    « What ties us to territory is tax. »
    -- Kevin Deldycke, 2014-11-07

The reason above is why we need fine-grained and meticulous territory
management and normalization. This project aims to solve this problem once for
all.

Don't get me wrong, this work is a huge undertaking. Postal address parsing,
normalization and rendering is hard. See the collection of `falsehoods
programmers believe about postal addresses
<https://github.com/kdeldycke/awesome-falsehood#postal-addresses>`_.

This library is still in its early stages, but is good enough to implement
the new European Directives on VAT, which requires all e-commerce shops to
guess the locality of their EU customers depending on their billing address.


Install
-------

This package is `available on PyPi
<https://pypi.python.org/pypi/postal-address>`_, so you can install the latest
stable release and its dependencies with a simple `pip` call:

.. code-block:: bash

    $ pip install postal-address


Development
-----------

Check out latest development branch:

.. code-block:: bash

    $ git clone git@github.com:scaleway/postal-address.git
    $ cd ./postal-address
    $ python ./setup.py develop

Run unit-tests:

.. code-block:: bash

    $ python ./setup.py nosetests

Run `PEP8 <https://pep8.readthedocs.org>`_ and `Pylint
<http://docs.pylint.org>`_ code style checks:

.. code-block:: bash

    $ pip install pep8 pylint
    $ pep8 postal-address
    $ pylint --rcfile=setup.cfg postal-address


Stability policy
----------------

Here is a bunch of rules we're trying to follow regarding stability:

* Patch releases (``0.x.n`` → ``0.x.(n+1)`` upgrades) are bug-fix only. These
  releases must not break anything and keeps backward-compatibility with
  ``0.x.*`` and ``0.(x-1).*`` series.

* Minor releases (``0.n.*`` → ``0.(n+1).0`` upgrades) includes any non-bugfix
  changes. These releases must be backward-compatible with any ``0.n.*``
  version but are allowed to drop compatibility with the ``0.(n-1).*`` series
  and below.

* Major releases (``n.*.*`` → ``(n+1).0.0`` upgrades) are not planned yet:
  we're still in beta and the final feature set of the ``1.0.0`` release is not
  decided yet.


Release process
---------------

Start from the ``develop`` branch:

.. code-block:: bash

    $ git clone git@github.com:scaleway/postal-address.git
    $ git checkout develop

Revision should already be set to the next version, so we just need to set the
released date in the changelog:

.. code-block:: bash

    $ vi ./CHANGES.rst

Create a release commit, tag it and merge it back to ``master`` branch:

.. code-block:: bash

    $ git add ./postal_address/__init__.py ./CHANGES.rst
    $ git commit -m "Release vX.Y.Z"
    $ git tag "vX.Y.Z"
    $ git push
    $ git push --tags
    $ git checkout master
    $ git pull
    $ git merge "vX.Y.Z"
    $ git push

Push packaging to the `test cheeseshop
<https://wiki.python.org/moin/TestPyPI>`_:

.. code-block:: bash

    $ pip install wheel
    $ python ./setup.py register -r testpypi
    $ python ./setup.py clean
    $ rm -rf ./build ./dist
    $ python ./setup.py sdist bdist_egg bdist_wheel upload -r testpypi

Publish packaging to `PyPi <https://pypi.python.org>`_:

.. code-block:: bash

    $ python ./setup.py register -r pypi
    $ python ./setup.py clean
    $ rm -rf ./build ./dist
    $ python ./setup.py sdist bdist_egg bdist_wheel upload -r pypi

Bump revision back to its development state:

.. code-block:: bash

    $ pip install bumpversion
    $ git checkout develop
    $ bumpversion --verbose patch
    $ git add ./postal_address/__init__.py ./CHANGES.rst
    $ git commit -m "Post release version bump."
    $ git push

Now if the next revision is no longer bug-fix only:

.. code-block:: bash

    $ bumpversion --verbose minor
    $ git add ./postal_address/__init__.py ./CHANGES.rst
    $ git commit -m "Next release no longer bug-fix only. Bump revision."
    $ git push


License
-------

This software is licensed under the `BSD 2-Clause License
<https://github.com/scaleway/postal-address/blob/develop/LICENSE.rst>`_.

ChangeLog
=========


1.2.0 (2016-11-14)
------------------

* Change internal structure of ``InvalidAddress`` exception to print invalid
  field values in error message.
* Update ``pycountry`` to the new calendar-versionned series.
* Allow unittests failure on PyPy3.


1.1.2 (2016-10-25)
------------------

* Keeps ``pycountry`` dependency to the 1.x series.


1.1.1 (2016-09-21)
------------------

* Replace dependency on ``fake-factory`` by ``Faker``.
* Add inactive unittests to highlight un-caught edge-cases in the country/state
  normalization code on derivation from subdivisions. Refs #16.


1.1.0 (2016-05-27)
------------------

* Remove deprecated ``random_word()``, ``random_phrase()`` and
  ``random_postal_code()``.
* Activate tests on Python 3.3.
* Allow production of random chinese addresses.
* Bump ``faker`` requirement to 0.5.4.
* Activate tests on PyPy and PyPy3.


1.0.0 (2016-02-25)
------------------

* Add a new ``territory_children_codes()`` utility to fetch all children of a
  territory.
* Use ``faker`` module to produce fuzzier random addresses.
* Deprecate ``random_word()``, ``random_phrase()`` and
  ``random_postal_code()`` in favor of ``faker`` module.
* Add ``isort`` configuration.
* Only allow string-like types to be set on editable address fields.
* Replace ``awesome-slugify`` dependency by ``boltons``.
* Activate tests on Python 3.5.


0.9.1 (2015-11-23)
------------------

* Switch from coveralls.io to codecov.io.


0.9.0 (2015-09-17)
------------------

* Change license from GPLv2+ to BSD 2-Clause license. Closes #13.
* Add bumpversion configuration.
* Add custom PEP8 and PyLint configuration.


0.8.1 (2015-06-01)
------------------

* Fix bad released version.


0.8.0 (2015-06-01)
------------------

* Normalize all white spaces, not only leadings and trailings.
* Test that the Address object is able to digest unicode messs.
* Normalize postal codes to uppercase alphanumerics with spaces and hyphens.
  Refs #2.


0.7.2 (2015-05-26)
------------------

* Fix encoding of README and CHANGES. Closes #12.


0.7.1 (2015-05-20)
------------------

* Add utility method to generate random addresses for test mockups.


0.7.0 (2015-04-14)
------------------

* Include internal fields disguised as properties when ``repr``-ing the
  ``Address`` object.
* Always use the common name of a country if available instead of its official
  default value.


0.6.1 (2015-04-07)
------------------

* Update all Online Labs references to Scaleway.


0.6.0 (2015-04-02)
------------------

* Add an option to bypass Address' strict normalization.


0.5.2 (2015-03-30)
------------------

* Always sort fields in error messages to improve reproducibility when
  unit testing.
* Deduplicate inconsistent field entries in custom address exception.


0.5.1 (2015-03-30)
------------------

* Fix bad released version.


0.5.0 (2015-03-30)
------------------

* Increase capabilities of alias resolution by ``country_aliases()`` method,
  which in turns increase address normalization efficiency.
* Remove backward compatibility with ``0.3`` series.
* Remove deprecated ``territory.territory_tree()`` method which provided
  backward compatibilityi with the ``0.1`` series. It should have been removed
  in the ``0.3.0`` release.
* Split-up ``supported_territory_codes()`` into ``supported_country_codes()``
  and ``supported_subdivision_codes()``.


0.4.3 (2015-03-26)
------------------

* Fix rendering of subdivision-less addresses.


0.4.2 (2015-03-26)
------------------

* Fix ``country_code`` to ``subdivision_code`` validation if the latter is not
  set.


0.4.1 (2015-03-26)
------------------

* Base our custom ``InvalidAddress`` exception on ``ValueError`` to increase
  backward compatibility.


0.4.0 (2015-03-25)
------------------

* Show subdivision as-is in rendered address if not already printed by state,
  country or city.
* Document stability policy. Closes #8.
* Change internals to refer to address components as ``fields``.
* Raise custom exception on address validation a detailed list of invalid
  fields in one go. Closes #7.


0.3.3 (2015-03-25)
------------------

* Fix bad released version.


0.3.2 (2015-03-25)
------------------

* Add backward compatibility to the ``0.2`` series following territory utils
  split out of the ``address`` module. See #8 and #9.


0.3.1 (2015-03-05)
------------------

* Fix rendering of state in address.


0.3.0 (2015-03-04)
------------------

* Remove backward compatibility with the ``0.1`` series.
* Allow direct import of classes from module root.
* Split territory utils out to their own file. See #3.
* Rename ``normalize_country_code`` to ``country_from_subdivision``. Mark the
  former as deprecated.
* Address normalization is now non-blocking. It simply reset invalid components
  to None. Only a call to ``validate`` method check data consistency.


0.2.1 (2014-12-22)
------------------

* Push a new release to fix cached desynced packages on cheeseshops and clones.


0.2.0 (2014-12-18)
------------------

* Package the whole module for proper distribution.


0.1.1 (2014-12-16)
------------------

* Restore partial backward compatibility with address module from the ``0.1``
  series.


0.1.0 (2014-12-15)
------------------

* First public release.


0.0.0 (2013-12-06)
------------------

* First commit.


