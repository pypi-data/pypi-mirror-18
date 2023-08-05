Overview of Solar Flares
========================

..  start-badges

|buildstatus| |docs|

.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/solar-flares.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/metrasynth/solar-flares

.. |docs| image:: https://readthedocs.org/projects/solar-flares/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://solar-flares.readthedocs.io/en/latest/?badge=latest

..  end-badges

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Purpose
-------

Sound design and performance tools for SunVox.


Tools included
--------------

Module Polyphonist
  Converts most monophonic-only MetaModules into polyphonic MetaModules
  that support up to 16 simultaneous voices while keeping controller
  values synchronized.

Pattern Polyphonist
  Converts a pattern that uses a standard module into one that
  rotates through the available voices of a polyphonic MetaModule.


Tools under development
-----------------------

MetaModule Construction Kit
  A MetaModule construction kit based on a mixture of: creating modules
  and initial controller settings via code; direct manipulation of code inputs
  and controller values; customized mapping of controllers and
  controller groups to the final MetaModule.

FM-n Construction Kit
  An application of the MetaModule Construction Kit and Module Polyphonist
  for creating and patching n-controller polyphonic FM synthesizers.


Support for dynamic UIs
-----------------------

Solar Flares has no interactive UI of its own;
it interacts with dynamic UIs through data structures
and hints.

Metrasynth `Solar Sails`_ is one such project:
a desktop app for Linux, Mac, and Windows
that wraps the Solar Flares tools.


Requirements
------------

- Python 3.5
