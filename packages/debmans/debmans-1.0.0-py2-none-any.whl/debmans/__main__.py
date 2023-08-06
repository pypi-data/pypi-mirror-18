# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
log = logging.getLogger(__name__)
try:
    import http.server as http
    import socketserver
except ImportError:
    import SimpleHTTPServer as http
    import SocketServer as socketserver
import os

import click

from debmans import version
from debmans.logger import setup_logging, levels
from debmans.utils import find_static_file
from debmans.extractor import extract, PackageMirror
from debmans.renderer import render, site


@click.group(chain=True)
@click.version_option(version=version)
# coied over from extractor, should probably be factored into parent
# command but i'm too lazy to learn contexts, and i still want this to
# work standalone
@click.option('--loglevel', 'loglevel',
              help='show only warning messages',
              type=click.Choice(levels),
              flag_value='WARNING', default=True)
@click.option('-v', '--verbose', 'loglevel', help='be more verbose',
              flag_value='INFO')
@click.option('-d', '--debug', 'loglevel', help='even more verbose',
              flag_value='DEBUG')
# would love to have a default here when no option is specified
# unfortunately, default= still asks for an argument
@click.option('-s', '--syslog', type=click.Choice(levels),
              help='send logs to syslog')
@click.option('-n', '--dryrun', is_flag=True,
              help='do not write anything')
@click.option('--progress', is_flag=True,
              help='show progress bars')
@click.option('--profile', is_flag=True,
              help="enable Python's profiler (cProfile)")
@click.option('-o', '--output', default='.', show_default=True,
              help='directory where to store files',
              type=click.Path(dir_okay=True, writable=True))
@click.option('-m', '--mirror', default='.', show_default=True,
              help='Debian mirror to inspect for binary packages',
              type=click.Path(exists=True, dir_okay=True, readable=True))
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='keep existing file if newer')
@click.option('--prefix', default='/', show_default=True,
              help='prefix to prepend to internal URLs')
@click.option('-t', '--theme', default=find_static_file('static'),
              show_default=True)
@click.option('-p', '--plugin', multiple=True, show_default=True,
              default=['debmans.renderer.DefaultManpageRenderer'],
              help='rendering plugins to load')
@click.pass_context
def debmans(ctx, loglevel, syslog, dryrun, plugin, theme,
            progress, profile, output, mirror, cache, prefix):
    '''Extract and render manuals from Debian packages'''
    setup_logging(level=loglevel, syslog=syslog)
    # not in parent command because i can't figure out how to disable
    # and collect stats when command completes
    if profile:
        import cProfile
        import pstats
        try:
            import StringIO as io
        except ImportError:
            import io
        pr = cProfile.Profile()
        pr.enable()
        logging.info('profiler enabled')

        @debmans.resultcallback()
        def profiler_stop(*args, **kwargs):
            pr.disable()
            s = io.StringIO()
            sortby = 'time'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            logging.info("profiler results:\n%s", s.getvalue())

    ctx.obj['dryrun'] = dryrun
    ctx.obj['patterns'] = {}
    ctx.obj['theme'] = theme
    template = os.path.join(theme, 'template.html')
    for command in plugin:
        logging.debug('looking for module %s', command)
        try:
            # last component should be a "from", normally a subclass
            # of CommandRenderer or something that looks like it
            module, cls = command.rsplit('.', 1)
            _temp = __import__(module, globals(), locals(), [cls], 0)
            renderer = getattr(_temp, cls)(template,
                                           cache=cache, dryrun=dryrun)
            ctx.obj['patterns'][renderer.pattern] = renderer
            log.debug('hooked renderer %s on pattern %s',
                      renderer, renderer.pattern)
        except (ImportError, ValueError) as e:
            log.error('module %s not found, aborting', command)
            ctx.exit(1)

    ctx.obj['progress'] = progress
    ctx.obj['output'] = output
    # break convention to (ab?)use cache
    ctx.obj['mirror'] = PackageMirror(mirror)
    ctx.obj['cache'] = cache
    ctx.obj['prefix'] = prefix

debmans.add_command(extract)
debmans.add_command(render)
debmans.add_command(site)


@click.command()
@click.option('-p', '--port', default=8000, show_default=True,
              help='port to start the server on')
@click.pass_obj
def serve(obj, port):
    '''convenience call for SimpleHTTPServer'''
    output = obj['output']
    os.chdir(output)
    handler = http.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    host, port = httpd.socket.getsockname()
    log.info('Serving %s over HTTP on %s port %d...', output, host, port)
    httpd.serve_forever()
debmans.add_command(serve)


def main():
    '''workaround a click quirk

    click seems to require a dict to be passed for pass_context to
    work correctly.

    this is so that setuptools works correctly.
    '''
    return debmans(obj={})

if __name__ == '__main__':
    main()
