.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

================================================
Mercurial All Paths extension
================================================

Push or pull to many (or all) paths at once. 
|drone-badge|

.. contents::
   :local:
   :depth: 2

.. sectnum::

Basic usage
================================================

Execute::

    hg pushall

to push to all remotes which are defined for the repository. Or::

    hg pullall

to pull from all remotes in order.

There are also::

    hg incomingall

    hg outgoingall

Standard push/pull options can be given, for example::

    hg pushall -f -B issue-13724

    hg pullall -r stable --insecure

Those commands iterate over all paths returned by ``hg paths``.  This
usually means iterating over paths defined in ``[paths]`` section of
``.hg/hgrc``, but `Path Pattern`_ paths are also handled. You can
impact this behaviour by configuration, see below.


Defining path groups
================================================

Instead of pushing/pulling everywhere, you can define and use *groups*::

    hg pushall -g publish

pushes to all paths from the ``publish`` group (where ``publish`` is
symbolic name of your choosing). Or::

    hg pullall -g shared

pulls from all paths in ``shared`` group.

There are two ways to define such a group:

1. Define appropriate entry in ``[all_paths]`` section (either in ``.hg/hgrc``
   or in your global ``~/.hgrc``). For example::

     [all_paths]
     group.publish = bitbucket github backup

   (path aliases ``bitbucket``, ``github`` and ``backup`` must
   be somehow defined).

2. (Legacy method) Put the section of the same name in ``.hg/hgrc``,
   and define all paths there. For example::

    [publish]
    bitbucket = ssh://hg@bitbucket.org/ludovicchabant/piecrust
    github = git+ssh://git@github.com:ludovicchabant/PieCrust.git
    backup = ssh://ludo@backup.local/piecrust

   The syntax is the same as in standard ``[paths]`` section, just
   name the section with the name of your group.

   .. note::

      Be careful to avoid conflicts with names which mean something
      to Mercurial. For example ``web`` would be a bad name as ``[web]``
      section configures ``hg serve`` behaviour, and ``ui`` would be
      fatal as ``[ui]`` configures various basic Mercurial settings.

I recommend the former method as it avoids the risk of conflicts,
makes it easy to define groups globally instead of defining them for
every repository (especially handy if you use `Path Pattern`_), and is
more compact.

Groups are also handled for ``incomingall`` and ``outgoingall``, but
long ``--group`` option must be used (``-g`` is already taken by
standard Mercurial, means reporting in ``--git`` diff format)::

     hg outgoingall --group publish

Configuration
=======================================================

The extension can be configured using ``[all_paths]`` section of your
global (``~/.hgrc``) or repository-level (``.hg/hgrc``) config file::

  [all_paths]
  prioritize = platon department
  ignore = bitbucket production
  group.publish = github bitbucket
  group.backup = homebackup awsbackup

``prioritize`` impacts the order, defines paths which are to be
handled first (if present). This is mostly useful for ``pullall``
where pulling from local fast computer before pulling from BitBucket
server means saving some time and traffic. So::

  prioritize = platon department

means: if path named ``platon`` is present, handle it first, then
path named ``department``, only then follow to other paths.

``ignore`` lists paths which should be ignored, those remotes will
be skipped. So::

  ignore = bitbucket production

means that ``hg pullall`` or ``hg pushall`` should not use
``bitbucket`` path (in my case because this is HTTP remote, and I have
also preferable ``bitssh``configured), and ``production`` path (as
there I prefer to pull and push only on specific demand).

Both those settings impact only *default* commands (those run
without ``-g GROUP`` option). In case of groups items are processed
in the order they are specified in group definition.

``group.«NAME»`` define group for ``-g «NAME»`` as described earlier. 


Installation
=======================================================

From PyPi
--------------------

If you have working ``pip`` or ``easy_install``::

    pip install --user mercurial_all_paths

or maybe::

    sudo pip install mercurial_all_paths

Then activate by::

    [extensions]
    mercurial_all_paths =

To upgrade, repeat the same command with ``--upgrade`` option, for
example::

    pip install --user --upgrade mercurial_all_paths

From source
-------------------------------------------------------

Clone this repository::

    cd ~/sources
    hg clone https://bitbucket.org/Mekk/mercurial-all_paths/

either::

    pip install --user -e mercurial-all_paths

and activate as above, or just activate by full path::

    [extensions]
    mercurial_path_pattern = ~/sources/mercurial-path_pattern/mercurial_path_pattern.py

To upgrade, pull and update.

History
=======================================================

See `HISTORY.txt`_

Development
=======================================================

Main extension repository, maintained by Ludovic Chabant, is available
at:

    https://bitbucket.org/ludovicchabant/allpaths

Fork by Marcin Kasperski, which is usually in sync, but at times may
contain some not-yet merged changes, is available at:

    http://bitbucket.org/Mekk/mercurial-all_paths/

Additional notes
=======================================================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/AllPathsExtension


.. _Path Pattern: https://bitbucket.org/Mekk/mercurial-path_pattern/
.. _HISTORY.txt: http://bitbucket.org/Mekk/mercurial-all_paths/src/tip/HISTORY.txt

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mercurial-all_paths/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mercurial-all_paths/latest
     :align: middle
