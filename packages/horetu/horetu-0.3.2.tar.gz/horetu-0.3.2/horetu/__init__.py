import os
import sys
import logging
from functools import partial, wraps
from collections import namedtuple

# Begin exports.
from . import input, output, render, exceptions
from . import templates, lib, config
from .util import config_template, CallableDict
from .signature import COUNT
from .exceptions import Error

logger = logging.getLogger(__name__)

def Interface(function, config_file, config_sep, i):
    '''
    :param i: Function that takes no arguments and returns an input.Input
    '''
    try:
        body = output.Output(config_file, config_sep, function, i())
    except exceptions.HoretuException as e:
        body = e
    return body

WebResponse = namedtuple('WebResponse', ['content_type', 'data'])
def content_type(x):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return WebResponse(x, func(*args, **kwargs))
        return wrapper
    return decorator

def wsgi(function,
         name=None, config_file=None, config_sep=None,
         default_content_type='text/plain; charset=UTF-8', debug=False):
    '''
    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config_file: str or None
    :param config_file: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    :param str name: Name of the program, used for environment variable settings
        If it is ``None`` (the default), we attempt to get the name from the function.
    :param str default_content_type: Content-Type with which pages should be served
    :param bool debug: Print errors and debugging information to web pages?
    :rtype: function
    :returns: WSGI application
    '''
    import traceback
    try:
        from webob import Response
    except ImportError:
        logger.error('WebOb is not installed; run this: pip install horetu[all]')
        sys.exit(1)

    def app(environ, start_response):
        res = Response()
        i = partial(input.wsgi, function, environ)
        try:
            out = Interface(config_file, config_sep, function, i)
        except Exception:
            if debug:
                res.content_type = 'text/plain; charset=UTF-8'
                body = [traceback.format_exception().encode('utf-8')]
            else:
                raise

        if isinstance(out, exceptions.HoretuCouldNotParse):
            res.status = 404
            wr = WebResponse('text/html',
                    templates.AppIter(render.wsgi.usage(function, out)))
        elif isinstance(out, exceptions.HoretuShowHelp):
            res.status = 200
            wr = WebResponse('text/html',
                    templates.AppIter(render.wsgi.man(function, out)))
        elif isinstance(out, exceptions.HoretuError):
            res.status = 400
            if isinstance(out, WebResponse):
                wr = out
            else:
                wr = WebResponse(default_content_type, out)
        else:
            res.status = 200
            if isinstance(out, WebResponse):
                wr = out
            else:
                wr = WebResponse(default_content_type, out)

        if wr.content_type.lower().startswith('text/plain'):
            res.app_iter = (chunk + b'\n' for chunk in wr.data)
        else:
            res.app_iter = wr.data
        res.content_type = wr.content_type
        return res(environ, start_response)
    return app

def default_config(function, fp=sys.stdout, config_sep=None):
    config.write(lib.Program(function), fp, config_sep)

def cli(function, argv=sys.argv, return_=False,
        name=None, config_file=None, config_sep=None,
        exit_=sys.exit,
        stdout=sys.stdout.buffer, stderr=sys.stderr.buffer):
    '''
    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config_file: str or None
    :param config_file: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    :param str name: Name of the program (``$0``), for usage text and
        environment variables. If it is ``None`` (the default), we
        use the following instead.
       
        1. If a function, rather than a list or dictionary, is passed as ``f``,
           use the function's name (``f.__name__``).
        2. Otherwise, use the first argv (``sys.argv[0]``).
    :param list argv: :py:obj:`sys.argv` by default
    :param bool return_: If this is ``True``, simply return the result of the function;
        do not write stuff to ``exit_``, ``stdout``, or ``stderr``.
    :param function exit_: :py:func:`sys.exit` by default
    :type stdout: Binary file
    :param stdout: :py:func:`sys.stdout.buffer` by default
    :type stderr: Binary file
    :param stderr: :py:func:`sys.stderr.buffer` by default
    '''
    argv = list(argv) # Prevent myself from modifying the input.

    if name is None:
        if hasattr(function, '__call__'):
            name = function.__name__
        else:
            name = os.path.basename(argv[0])

    try:
        out = Interface(function, config_file, config_sep,           # pass through
                        partial(input.cli, function, argv[1:])) # input
    except exceptions.Error as e:
        out = e

    code = 0
    fp = stdout
    if isinstance(out, exceptions.HoretuException):
        if not out.ok:
            fp = stderr

        if isinstance(out, exceptions.HoretuShowHelp):
            app_iter = templates.AppIter(render.cli.man(name, function, out))
        else:
            if isinstance(out, exceptions.HoretuCouldNotParse):
                code = 2
            else:
                code = 1
            app_iter = templates.AppIter(render.cli.usage(name, function, out))
    else:
        app_iter = out
    _communicate_cli(stdout, stderr, fp, app_iter)
    exit_(code)

def _communicate_cli(stdout, stderr, fp, app_iter):
    try:
        for line in app_iter:
            fp.write(line + b'\n')
    except BrokenPipeError:
        stderr.close()
    except exceptions.Error as e:
        stdout.write(e.message.rstrip('\n').encode('utf-8') + b'\n')

def django(function):
    try:
        from django.core.management.base import BaseCommand, CommandError
    except ImportError:
        logger.error('Django is not installed; run this: pip install horetu[all]')
        sys.exit(1)
    class Command(BaseCommand):
        def add_arguments(self, parser):
            render.argparse.update_parser(function, parser)
        def handle(self, *args, **options):
            fp = self.stdout
            try:
                y = render.argparse.evaluate(function, args, options)
            except Exception as e:
                raise CommandError(str(e))
            else:
                _communicate_cli(self.stdout, self.stderr, fp.buffer,
                                 templates.AppIter(y))
    return Command

@wraps(cli)
def horetu(*args, **kwargs):
    logger.warn('The horetu.horetu interface is deprecated; use horetu.cli.')

    if 'description' in kwargs:
        del(kwargs['description'])

    if 'args' in kwargs:
        kwargs['argv'] = sys.argv[:1] + kwargs.pop('args')

    return cli(*args, **kwargs)

def irc(function, config=None, config_sep=' ',
        ):
    '''
    Render Python functions as an IRC bot.

    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config: str or None
    :param config: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    '''
    raise NotImplementedError

def webcli(function, config=None, config_sep=' '):
    '''
    Render Python functions as text terminal website.

    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config: str or None
    :param config: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    '''
    raise NotImplementedError
