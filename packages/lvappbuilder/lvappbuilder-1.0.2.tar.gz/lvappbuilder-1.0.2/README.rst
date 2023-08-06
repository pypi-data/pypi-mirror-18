pylvappbuilder
==============

API for LabVIEW Application Builder.

`Sources <https://github.com/gergelyk/pylvappbuilder>`_

`Package <https://pypi.python.org/pypi/lvappbuilder>`_

Introduction
------------

This library has been created to enable LabVIEW users build their projects in command line. This is an important step for these who attempt to automate build process for instance as a part of `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ concept.

Primarly pylvappbuilder was intended to provide it's functionality to `pydoit <http://pydoit.org/>`_. Even though, other tools that can cooperate with Python are welcome too.

**Advantages** of using pylvappbuilder include:

* One-click solution for building multiple variants of the software.
* Possibility of defining Conditional Disable Symbols for each build of the LabVIEW project.
* Possibility of sourcing separate builds with the same version number without need of editing LabVIEW project manually.

In conjunction with pydoit, additional **user-defined actions** can be specified too. For instance:

* Running tests againgst the sources.
* Building a package based on LabVIEW project.
* Installing/uninstalling sources in directories of LabVIEW installation.
* Publishing the sources.

Requirements
------------

* Library has been developed for Windows operating system. However small modifications can make it also usable under other operating systems.
* VIs that library consists of have been created in LabVIEW 2015, thus pylvappbuilder supports >= LabVIEW 2015. If older versions of LabVIEW have to be supported, VIs should be saved in a way which is compatible with that version (use `Save for Previous Version` option in LabVIEW).
* Library has been tested against build definitions definded under `My computer`, which means against building Windows applications. However other targets like RT, FPGA are expected to be supported too, without need of making any modifications.

Usage
-----

Example project can be found in ``pylvappbuilder/example/``. To try it out, one should:

1. Make sure that LabVIEW 2015, Python interpreter, as well as the packages: ``pylvappbuilder`` and ``doit`` are installed in the system.
2. Close all instances of LabVIEW (or they will be killed otherwise).
3. Open system shell prompt in ``pylvappbuilder/example`` and invoke:

::

    doit

3. As an effect, two variants of the project will be built and stored in subdirectories ``build\Debug`` and ``build\Release``.
4. Finally workspace can be cleaned by invoking:

::

    doit clean

Documentation
-------------

Currently no formal documentation for this API exists. All the functions however have self-explanatory names and are documented in the code. Additionally, library includes ``act`` submodule which defines actions that seem to represent the most common usage of the API. **Actions defined in** ``act`` **submodule can be used by pydodit as they are, or they can be used as templates for defining other actions.**








