.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 12:57:10 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.avspoof/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.avspoof/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.avspoof/badges/v2.2.4/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.avspoof/commits/v2.2.4
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.avspoof
.. image:: http://img.shields.io/pypi/v/bob.db.avspoof.png
   :target: https://pypi.python.org/pypi/bob.db.avspoof
.. image:: http://img.shields.io/pypi/dm/bob.db.avspoof.png
   :target: https://pypi.python.org/pypi/bob.db.avspoof


====================================
 AVspoof Database Interface for Bob
====================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains the access API and descriptions for the AVspoof_ Database.
The database contains speech recordings of 44 persons (31 males and 13 females)
performed during the course of two months in four different sessions. The
database also contains several spoofing attacks for the recorded speech,
including voice conversion, speech synthesis, and replay attacks.  Replay
attacks were performed using laptop or two different phones.

This package contains the Bob_-compliant interface implementation with methods
to use the database directly from Python with our certified protocols.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
.. _avspoof: https://www.idiap.ch/dataset/avspoof
