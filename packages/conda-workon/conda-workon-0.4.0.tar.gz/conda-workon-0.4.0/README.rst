============
conda-workon
============

This is a small tool which can be used to activate conda environments.
It is an alternative to using ``source activate <env>`` and instead
uses a conda sub-command to spawn a new shell with the environment
activated.  Deactivating the environment is simply done by exiting
this sub-shell.  This is very similar to, and based on, the ``pew
workon`` command from pew_.  One major advantage of this is that it
does not depend on the shell you use nor does it interact with the
shell at all.  This means it is not restricted to bash and zsh.

.. _pew: https://pypi.python.org/pypi/pew

Activating an environment simply looks like this::

   $ conda create -n py26 python=2.6
   ...
   $ conda info -e
   # conda environments:
   #
   py26                     /home/flub/miniconda3/envs/py26
   root                  *  /home/flub/miniconda3
   $ conda workon py26
   Launching subshell in conda environment.  Type "exit" or "Ctr-D" to return.
   (py26) $ conda info -e
   # conda environments:
   #
   py26                  *  /home/flub/miniconda3/envs/py26
   root                     /home/flub/miniconda3
   (py26) $ exit
   $ conda info -e
   # conda environments:
   #
   py26                     /home/flub/miniconda3/envs/py26
   root                  *  /home/flub/miniconda3

Listing the available environments can be done using either ``conda
workon -l|--list`` or using the standard ``conda env list`` or ``conda
info -e|--envs``.

Another feature is that it provides an easy throw-away temporary
environment based on a package spec on the command line::

   $ conda worktmp python=3.4 sphinx
   Fetching package metadata: ..
   Solving package specifications: .
   Package plan for installation in environment /tmp/tmp7ua0_le9/env:
   ...
   Proceed ([y]/n)? y
   ...
   Launching subshell in conda environment.  Type "exit" or "Ctr-D" to return.
   $ conda info | grep default
     default environment : /tmp/tmp7ua0_le9/env
   $ exit
   $ conda info | grep default
     default environment : /home/flub/miniconda3
   $

Likewise a temporary environment can be created from an
environment.yml file::

   $ conda worktmp -f path/to/environment.yml
   ...
   Launching subshell in conda environment.  Type "exit" or "Ctr-D" to return.

If ``-f|--file`` is used without an argument this will look for
``environment.yml`` in the current directory.  When using ``worktmp``
one can also directly invoke ``pip -e <path>`` by using the
``-e|--editable`` option.  This is convenient to start developing on a
package::

   $ conda worktmp -f -e.
   ...
   Proceed ([y]/n)? y
   ...
     Running setup.py develop for foo
   Successfully installed foo
   Launching subshell in conda environment.  Type "exit" or "Ctr-D" to return.
   $


Installation
============

The ``conda-workon`` command needs to be installed in the root conda
environment.

Using pip
---------

Ensure you have ``pip`` installed in the conda root environment using
``conda install pip``.  Then making sure to use this version of pip
install ``conda-workon`` using::

  $ pip install conda-workon

Using conda
-----------

The conda-forge project packages ``conda-workon`` so you can install
it once you have added the conda-forge channels::

   conda config --add channels conda-forge
   conda install conda-workon


Configuring the Prompt
======================

The ``conda-workon`` command does not interfere with the shell at all,
it simply starts a new sub-shell with a modified path.  This means
that by default the prompt of the shell will not indicate which conda
environment you are using.  However the currently activated conda
environment is available in the ``CONDA_DEFAULT_ENV`` environment
variable, which allows you to easily configure your shell as you
prefer.  A simple example using the fish shell is to include the
following fragment in the ``fish_prompt`` function::

   # Show the conda environment, calculate __fish_prompt_conda only once
   if set -q CONDA_DEFAULT_ENV
       if not set -q __fish_prompt_conda
           set -g __fish_prompt_conda (set_color --bold -b blue red)$CONDA_DEFAULT_ENV"$__fish_prompt_normal "
       end
       echo -n $__fish_prompt_conda
   end


Changelog
=========

0.4
---

* Split into two commands: ``conda-workon`` and ``conda-worktmp``.

* Implement listing using ``conda-workon -l|--list``.

* Add support for using environment.yml using ``conda-worktmp -f|--file``.

* Add support for directly calling ``pip -e <path>`` using
  ``conda-worktmp -e|--editable <path>``.


0.3
---

* Add a ``--use-local`` option to use together with ``--tmp``.  This
  will use ``conda create --use-local`` to create the environment.

* Use the conda binary invoked rather then looking it up on the PATH.
