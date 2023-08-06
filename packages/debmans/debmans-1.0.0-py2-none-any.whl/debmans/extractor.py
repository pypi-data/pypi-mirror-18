#!/usr/bin/python3
# coding: utf-8
#
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

from __future__ import division, absolute_import
from __future__ import print_function

from contextlib import contextmanager
import bz2
import errno
import gzip
import lzma
import os.path
import re
import time

import apt.debfile
from debian import deb822
import click
# workaround missing import issue in 0.5
from humanize.time import naturaldelta

import logging
logger = logging.getLogger(__name__)

from debmans.utils import mkdirp

# supported compression formats for Sources files. Order does matter: formats
# appearing early in the list will be preferred to those appearing later
SOURCES_COMP_FMTS = ['gz', 'xz']


class PackageExtractor(object):
    '''extract certain files from debian packages'''

    patterns = []

    def __init__(self, regex=[], root='.', destdir=None, dryrun=False):
        '''setup extractor and caching

        patterns may have a named subgroup called ``path`` to extract
        only parts of the path

        :param list regex: patterns to add to the existing patterns list
        :param str root: directory where to find packages
        :param str destdir: where to store the extract pages
        :param bool dryrun: if True, do not actually write packages'''
        # this takes one second to load, swallow the cost now instead of
        # for every package
        self.apt_cache = apt.Cache()
        self.files = []
        self.root = root
        self.destdir = destdir
        self.dryrun = dryrun
        self._regexes = None
        self.patterns += regex

    @property
    def regexes(self):
        '''compiled static cache of regex patterns

        to regenerate this when patterns is changed, set
        :attr:`_regexes` to None.
        '''
        if self._regexes is None:
            self._regexes = [re.compile(pattern) for pattern in self.patterns]
        return self._regexes

    def write_file(self, item, data):
        '''callback to actually write files in archive

        this will check for the internal regex list and write the
        given file in :attr:`PackageExtractor.destdir`, creating missing
        directories as needed.

        only the part that is matching the pattern is extracted,
        unless the pattern features a ``path`` group, in which case
        only *that* part is then extracted.
        '''

        for regex in self.regexes:
            m = regex.search(item.name)
            if m and item.isfile():
                break
        else:
            return
        if 'path' in regex.groupindex:
            filename = os.path.join(self.destdir, m.group('path'))
        else:
            filename = os.path.join(self.destdir, m.group())
        if not self.dryrun:
            mkdirp(os.path.dirname(filename))
        logger.debug('writing file %s', filename)
        if not self.dryrun:
            with open(filename, 'wb') as extracted_file:
                extracted_file.write(data)
        self.files.append(filename)

    def extract(self, pkg, destdir=None, cache=True):
        '''extract matching patterns into destdir

        :param debian.deb822.Deb822 pkg: a package dictionnary with
                                         fields like Filename, Package
                                         and Version at least.
        :param destdir: where to store the extracted files
        :type destdir: str or None to default to the path given in constructor
        :param bool cache: if we should check and create the cache file 
                           (a PackageCacheFile)
        :return: extracted files paths
        :rtype: list

        :raises PackageCorruptedError: if apt fails to extract the file

        '''
        if destdir is not None:
            self.destdir = destdir
        if self.destdir is None:
            raise AttributeError('no destdir provided')
        cachefile = PackageCacheFile(self.destdir, pkg)
        if cache and cachefile.exists():
            logger.debug('skipped package %s because cache present in %s',
                         pkg.get('Package'), cachefile.filename)
            return self.files

        path = os.path.join(self.root, pkg.get('Filename'))

        deb = apt.debfile.DebPackage(path, self.apt_cache)
        checksums = deb.control_content('md5sums')
        # some packages do not have checksums at all
        if checksums:
            logging.debug('found md5sums file')
            for regex in self.regexes:
                if regex.search(checksums):
                    break
            else:
                # no manpage found in control file, don't extract
                if cache:
                    cachefile.create()
                return self.files
        else:
            logging.debug('no md5sums file found')

        try:
            deb._debfile.data.go(self.write_file)
        except SystemError:
            raise PackageCorruptedError('could not read package %s' % path)
        if cache:
            cachefile.create()
        return self.files


@click.command()
@click.option('-f', '--file', 'debfile',
              help='process only a single Debian package file',
              type=click.Path(exists=True, file_okay=True, readable=True))
@click.pass_obj
def extract(obj, debfile):
    '''extract manpages from Debian binary packages in mirror

    iterate over all binary packages found in the mirror, and
    extract each included manpage to the OUTPUT directory. the
    directory is created if missing.
    '''
    mirror = obj['mirror']
    output = obj['output']
    cache = obj['cache']
    regex = obj['patterns'].keys()

    extractor = PackageExtractor(regex, root=mirror.path, dryrun=obj['dryrun'])
    logger.info('extracting files matching patterns: %s in mirror %s',
                extractor.patterns, mirror.path)
    if debfile:
        name, version, _ = os.path.basename(debfile).split('_')
        fake_pkg = {'Filename': debfile,
                    'Package': name,
                    'Version': version,
                    }
        package_list = [('unstable', fake_pkg)]
    else:
        package_list = mirror.packages
    if obj['progress']:
        progress = click.progressbar
    else:
        @contextmanager
        def no_progress(iterator, *args, **kwargs):
            yield iterator
        progress = no_progress
    i = 0
    suites = set()
    t = time.time()
    with progress(package_list, label='extracting packages') as bar:
        for suite, pkg in bar:
            suites.add(suite)
            i += 1
            logger.debug("found package %s-%s",
                         pkg.get('Package'), pkg.get('Version'))
            suite_output = os.path.join(output, suite)
            extractor.extract(pkg, destdir=suite_output, cache=cache)
    logging.info('extracted %d files out of %d packages in %s',
                 i, len(extractor.files), naturaldelta(time.time() - t))
    # for render if also called
    obj['changed_paths'] = extractor.files
    obj['suites'] = suites


class PackageCacheFile(object):
    '''a cache file to see if we have inspected a package before

    this creates an empty named pkgname-version in the given destdir
    on create. there are also facilities to check existence.

    it is assumed that if there is no version change, no change is
    required in the man pages as well.

    it is not possible to atomically check existence just yet.

    this will leave stray cache files behind.
    '''
    dirs = set()

    def __init__(self, destdir, pkg):
        self.destdir = destdir
        self.pkg = pkg

    @property
    def filename(self):
        '''the full path to the cache file'''
        pkg_id = (self.pkg.get('Package'), self.pkg.get('Version'))
        return os.path.join(self.destdir, '.cache', '%s-%s' % pkg_id)

    def exists(self):
        '''if the cache file exists'''
        return os.path.exists(self.filename)

    def create(self):
        '''create the cache file with the given field as content'''
        if self.destdir not in self.dirs:
            mkdirp(os.path.join(self.destdir, '.cache'))
            self.dirs.add(self.destdir)
        open(self.filename, 'w').close()


class PackageMirror(object):
    '''inspect a Debian mirror for binary packages
   
    this is a modified replica of debsources's SourceMirror
    class. Ideally, this would be merged back into the original class
    as a derivative.
    '''

    def __init__(self, path):
        '''create a mirror object.

        :param str path: path to the root of the repository
        '''
        self.path = os.path.realpath(path)
        self._packages = None
        self._releases = None
        self._dists_dir = os.path.join(self.path, 'dists')
        # work with ad-hoc repositories, mostly for tests
        if not os.path.exists(self._dists_dir):
            self._dists_dir = self.path

    @property
    def packages(self):
        """return the mirror packages as a set of <package, version> pairs

        .. note: This is just like calling :func:`ls`, except there is
                 a cache to avoid calling it multiple times.
        """
        if self._packages is None:
            self._packages = list(self.ls())
        return self._packages

    @property
    def releases(self):
        '''list of releases in this repository

        :returns: (codename -> description) mappings. description is
                  in the format ``X.Y codename (stable)``, unless no
                  matching Release file was found, in which case it
                  can be just ``codename``, which is taken from the
                  :func:`packages` list of suites.

        :rtype: dict

        '''
        if self._releases is None:
            self.__find_releases()
        return self._releases

    def __find_releases(self):
        self._releases = {}
        # first extract codenames from hackish packages parser
        for rel, pkg in dict([(x, x) for x, y in self.packages]).iteritems():
            if rel not in self._releases:
                self._releases[rel] = None
        for root, dirs, files in os.walk(self._dists_dir):
            relfiles = set([os.path.join(root, os.path.splitext(file)[0])
                            for file in files
                            if os.path.splitext(file)[0] == 'Release'])
            for path in relfiles:
                with open(path, 'r') as relfile:
                    p = list(deb822.Packages.iter_paragraphs(sequence=relfile))[0]
                    if p.get('Codename') \
                       and (p.get('Codename') not in self._releases \
                       or self._releases[p.get('Codename')] is None):
                        self._releases[p.get('Codename')] = "%s %s (%s)" \
                                                            % (p.get('Version'),
                                                               p.get('Codename'),
                                                               p.get('Suite'))
        for rel, val in self._releases.iteritems():
            if val is None:
                logging.info('suite %s was not found in any Release file', rel)
                self._releases[rel] = rel

    def __find_packages_files(self, arch=None, suite=None):
        def choose_comp(base):
            """pick the preferred compressed variant of a given Sources file"""
            variants = [base + '.' + fmt
                        for fmt in SOURCES_COMP_FMTS
                        if os.path.exists(base + '.' + fmt)]
            # uncompressed variant
            variants.insert(0, base)
            if not variants:
                raise DebmirrorError('no supported compressed variants of '
                                     'Sources file: ' + base)
            else:
                return variants[0]

        for root, dirs, files in os.walk(self._dists_dir):
            src_bases = set([os.path.join(root, os.path.splitext(file)[0])
                             for file in files
                             if os.path.splitext(file)[0] == 'Packages'])
            src_indexes = [choose_comp(b) for b in src_bases]
            for f in src_indexes:
                steps = f.split('/')
                try:
                    suite = steps[-4]  # wheezy, jessie, sid, ...
                except IndexError:
                    logging.warning('non-standard repository layout, suite unknown')
                    suite = 'unknown'
                yield suite, f

    def ls(self):
        '''iterate over packages found in the mirror

        this will yield ``(suite, pkg)`` pairs. the ``suite`` is
        determined by looking at the name of the 4th directory up from
        where the Packages file is located, as is standard in complete
        apt repositories. this may yield weird codenames when working
        with ad-hoc repositories as the chosen name may be a bit
        random depending on your directory structure.

        :return: ``(suite, pkg)`` tuples for each package found.
        :rtype: ``pkg`` is a deb822 fragment, ``suite`` is a string.
        '''
        for suite, filename in self.__find_packages_files():
            if filename.endswith('.gz'):
                zopen = gzip.open
            elif filename.endswith('.bz2'):
                zopen = bz2.BZ2File
            elif filename.endswith('.xz'):
                zopen = lzma.open
            else:
                zopen = open
            try:
                pkgs_path = os.path.join(self.path, filename)
                with zopen(pkgs_path) as pkgs_file:
                    logger.debug('inspecting file %s', pkgs_path)
                    for pkg in deb822.Packages.iter_paragraphs(sequence=pkgs_file):
                        pkg_id = (pkg.get('Package'), pkg.get('Version'))
                        logger.debug('found package %s', pkg_id)
                        yield suite, pkg
            except IOError as e:
                if e.errno != errno.ENOENT:
                    raise


class DebmirrorError(RuntimeError):
    """runtime error when using a local Debian mirror"""
    pass


class PackageCorruptedError(RuntimeError):
    """runtime error when using a local Debian mirror"""
    pass
