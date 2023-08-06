# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Kevin Deldycke <kevin@deldycke.com>
#                    and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from __future__ import absolute_import, division, print_function

import logging
from json import dumps as json_dumps
from operator import itemgetter

import click
import click_log
from tabulate import tabulate

from . import __version__, logger
from .managers import pool

# Output rendering modes. From machine to human-readable.
RENDERING_MODES = {
    'json': 'json',
    # Mapping of table formating options to tabulate's parameters.
    'plain': 'plain',
    'simple': 'simple',
    'fancy': 'fancy_grid'}


def json(data):
    """ Utility function to render data structure into pretty printed JSON. """
    return json_dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


@click.group(invoke_without_command=True)
@click_log.init(logger)
@click_log.simple_verbosity_option(
    default='INFO', metavar='LEVEL',
    help='Either CRITICAL, ERROR, WARNING, INFO or DEBUG. Defaults to INFO.')
@click.option(
    '-o', '--output-format', type=click.Choice(RENDERING_MODES),
    default='fancy', help="Rendering mode of the output. Defaults to fancy.")
@click.version_option(__version__)
@click.pass_context
def cli(ctx, output_format):
    """ CLI for multi-package manager updates and upgrades. """
    level = click_log.get_level()
    level_name = logging._levelNames.get(level, level)
    logger.debug('Verbosity set to {}.'.format(level_name))

    # Print help screen and exit if no sub-commands provided.
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()

    # Load up global options to the context.
    ctx.obj = {
        'rendering': RENDERING_MODES[output_format]}

    # Silent all log message in JSON rendering mode unless it's at debug level.
    if ctx.obj['rendering'] == 'json' and level_name != 'DEBUG':
        click_log.set_level(logging.CRITICAL * 2)


@cli.command(short_help='List supported package managers and their location.')
@click.pass_context
def managers(ctx):
    """ List all supported package managers and their presence on the system.
    """
    rendering = ctx.obj['rendering']

    # Machine-friendly data rendering.
    if rendering == 'json':
        fields = [
            'name', 'id', 'cli_path', 'exists', 'executable', 'version_string',
            'supported', 'available']
        # JSON mode use print to output data because the logger is disabled.
        print(json({
            manager_id: {fid: getattr(manager, fid) for fid in fields}
            for manager_id, manager in pool().items()}))
        return

    # Human-friendly content rendering.
    table = []
    for manager_id, manager in pool().items():
        table.append([
            manager.name,
            manager_id,
            manager.cli_path,
            u'✅' if manager.exists else '',
            u'✅' if manager.executable else '',
            u"{}  {}".format(
                u'✅' if manager.supported else u'❌',
                manager.version if manager.version else '')
            if manager.exists else ''])
    table = [[
        'Package manager', 'ID', 'CLI path', 'Found', 'Executable',
        'Version']] + sorted(table, key=itemgetter(1))
    logger.info(tabulate(table, tablefmt=rendering, headers='firstrow'))


@cli.command(short_help='Sync local package info.')
@click.pass_context
def sync(ctx):
    """ Sync local package metadata and info from external sources. """
    for manager_id, manager in pool().items():

        # Filters-out inactive managers.
        if not manager.available:
            logger.warning('Skip unavailable {} manager.'.format(manager_id))
            continue

        manager.sync()


@cli.command(short_help='List available updates.')
@click.pass_context
def outdated(ctx):
    """ List available package updates and their versions for each manager. """
    # Build-up a global list of outdated packages per manager.
    outdated = {}

    for manager_id, manager in pool().items():

        # Filters-out inactive managers.
        if not manager.available:
            logger.warning('Skip unavailable {} manager.'.format(manager_id))
            continue

        # Force a sync to get the freshest updates.
        manager.sync()

        if manager.error:
            logger.error(manager.error)

        outdated[manager_id] = {
            'id': manager_id,
            'name': manager.name,
            'packages': [{
                'name': pkg_info['name'],
                'id': pkg_info['name'],
                'installed_version': pkg_info['installed_version'],
                'latest_version': pkg_info['latest_version']}
                for pkg_info in manager.updates]}

    rendering = ctx.obj['rendering']

    # Machine-friendly data rendering.
    if rendering == 'json':
        # JSON mode use print to output data because the logger is disabled.
        print(json(outdated))
        return

    # Human-friendly content rendering.
    table = []
    for manager_id, outdated_pkg in outdated.items():
        table += [[
            pkg_info['name'],
            pkg_info['id'],
            manager_id,
            pkg_info['installed_version'],
            pkg_info['latest_version']]
            for pkg_info in outdated_pkg['packages']]

    def sort_method(line):
        """ Force sorting by lower-cased package ID first, then manager ID. """
        return line[1].lower(), line[2]

    # Sort and print table.
    table = [[
        'Package name', 'ID', 'Manager', 'Installed version',
        'Latest version']] + sorted(table, key=sort_method)
    logger.info(tabulate(table, tablefmt=rendering, headers='firstrow'))
    # Print statistics.
    manager_stats = {
        manager_id: len(packages) for manager_id, packages in outdated.items()}
    total_outdated = sum(manager_stats.values())
    per_manager_totals = ', '.join([
        '{} from {}'.format(v, k) for k, v in sorted(manager_stats.items())])
    if per_manager_totals:
        per_manager_totals = ' ({})'.format(per_manager_totals)
    logger.info('{} outdated package{} found{}.'.format(
        total_outdated,
        's' if total_outdated > 1 else '',
        per_manager_totals))


@cli.command(short_help='Update all packages.')
@click.pass_context
def update(ctx):
    """ Perform a full package update on all available managers. """
    for manager_id, manager in pool().items():

        # Filters-out inactive managers.
        if not manager.available:
            logger.warning('Skip unavailable {} manager.'.format(manager_id))
            continue

        logger.info(
            'Updating all outdated packages from {}...'.format(manager_id))
        output = manager.update_all()
        logger.info(output)
