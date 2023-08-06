Craftr 2.x
==========

|PyPI Version| |CII Best Practices|

    Note: Craftr 2.x is different from the initial Craftr version in
    many ways and can not be used interchangibly. The latest version of
    Craftr 1.x can be found under the
    `v1.1.4-unreleased <https://github.com/craftr-build/craftr/tree/v1.1.4-unreleased>`__
    tag.

Craftr is a meta build system based on `Python
3 <https://www.python.org/>`__ scripts which produces
`Ninja <https://github.com/ninja-build/ninja>`__ build manifests. It
enforces the use of modular build definitions that can be re-used
easily. Craftr provides a standard library to support various
programming languages and common libraries out of the box:

-  C/C++ (cURL, DLib, GoogleTest, GoogleBenchmark, tiny-dnn, Qt5, Boost,
   getopt)
-  Cython
-  C#
-  Java
-  Vala

Additional links:

-  `Documentation <https://github.com/craftr-build/craftr/tree/master/doc>`__
-  `Getting
   Started <https://github.com/craftr-build/craftr/tree/master/doc/getting-started.md>`__
-  `Craftr 2.x Wiki <https://github.com/craftr-build/craftr/wiki>`__

Features
--------

-  [x] Moduler build scripts (Craftr packages) with dependency
   management
-  [x] Loaders: if required, automatically download and build libraries
   from source!
-  [ ] Package manager (hosted on `Craftr.net <https://craftr.net>`__)
-  [ ] Embed actual Python functions into the build graph
-  [ ] Dependency-version lockfiles

Contributions
-------------

Craftr is a one-man-show and an immature piece of software. I am happy
about every contribution and feedback, be it questions, criticism,
feature requests, bug reports or pull requests!

I would love to see Craftr used by more people. If you think it's worth
to give it a shot, don't hesitate to ask if you're getting stuck!

Issue Tracker: https://github.com/craftr-build/craftr/issues Twitter:
[@rosensteinn](twitter.com/rosensteinn)
[@craftr\_build](https://twitter.com/craftr\_build)

Installation
------------

Craftr 2.x does not have a stable release yet, though the ``2.0.0.devx``
tags are already available on PyPI. If you do not explicitly specify the
version number, Pip will install Craftr 1.x.

::

    $ pip install craftr-build==2.0.0.dev5

To get the cutting edge development version, I suggest installing Craftr
from the Git repository into a virtualenv.

::

    $ virtualenv -p python3 env && source env/bin/activate
    $ git clone https://github.com/craftr-build/craftr.git -b development
    $ cd craftr
    $ pip install -e .

Requirements
------------

-  `Ninja <https://github.com/ninja-build/ninja>`__ 1.7.1 or newer
-  `Python <https://www.python.org/>`__ 3.4, 3.5

Python
~~~~~~

-  `colorama <https://pypi.python.org/pypi/colorama>`__ (optional,
   Windows)
-  `glob2 <https://pypi.python.org/pypi/glob2>`__
-  `jsonschema <https://pypi.python.org/pypi/jsonschema>`__
-  `ninja\_syntax <https://pypi.python.org/pypi/ninja_syntax>`__
-  `nr <https://pypi.python.org/pypi/nr>`__
-  `py-require <https://pypi.python.org/pypi/py-require>`__
-  `termcolor <https://pypi.python.org/pypi/termcolor>`__ (optional)
-  `werkzeug <https://pypi.python.org/pypi/werkzeug>`__

License
-------

::

    The Craftr build system
    Copyright (C) 2016  Niklas Rosenstein

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

For more information, see the ``LICENSE.txt`` file.

.. |PyPI Version| image:: https://img.shields.io/pypi/v/craftr-build.svg
   :target: https://pypi.python.org/pypi/craftr-build
.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/530/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/530
