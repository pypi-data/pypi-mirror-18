#!/usr/bin/env python

import os
import sys
import argparse
import subprocess


def main(args=sys.argv[1:]):
    """
    Manage a virtualenv for a project based on the its path.
    """
    opts = parse_args(args)
    venvdir = get_venv_path(opts.VENVROOT, opts.PROJDIR)
    opts.cmdfunc(venvdir, opts.PROJDIR)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    venvroot_default = '~/.virtualenv-here/venvs'
    p.add_argument(
        '--virtualenv-root',
        dest='VENVROOT',
        default=os.path.expanduser(venvroot_default),
        help='The root for storage of virtualenvs. Default: {}'.format(
            venvroot_default,
        ),
    )

    p.add_argument(
        '--project-dir',
        dest='PROJDIR',
        default='.',
        help='The project directory. Default: .',
    )

    subp = p.add_subparsers()

    cmdnames = set()
    for cmdfunc in [cmd_path, cmd_init, cmd_shell]:
        cmdname = cmdfunc.__name__[len('cmd_'):]
        cmdnames.add(cmdname)
        cmdp = subp.add_parser(cmdname, help=cmdfunc.__doc__)
        cmdp.set_defaults(cmdfunc=cmdfunc)

    if not args or (args[-1] not in cmdnames):
        args = args + ['shell']

    return p.parse_args(args)


def cmd_path(venvdir, _):
    '''Display the virtualenv path for PROJDIR.'''
    print venvdir


def cmd_init(venvdir, projdir):
    '''Initialize a virtualenv for PROJDIR.'''
    display_message('Initializing virtualenv for project: {!r}', projdir)
    subprocess.check_call(['virtualenv', venvdir])


def cmd_shell(venvdir, projdir):
    '''Start a subshell configured for the virtualenv for PROJDIR.'''
    if not os.path.isdir(venvdir):
        cmd_init(venvdir, projdir)

    display_message('Launching subshell for project: {!r}', projdir)

    env = os.environ.copy()
    env.update({
        'PATH': '{}{}{}'.format(
            os.path.join(venvdir, 'bin'),
            os.pathsep,
            env.get('PATH', ''),
        ),
        'VIRTUAL_ENV': venvdir,
        'PS1': '(virtualenv for {!r}) {}'.format(
            projdir,
            env.get('PS1', '\\$ '),
        ),
    })

    status = subprocess.call(
        [env.get('SHELL', '/bin/bash')],
        env=env,
    )
    display_message(
        'Exiting subshell (status {!r}) for project: {!r}',
        status,
        projdir,
    )
    sys.exit(status)


def display_message(tmpl, *args):
    print 'virtualenv-here: {}'.format(tmpl.format(*args))


def get_venv_path(venvroot, projdir):
    absprojdir = os.path.abspath(projdir)

    # FIXME: This assertion may be false for non-unix:
    assert absprojdir.startswith(os.path.sep), (absprojdir, os.path.sep)

    venvname = absprojdir[len(os.path.sep):].replace('/', '.')
    return os.path.join(venvroot, venvname)


if __name__ == '__main__':
    main()
