import functools
import os
import shlex
import subprocess
import sys

from nearby.exceptions import MissingDependencyException


def requires(*dependencies):
    """
    Decorator that ensures dependencies exist at first function invocation

    Assumes `which` exists.
    """
    def decorator(f):
        has_checked_deps = False

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal has_checked_deps
            if not has_checked_deps:
                for dep in dependencies:
                    try:
                        subprocess.run(
                            ['which', dep],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            check=True)
                    except subprocess.CalledProcessError:
                        raise MissingDependencyException(
                            'Local {} install not found'.format(dep))
                has_checked_deps = True
            return f(*args, **kwargs)
        return wrapper
    return decorator


@requires('sshfs')
def mount(host, user, local_path, remote_path):
    host_dir = os.path.join(local_path, host)
    if os.path.exists(host_dir):
        print('{} already exists. Exiting.'.format(host_dir))
        sys.exit(1)

    conn_str = '{user}@{host}:{path}'.format(
        user=user,
        host=host,
        path=remote_path)
    if not os.path.exists(host_dir):
        _create_dirs(host_dir)
    command = 'sshfs {conn_str} {host_dir}'.format(
        conn_str=conn_str, host_dir=host_dir)
    _shell(command)


@requires('fusermount')
def unmount(host, local_path):
    host_dir = os.path.join(local_path, host)
    command = 'fusermount -u {host_dir}'.format(host_dir=host_dir)
    _shell(command)
    _remove_dir(host_dir, local_path)


def _shell(command):
    print('Running {}'.format(command))
    args = shlex.split(command)
    try:
        subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
    except (subprocess.CalledProcessError) as e:
        print('Error running {}'.format(command))
        print('subprocess stdout: {}'.format(
            e.output[:10000].decode('utf-8') + '[...snip]'))
        raise


def _create_dirs(path):
    print('{} not found. Creating now...'.format(path))
    os.makedirs(path)


def _remove_dir(path, base_path):
    abs_path = os.path.abspath(path)
    abs_base = os.path.abspath(base_path)
    in_common = os.path.commonprefix([abs_base, abs_path])
    # only delete subdirs of base_path
    if in_common == abs_base and not abs_path == abs_base:
        print('Removing directory {}'.format(abs_path))
        os.rmdir(abs_path)
    else:
        print('{} must be a subdirectory of {}. Skipping.'.format(
            path, abs_base
        ))
        sys.exit(1)
