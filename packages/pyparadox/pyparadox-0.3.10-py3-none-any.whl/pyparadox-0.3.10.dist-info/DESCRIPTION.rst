===============================
PyParadox
===============================

.. image:: https://img.shields.io/pypi/v/pyparadox.svg
    :target: https://pypi.python.org/pypi/pyparadox
.. image:: https://img.shields.io/pypi/pyversions/pyparadox.svg
    :target: https://pypi.python.org/pypi/pyparadox
.. image:: https://img.shields.io/pypi/format/pyparadox.svg
    :target: https://pypi.python.org/pypi/pyparadox
.. image:: https://img.shields.io/pypi/l/pyparadox.svg
    :target: https://www.gnu.org/copyleft/gpl.html


PyParadox is a nix launcher for Paradox titles.

* Free software: GPLv3+
* Documentation: https://pyparadox.readthedocs.org
* Source code: https://gitlab.com/carmenbbakker/pyparadox
* PyPI: https://pypi.python.org/pypi/pyparadox

.. image:: http://i.imgur.com/f21Pesf.png

Requirements
------------

* Operating system:

  * Linux: Any modern distribution with up-to-date packages
  * OS X: Latest version
  * Windows: 7 and later

* Python: 3.3+
* Qt: Qt 5.3+ via PyQt5

Features
--------

* Games: PyParadox supports all cross-platform grand strategy titles of
  Paradox Interactive that use the Clausewitz engine.  To date, these include:

  * Crusader Kings II
  * Europa Universalis IV
  * Stellaris

* Steam: PyParadox can be launched from Steam when starting the title from the
  Steam interface.  All Steam integration should work just fine.  A small
  configuration inside Steam is required to make sure that PyParadox is used
  instead of the stock launcher.  See the documentatation on how to set this
  up.
* PyParadox separates the expansion DLCs from the regular DLCs.  This should
  make it easier to start up your game with the exact expansions you want.
* PyParadox fixes an anomaly under Linux that causes the game to mess with
  the screen resolution when alt+tabbing.  This anomaly was introduced when
  Paradox released their (new) stock launcher for Linux.  By bypassing this
  launcher, PyParadox also bypasses the anomaly.

Installation
------------

`Read the documentation
<https://pyparadox.readthedocs.org/en/latest/installation.html>`_.




=======
History
=======

0.3.10 (2016-11-17)
------------------

* Added The Reaper's Due and Rights of Man.

0.3.9 (2016-05-13)
------------------

* Added Mare Nostrum EU4 expansion.

0.3.8 (2016-05-12)
------------------

* Added Stellaris.

0.3.7 (2016-02-13)
------------------

* Added Conclave and The Cossacks to expansions.
* Added testing for gui module.

0.3.6 (2016-01-29)
------------------

* Improved logging.
* Improved main algorithm.
* Raise error on Python < 3.3 installation attempts.
* Improved documentation.
* Added COPYING file.  Apparently this was lacking all along.

0.3.5 (2015-08-17)
------------------

* Added basic logging.

0.3.4 (2015-08-09)
------------------

* Moved Linux default game directory from ``~/.local/share/Steam/...`` to
  ``~/.steam/root/...``.  The former directory was deprecated by Ubuntu, but
  not by Arch.  The latter directory works on both distributions.
* Fixed OS X compatibility.  Now launches the game correctly.

0.3.3 (2015-07-23)
------------------

* Fixed bug that caused ``pyparadox-qml`` to fail to launch.  This presumably
  only happens in more recent versions of Qt/PyQt5.

0.3.2 (2015-07-18)
------------------

* Added new expansions to the list of expansions.

0.3.1 (2015-04-23)
------------------

* Scrollbars in the QML front-end are now always visible.
* QML front-end now uses the absolute minimum imports that I could find.  This
  has resulted in the use of Qt 5.3 rather than Qt 5.2.  It is still possible
  to use Qt 5.1 with the QtWidgets version.

0.3.0 (2015-04-23)
------------------

* Implemented QML front-end that is almost identical to the QtWidgets
  front-end.  This is a proof of concept to indicate that the backend is fairly
  decoupled.  There *is* some code repetition, but almost no reptition in
  business logic.  Then again, the business logic of this program is fairly
  small.

0.2.3 (2015-04-17)
------------------

* Added error message when program fails to launch.
* Greatly improved documentation.
* Fixed bug that caused a failed launch on Ubuntu 14.04.  Incidentally, this
  also causes the menu bar to be used locally rather than integrated into the
  top panel bar.  Fortunately, PyParadox doesn't *have* a menu bar.  Yet.

0.2.2 (2015-04-12)
------------------

* Patched a bug that caused PyParadox to fail to launch from Steam.
* Removed Python 2.7 support from PyPI.

0.2.1 (2015-04-11)
------------------

* Minor patches to documentation because apparently I can't release anything
  without messing that stuff up.

0.2.0 (2015-04-11)
------------------

* Complete rewrite of the project, with reuse of some code.
* Now no longer supports Python 2.7 and Qt 4.  This program will only work with
  Python 3.3+ and PyQt5.
* Configuration files relocated to a different location.  Old configuration
  files no longer valid.
* Graphical user interface makes use of Qt .ui files, rather than hardcoded
  QtGui/QtWidgets code.
* A lot of functionality has been decoupled from the user interface.  While the
  UI code performs *some* glue logic, it should be relatively trivial to cook
  up a user interface in a different framework.  An experimental QML front-end
  is under consideration.
* Unit tests are a lot leaner, using fewer mocks and patches, instead relying
  much more on dependency injection.
* Documentation rewritten.

0.1.3 (2015-01-31)
------------------

* Added --pyqt4 argument to force the usage of PyQt4.
* Fixed PyQt4 compatibility issues.

0.1.2 (2014-07-20)
------------------

* Fixed typo that caused README to display incorrectly.

0.1.1 (2014-07-20)
------------------

* Sweetened up the README with images of the program.

0.1.0 (2014-07-20)
------------------

* Added descriptive error message when game fails to run.
* Added experimental PyQt4 support.
* Detailed installation instructions per platform added.
* A logo of each game is now displayed.
* Mods and DLCs are now sorted.
* The application now has an icon.

0.0.2 (2014-07-13)
------------------

* Windows compatibility added.
* Window titles set correctly.
* Small UI tweaks (alt-shortcuts).
* Better game process management.
* Better unit testing, though incomplete.
* Just general code refactoring.
* Tested on Kubuntu 14.04 and Windows 8.1.  Still not sure about OS X.

0.0.1 (2014-07-10)
------------------

* First release on PyPI.
* Basic functionality.  No polish yet.
* Only tested on Kubuntu 14.04.


