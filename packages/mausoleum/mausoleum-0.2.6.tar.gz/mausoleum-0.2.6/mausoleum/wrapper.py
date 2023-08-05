import subprocess

import click


def dig_tomb(name, size):
    """Dig a new tomb container.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    size -- the size of the container in megabytes
    """
    return subprocess.call(['tomb', 'dig', '-s', str(size), name])


def forge_tomb(key, password, sudo=None, debug=False):
    """Forge a new key for a tomb container.

    Positional arguments:
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password to be used with the key

    Keyword arguments:
    sudo -- the sudo password of the current admin, default is None
    debug -- used to test key generation
    """
    arguments = ['sudo', '--stdin', 'tomb', 'forge', '--unsafe', '--tomb-pwd', password, key]
    if debug:
        arguments.extend(['--ignore-swap', '--use-urandom'])
    if sudo is not None:
        forge_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, universal_newlines=True)
        return forge_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def lock_tomb(name, key, password, sudo=None, debug=False):
    """Lock a tomb container with the given key.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key

    Keyword arguments:
    sudo -- the sudo password of the current admin, default is None
    debug -- used to ignore the swap partition
    """
    arguments = ['sudo', '--stdin', 'tomb', 'lock', '--unsafe', '--tomb-pwd',
                 password, name, '-k', key]
    if debug:
        arguments.append('--ignore-swap')
    if sudo is not None:
        lock_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, universal_newlines=True)
        return lock_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def open_tomb(name, key, password, sudo=None):
    """Open a tomb container with the given key.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key

    Keyword arguments:
    sudo -- the sudo password of the current admin, default is None
    """
    arguments = ['sudo', '--stdin', 'tomb', 'open', '--unsafe',
                 '--tomb-pwd', password, name, '-k', key]
    if sudo is not None:
        open_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, universal_newlines=True)
        return open_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def resize_tomb(name, size, key, password):
    """Resize a tomb container to the given size.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    size -- the size of the container in megabytes
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key
    """
    return subprocess.call(['tomb', 'resize', name, '-s', str(size), '-k', key, '--unsafe',
                            '--tomb-pwd', password])


def list_tombs():
    """Create a list of all open tombs."""
    try:
        tomb_output = subprocess.check_output(['tomb', 'list', '--no-color'],
                                              stderr=subprocess.STDOUT,
                                              universal_newlines=True).split('\n')
        return [line.replace('tomb  .  ', '') for line in tomb_output if 'open on' in line]
    except subprocess.CalledProcessError:
        return []


def close_tomb(name=None):
    """Close an open tomb container.

    Positional argument:
    name -- the name of the container to close (if multiple tombs are open)
    """
    return subprocess.call(['tomb', 'close'])


def close_tombs():
    """Close all open tombs."""
    return subprocess.call(['tomb', 'close', 'all'])


def slam_tombs():
    """Force close all open tombs."""
    return subprocess.call(['tomb', 'slam'])


@click.group()
def cli():
    """Access Tomb's command line interface with Mausoleum.

    Mausoleum includes multiple commands that wrap around Tomb's command line interface:
    $  mausoleum construct [OPTIONS] NAME SIZE [KEY]
    $  mausoleum enter [OPTIONS] NAME [KEY]
    $  mausoleum alter [OPTIONS] NAME SIZE [KEY]

    To create and open a new 500MB tomb container and key, run:
    $  mausoleum construct --open secret.tomb 500

    To open an existing tomb container, run:
    $  mausoleum enter secret.tomb

    To resize an existing tomb container to 20MB, run:
    $  mausoleum alter secret.tomb 20
    """


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
@click.password_option()
@click.option('--open', is_flag=True, help='Open a tomb after constructing it.')
def construct(name, size, key, password, open):
    """Dig, forge, and lock a new tomb container.

    The default key name is the name of the tomb with .key appended as the suffix. If
    you would like the key to use a different naming convention, it must be passed as an
    argument.

    To open the container after creation, use the --open flag.
    """
    construction = dig_tomb(name, size)
    if key is None:
        key = '{}.key' .format(name)
    if construction == 0:
        fabrication = forge_tomb(key, password)
        if fabrication == 0:
            lock_tomb(name, key, password)
            if open:
                open_tomb(name, key, password)


@cli.command()
@click.argument('name')
@click.argument('key', required=False, default=None)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
def enter(name, key, password):
    """Open an existing tomb container.

    The default key name is the name of the tomb with .key as the suffix. If the
    key uses a different naming convention, it must be passed as an argument.
    """
    if key is None:
        key = '{}.key' .format(name)
    open_tomb(name, key, password)


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--open', is_flag=True, help='Open the tomb after resizing it.')
def alter(name, size, key, password, open):
    """Resize an existing tomb container.

    The default key name is the name of the tomb with .key as the suffix. If the
    key uses a different naming convention, it must be passed as an argument.

    To open the container after resizing, use the --open flag.
    """
    if key is None:
        key = '{}.key' .format(name)
    resize_tomb(name, str(size), key, password)
    if open:
        open_tomb(name, key, password)
