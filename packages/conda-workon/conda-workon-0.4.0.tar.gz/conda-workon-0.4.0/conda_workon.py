"""A workon command for conda

This implements a ``conda workon <envname>`` command which can be used
to spawn a new shell with the given conda environment activated.

The -l option can also be achieved using ``conda info --envs|-e``.
"""

from __future__ import absolute_import, print_function, division

import argparse
import os
import subprocess
import sys
import tempfile

import conda.config
import conda.misc

try:
    import yaml
except ImportError:
    yaml = None


def main_workon(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available environments',
    )
    parser.add_argument(
        'envname',
        nargs='?',
        help='The environment to activate',
    )
    args = parser.parse_args(argv)
    if args.list:
        for name, prefix in iter_envs():
            print(name)
        sys.exit(0)
    elif not args.envname:
        parser.error('Choose an environment name of list using -l')
    workon(args.envname)


def main_tmp(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--use-local',
        action='store_true',
        help='Use locally built packages',
    )
    parser.add_argument(
        '-f', '--file',
        nargs='?',
        const='environment.yml',
        default=None,
        help='Create environment from yaml specification',
    )
    parser.add_argument(
        '-e', '--editable',
        metavar='<path/url>',
        help='Call pip install -e after creating the environment',
    )
    parser.add_argument(
        'package_spec',
        nargs='*',
        const=None,
        help='Install packages from spec',
    )
    args = parser.parse_args(argv)
    if args.file:
        conda_specs, pip_specs = read_yaml(args.file)
    else:
        conda_specs = []
        pip_specs = []
    if args.package_spec:
        conda_specs.extend(args.package_spec)
    if not conda_specs:
        conda_specs = ['python=3']
    tmpenv(conda_specs, pip_specs,
           use_local=args.use_local, editable=args.editable)


def read_yaml(path):
    """Read and parse the environment.yaml file.

    Returns a tuple of ``(conda_specs, pip_specs)`` of packages
    required by this environment file.

    """
    if not yaml:
        sys.exit('environment.yml support needs '
                 'a YAML parser, please install PyYAML')
    with open(path) as fp:
        data = yaml.load(fp)
    conda_deps = []
    pip_deps = []
    for spec in data['dependencies']:
        if isinstance(spec, str):
            conda_deps.append(spec)
        elif isinstance(spec, dict):
            for dep in spec['pip']:
                if isinstance(dep, str):
                    pip_deps.append(dep)
    return conda_deps, pip_deps


def tmpenv(conda_specs, pip_specs, use_local=False, editable=None):
    if editable and not any(s.startswith('pip') for s in conda_specs):
        conda_specs.append('pip')
    with tempfile.TemporaryDirectory() as tmpdir:
        envdir = os.path.join(tmpdir, 'env')
        binary = os.path.join(bindir(), 'conda')
        args = [binary, 'create', '-p', envdir]
        args.extend(conda_specs)
        if use_local:
            args.insert(2, '--use-local')
        subprocess.check_call(args)
        pip = os.path.join(bindir(envdir), 'pip')
        if pip_specs:
            args = [pip, 'install'] + pip_specs
            subprocess.check_call(args)
        if editable:
            args = [pip, 'install', '-e', editable]
            subprocess.check_call(args)
        workon(envdir)


def workon(env):
    """Activate a conda environment in a subshell.

    :param env: Either the name of an environment or the full prefix
       of an environment.

    """
    path = os.environ['PATH'].split(os.pathsep)
    if os.path.isdir(env):
        envbindir = bindir(env)
    else:
        envbindir = None
    for name, prefix in iter_envs():
        envdir = bindir(prefix)
        try:
            path.remove(envdir)
        except ValueError:
            pass
        if name == env:
            envbindir = envdir
    if not envbindir:
        sys.exit('Unknown environment: {}'.format(env))
    path.insert(0, envbindir)
    environ = os.environ.copy()
    environ['PATH'] = os.pathsep.join(path)
    environ['CONDA_DEFAULT_ENV'] = env
    print('Launching subshell in conda environment.'
          '  Type "exit" or "Ctr-D" to return.')
    sys.exit(subprocess.call(environ['SHELL'], env=environ))


def iter_envs():
    """Iterator of the available conda environments

    Yields (name, prefix) pairs.
    """
    for prefix in conda.misc.list_prefixes():
        if prefix == conda.config.root_dir:
            yield 'root', prefix
        else:
            yield os.path.basename(prefix), prefix


def bindir(env=None):
    """The direcotry where the binaries are stored.

    If env is None the bindir for the root environment is returned.
    """
    if sys.platform == 'win32':
        dirname = 'Scripts'
    else:
        dirname = 'bin'
    if env is None:
        bindir = os.path.join(conda.config.root_dir, dirname)
    else:
        bindir = os.path.join(env, dirname)
    return bindir
