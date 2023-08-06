# -*- coding: utf-8 -*-
"""ldapmgk

Usage:
    ldapmgk [options] user ACTION <username> <email> [<name>]
    ldapmgk [options] group ACTION <groupname>
    ldapmgk [options] group ACTION <groupname> <username>
    ldapmgk [options] servergroup ACTION <groupname> <username>
    ldapmgk --version
    ldapmgk -h

User Arguments:
    ACTION    Use add|remove to add a user or remove it
    ACTION    Use resetpwd to reset a user password

Group Arguments:
    ACTION    Use create|delete to create or remove a group
    ACTION    Use add|remove to add or remvoe a user from a group

Server Group Arguments:
    ACTION    Use add|remove to add or remvoe a user from a server group

Examples:
    ldapmgk user add ldapmgk ldapmk@example.com "ldapmgk user"
    ldapmgk group create vpn
    ldapmgk group add vpn ldapmgk
    ldapmgk servergroup add server_admin ldapmgk
    ldapmgk user resetpwd ldapmgk

Global Options:
    -c, --config=<file>     Configuration file [default:
                            /etc/ldapmgk/config.cfg]
    -o, --output=<file>     Log output to file
    -f, --force             Force some procedures
    -v, --verbose           Verbose output
    -d, --debug             Debug output
    -q, --quiet             Quiet output
    -h, --help              Show this screen
    -V, --version           Show version

"""
from inspect import getmembers, isclass
from docopt import docopt
import sys
import logging
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands

    options = docopt(
        __doc__,
        version="ldapmgk %s" % (VERSION)
    )

    # intialize logging
    if options['--debug'] is True:
        log_level = logging.DEBUG
    elif options['--verbose'] is True:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    log = logging.getLogger("")
    log.setLevel(log_level)

    # stdout handler if needed
    if not (options['--quiet']):
        log_ch = logging.StreamHandler(sys.stdout)
        log_ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        log.addHandler(log_ch)

    # file handler if needed
    if (options['--output']):
        log_fh = logging.FileHandler(options['--output'])
        log_fh.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        log.addHandler(log_fh)

    # dinamically match the command line and load corresponding class
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [
                command[1] for command in commands if command[0] != 'Base'
            ][0]
            command = command(options)
            command.run()
