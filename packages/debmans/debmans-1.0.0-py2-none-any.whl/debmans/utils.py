# coding: utf-8
'''various utilities for debmans'''
# Copyright (C) 2016 Antoine Beaupré <anarcat@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import errno
import inspect
import os.path
import pkg_resources


import logging
logger = logging.getLogger(__name__)


def find_parent_module():
    """find the name of a the first module calling this module

    if we cannot find it, we return the current module's name
    (__name__) instead.
    """
    try:
        frame = inspect.currentframe().f_back
        module = inspect.getmodule(frame)
        while module is None or module.__name__ == __name__:
            frame = frame.f_back
            module = inspect.getmodule(frame)
        return module.__name__
    except AttributeError:
        # somehow we failed to find our module
        # return the logger module name by default
        return __name__


def find_static_file(path):
    '''locate a file in the distribution

    this will look in the shipped files in the package

    this assumes the files are at the root of the package or the
    source tree (if not packaged)

    this does not check if the file actually exists.

    :param str path: path for the file, relative to the source tree root
    :return: the absolute path to the file
    '''
    try:
        pkg = pkg_resources.Requirement.parse("debmans")
        filename = pkg_resources.resource_filename(pkg, os.path.join('debmans', path))
    except pkg_resources.DistributionNotFound:
        filename = os.path.join(os.path.dirname(__file__), path)
    return os.path.realpath(filename)


def mkdirp(path):
    '''make directories without error

    this is a simple wrapper around :func:`os.makedirs` to avoid
    failing if the directory already exists.

    it also logs to the ``DEBUG`` :mod:`logging` facility when a
    directory is created.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    else:
        logger.debug('created directory %s', path)
