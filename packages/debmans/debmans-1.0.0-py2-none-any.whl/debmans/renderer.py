#!/usr/bin/python3
# coding: utf-8

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

import glob
import itertools
import os
import re
import shlex
import shutil
import subprocess
import time

import logging
logger = logging.getLogger(__name__)

import click
from jinja2 import Template
from markdown import markdown
# workaround missing import issue in 0.5
from humanize.time import naturaldelta

from debmans.extractor import PackageExtractor
from debmans.utils import mkdirp


@click.command()
@click.option('-s', '--srcdir', default='.',
              help='where the source manuals are (default: output of the extract command)')
@click.option('-l', '--filelist', type=click.File(),
              help='process files from given list, overrides -m')
@click.option('-f', '--file', type=click.Path(), multiple=True,
              help='process the given file, may be repeated, overrides -m')
@click.pass_obj
def render(obj, srcdir, filelist, file):
    '''render documentation to HTML

    this looks for patterns matching a certain regex in the given
    SRCDIR directory
    '''
    output = obj['output']
    cache = obj['cache']
    mirror = obj['mirror']
    patterns = obj['patterns']

    if not filelist and not file and 'changed_paths' not in obj:
        logging.info('looking for patterns %s in %s', patterns, srcdir)
        filelist = find_files(srcdir, patterns)

    if not filelist:
        filelist = []
    if file:
        filelist = itertools.chain(filelist, file)
    # get modified paths from extractor, if it was also called
    if 'changed_paths' in obj:
        logging.info('received %d paths from extractor', len(obj['changed_paths']))
        filelist = itertools.chain(filelist, obj['changed_paths'])

    if obj['progress']:
        progress = click.progressbar
    else:
        class fake_progress:
            def __init__(self, it, label=None):
                self.it = it

            def __enter__(self):
                return self.it

            def __exit__(self, type, value, traceback):
                pass
        progress = fake_progress
    i = 0
    t = time.time()
    with progress(list(match_jobs(filelist, patterns)),
                  label='rendering manpages') as bar:
        for job in bar:
            dispatch(job, destdir=output, dryrun=obj['dryrun'],
                     cache=cache, prefix=obj['prefix'], mirror=mirror)
            i += 1
    logger.info('rendered %d manpages in %s', i,
                naturaldelta(time.time() - t))


class JinjaRenderer(object):
    '''render Jinja templates using given parameters, caching and
    simulation

    this is basically an extension of the Template class, but extended
    so we can easily pass paths (instead of strings) in and out.

    .. todo:: we should probably have derived Template directly here.
    '''

    def __init__(self, template, cache=True, dryrun=False):
        '''create a renderer

        :param str template: path to the Jinja2 template
        :param bool cache: do not overwrite output file if newer
        :param bool dryrun: do not write anything in any case, useful
                            to test cache detection
        '''
        self.template = template
        self.cache = cache
        self.dryrun = dryrun
        # source file currently processed
        self.source = None

    def generated_time(self):
        '''handy function to add timestamp to footers'''
        return 'Generated on %s' % time.strftime('%Y-%m-%d %H:%M:%S%Z')

    def render(self, output, **data):
        '''render template with given data

        if ``pageinfo`` isn't provided in :attr:`data`, it is set to
        the output of :func:`generated_time`.

        :param str output: path to the output file
        :param dict data: set of parameters passed to Template.render()
        '''
        if 'pageinfo' not in data:
            data['pageinfo'] = self.generated_time()
        if self.uptodate(output):
            logging.debug('%s is up to date with template %s',
                          output, self.template)
        else:
            if self.dryrun:
                logging.debug('dryrun: not writing file %s with template %s',
                              output, self.template)
                return
            mkdirp(os.path.dirname(output))
            logging.debug('writing file %s with template %s',
                          output, self.template)
            with open(self.template, 'r') as templatefile,\
                    open(output, 'w') as outputfile:
                tmpl = Template(templatefile.read().decode('utf-8'))
                outputfile.write(tmpl.render(data).encode('utf-8'))

    def uptodate(self, output):
        '''check if the output file is newer than template

        also checks the :attr:`source` attribute if it is set, which
        allos for subclasses to add a file to check.'''
        return self.cache and os.path.exists(output) \
            and os.stat(self.template).st_mtime <= os.stat(output).st_mtime \
            and (self.source is None
                 or os.stat(self.source).st_mtime <= os.stat(output).st_mtime)


class MarkdownRenderer(JinjaRenderer):
    '''render markdown source files with a jinja template'''
    def render(self, source, output, **data):
        '''render the given source file

        :param str source: path to the Markdown source file
        :param str output: passed to :func:`JinjaRenderer.render`
        '''
        self.source = source
        with open(source, 'r') as sourcefile:
            html = markdown(sourcefile.read())
            super(MarkdownRenderer, self).render(output, content=html, **data)


class CommandRenderer(JinjaRenderer):
    '''a simple template-based rendering system

    a file is passed as an argument to a command and the output is
    written into the given template, in the `{{content}}` Jinja2
    element.

    this is meant to be subclassed in command-specific renderers.

    those can also not even be command-based, as long as they have the
    following parameters:

    - ``pattern``: regular expression pattern for this class

    - ``render(source, target, **data)``: render the given source file
    into the target file, with the attached Jinja data. at least
    ``content`` is expected in there, but ``description`` and
    ``title`` are also encouraged, those should match the template.
    '''
    def __init__(self, template, command=None, cache=True, dryrun=False):
        '''create a renderer with the given command

        :param str command: command to launch for this renderer

        Other parameters passed as is to
        :func:`JinjaRenderer.__init__`
        '''
        if command is not None:
            self.command = command
        super(CommandRenderer, self).__init__(template, cache, dryrun)

    def postprocess(self, data):
        '''modify the data sent to the template after execution

        this allows subclasses to intervene between the command call
        and the render call.

        by default does nothing
        '''
        
    def render(self, source, target, **data):
        '''render the given source file using external command defined in
        constructor

        does not call command in :attr:`dryrun` mode.

        .. todo:: support %(target)s instead of standard output, if
                  necessary?

        :param str source: path to the source file
        :param str target: path to the output file
        :param dict data: remaining arguments passed as is to
                          :func:`JinjaRenderer.render`
        :raises CommandRendererError: if command fails to convert given page

        '''
        # w3m parser requires absolute paths
        self.source = os.path.abspath(source)
        # build a safe command using the shell lexer
        command = [x % {'source': self.source} for x in shlex.split(self.command)]
        if self.uptodate(target):
            logging.debug('%s is up to date, not running %s', target, command)
            return
        if self.dryrun:
            logger.debug('dryrun: not running command %s', command)
            data['content'] = ''
        else:
            logger.debug('running command %s', command)
            try:
                content = subprocess.check_output(command,
                                                  stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                raise CommandRendererError('%s failed to convert %s: %s'
                                           % (self.command, self.source, e))
            data['content'] = content.decode('utf-8', 'replace')
        self.postprocess(data)
        super(CommandRenderer, self).render(target, **data)


class CommandRendererError(RuntimeError):
    '''error raised when man2html fails to render the manpage'''
    pass


class ManpageRenderer(object):
    '''abstract class to store the manpage regex pattern'''

    #: default pattern for manpages
    pattern = r'/(?P<path>man/(?:\w+/)?man[1-9]/.+\.[1-9]\w*(?:\.gz))?$'


class W3mRenderer(CommandRenderer, ManpageRenderer):
    '''render manpages with w3m'''

    #: path to w3m converter
    command = '/usr/lib/w3m/cgi-bin/w3mman2html.cgi "quit=1&local=%(source)s"'

    def postprocess(self, data):
        '''process w3m parser output'''
        content = data['content']
        content = re.sub(r'<a href="file:///[^?]*\?([^(]*)\(([^)]*)\)">',
                         r'<a href="../man\2/\1.\2.html">', content)
        # copy-pasted from Man2htmlRenderer
        content = re.sub(r'^.*<body>', '', content,
                         flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'</body>.*$', '', content,
                         flags=re.DOTALL | re.IGNORECASE)
        # find the page title
        match = re.search(r'^<b>NAME</b>\s*^\s+(.*?)^<b>', content,
                          re.DOTALL | re.MULTILINE)
        if match:
            logger.debug('found page name %s', match.group(1).strip())
            if '-' in match.group(1):
                title, description = match.group(1).split('-')[:2]
                data['title'] = title.strip()
                data['description'] = description.strip()
            else:
                data['title'] = match.group(1).strip()
        # fix broken headings
        content = re.sub(r'\n<b>([^<]*)</b> +<b>', r'<b>\1 ', content)
        # turn section headers into H2
        content = re.sub(r'\n<b>([\w ]+)</b>', r'\n<h2>\1</h2>',
                         content, re.UNICODE)
        data['content'] = content


class Man2htmlRenderer(CommandRenderer, ManpageRenderer):
    '''render manpages with man2html'''
    command = 'man2html %(source)s'

    def postprocess(self, data):
        '''process man2html output

        - it doesn't return proper exit codes, look for Status header
          instead. Anything 40X is bad.
        - the title is in the ``NAME`` level two header (``<h2>``)
        - keep only the inside of the ``<body>`` tag
        - rewrite URLs to point to the right place
        - remove attribution
        '''
        content = data['content']
        if content.startswith('Status: 40'):
            e = re.sub(r'^.*<title>(.*)</title>.*$', r'\1',
                       content, re.DOTALL | re.IGNORECASE)
            raise CommandRendererError('%s failed to convert %s: %s'
                                       % (self.command, self.source, e))
        match = re.search(r'<h2>\w*NAME\w*</h2>\w*([^<]*)<', content,
                          re.DOTALL | re.IGNORECASE)
        if match:
            logger.debug('found page name %s', match.group(1))
            if '-' in match.group(1):
                title, description = match.group(1).split('-')[:2]
                data['title'] = title.strip()
                data['description'] = description.strip()
            else:
                data['title'] = match.group(1).strip()
        content = re.sub(r'^.*<body>', '', content,
                         flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'</body>.*$', '', content,
                         flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'/cgi-bin/man/man2html\?([1-9])\+(\w+)',
                         r'/man/man\1/\2.\1.html', content)
        content = re.sub(r'<HR>\s+This document was created by\s+<A HREF="/cgi-bin/man/man2html">.*$',
                         '', content, flags=re.IGNORECASE | re.DOTALL)
        data['content'] = content
        return data


#: quick switch to toggle default manpage rendering implementation
DefaultManpageRenderer = W3mRenderer


def find_files(directory, patterns):
    '''look for file paterns in the given directory and return the right
    command to run

    .. todo:: this may be slow in large directories and may be
              reimplemented with :func:`scandir` if we ever depend on
              Python 3.5 or later.

    .. todo:: doesn't look at patterns at all?!

    '''
    for root, dirs, files in os.walk(directory):
        logging.debug('walking: %s %s %s', root, dirs, files)
        for path in files:
            yield os.path.join(root, path)


def match_jobs(files, patterns):
    '''dispatch the right command for the matching pattern

    :param list files: list of file paths to inspect
    :param list patterns: list of tuples (``cls``,
                          ``regex``). ``regex`` is a compiled regex
                          patterns to match against the pathnames,
                          ``cls`` is a CommandRenderer subclass to run
    :return: ``command``, ``path`` tuples
    :rtype: list
    '''
    for path in files:
        for regex, module in patterns.iteritems():
            if re.search(regex, path):
                yield module, path


def dispatch(job, destdir, dryrun=False, cache=True, prefix=None, mirror=None):
    '''process a specific job and call the correct renderer

    .. todo:: fix suite detection here?
    '''
    renderer, file = job
    # should match debmans.PackageExtractor.pattern_manpages
    # XXX: total hack: [^/]* is the suite here
    htmlfile = re.sub(r'^.*/([^/]*/man/(?:\w+/)?man[1-9]/.+\.[1-9]\w*)(?:\.gz)?$', r'\1.html', file)
    htmlfile = os.path.join(destdir, htmlfile)
    try:
        renderer.render(file, htmlfile, prefix=prefix, suites=mirror.releases)
    except CommandRendererError as e:
        logging.warn('%s failed to convert %s: %s', renderer, file, e)


@click.command()
@click.pass_obj
def site(obj):
    '''render the whole static site'''
    suites = obj['mirror'].releases
    pattern = os.path.join(obj['theme'], '*.mdwn')
    template = os.path.join(obj['theme'], 'template.html')
    logging.info('rendering files in %s with template %s',
                 pattern, template)
    i = 0
    t = time.time()
    for path in glob.glob(pattern):
        output = re.sub(r'.mdwn$', '.html', path)
        output = os.path.join(obj['output'], os.path.basename(output))
        r = MarkdownRenderer(template, dryrun=obj['dryrun'],
                             cache=obj['cache'])
        r.render(path, output, prefix=obj['prefix'], suites=suites)
        i += 1
    logging.info('rendererd %d files in %s', i,
                 naturaldelta(time.time() - t))
    logging.info('copying files')
    i = 0
    t = time.time()
    for pattern in '*.css', '*.js':
        for static in glob.glob(os.path.join(obj['theme'], pattern)):
            i += 1
            logging.debug('copying %s to %s', static, obj['output'])
            shutil.copy(static, obj['output'])
    picsdir = os.path.join(obj['theme'], 'Pics')
    pics = os.path.join(picsdir, '*')
    targetdir = os.path.join(obj['output'], 'Pics')
    mkdirp(targetdir)
    logging.debug('copying pics %s', pics)
    for static in glob.glob(pics):
        i += 1
        logging.debug('copying %s to %s', static, targetdir)
        shutil.copy(static, targetdir)
    logging.info('rendererd %d files in %s', i,
                 naturaldelta(time.time() - t))
