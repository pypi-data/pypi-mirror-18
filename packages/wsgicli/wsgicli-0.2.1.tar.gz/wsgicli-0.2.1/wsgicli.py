import click
from importlib.machinery import SourceFileLoader
import os
import sys
import time
import threading
import _thread
from wsgiref.simple_server import make_server


#####################################################################################
# Command Line Interface
#####################################################################################
@click.group()
def cli():
    pass


#####################################################################################
# For run server
#####################################################################################
def run_server(app, host, port):
    click.echo('Start: {host}:{port}'.format(host=host, port=port))
    httpd = make_server(host, port, app)
    httpd.serve_forever()


# For reloading server when detected python files changes.
EXIT_STATUS_RELOAD = 3


class FileCheckerThread(threading.Thread):
    # This class is copied and pasted from following source code of Bottle.
    #   https://github.com/bottlepy/bottle/blob/master/bottle.py#L3647-L3686
    """ Interrupt main-thread as soon as a changed module file is detected,
        the lockfile gets deleted or gets too old. """

    def __init__(self, lockfile, interval):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lockfile, self.interval = lockfile, interval
        #: Is one of 'reload', 'error' or 'exit'
        self.status = None

    def run(self):
        files = dict()

        for module in list(sys.modules.values()):
            path = getattr(module, '__file__', '')
            if path[-4:] in ('.pyo', '.pyc'):
                path = path[:-1]
            if path and os.path.exists(path):
                files[path] = os.stat(path).st_mtime

        while not self.status:
            if not os.path.exists(self.lockfile) or \
                    os.stat(self.lockfile).st_mtime < time.time() - self.interval - 5:
                self.status = 'error'
                _thread.interrupt_main()
            for path, last_mtime in files.items():
                if not os.path.exists(path) or os.stat(path).st_mtime > last_mtime:
                    self.status = 'reload'
                    _thread.interrupt_main()
                    break
            time.sleep(self.interval)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, *_):
        if not self.status:
            self.status = 'exit'  # silent exit
        self.join()
        return exc_type is not None and issubclass(exc_type, KeyboardInterrupt)


def run_live_reloading_server(interval, app, host, port):
    if not os.environ.get('WSGICLI_CHILD'):
        import subprocess
        import tempfile
        lockfile = None
        try:
            fd, lockfile = tempfile.mkstemp(prefix='wsgicli.', suffix='.lock')
            os.close(fd)  # We only need this file to exist. We never write to it
            while os.path.exists(lockfile):
                args = [sys.executable] + sys.argv
                environ = os.environ.copy()
                environ['WSGICLI_CHILD'] = 'true'
                environ['WSGICLI_LOCKFILE'] = lockfile
                p = subprocess.Popen(args, env=environ)
                while p.poll() is None:  # Busy wait...
                    os.utime(lockfile, None)  # Alive! If lockfile is unlinked, it raises FileNotFoundError.
                    time.sleep(interval)
                if p.poll() != EXIT_STATUS_RELOAD:
                    if os.path.exists(lockfile):
                        os.unlink(lockfile)
                        sys.exit(p.poll())
        except KeyboardInterrupt:
            pass
        finally:
            if os.path.exists(lockfile):
                os.unlink(lockfile)
        return

    try:
        lockfile = os.environ.get('WSGICLI_LOCKFILE')
        bgcheck = FileCheckerThread(lockfile, interval)
        with bgcheck:
            run_server(app=app, host=host, port=port)
        if bgcheck.status == 'reload':
            sys.exit(EXIT_STATUS_RELOAD)
    except KeyboardInterrupt:
        pass
    except (SystemExit, MemoryError):
        raise
    except:
        time.sleep(interval)
        sys.exit(3)


@cli.command()
@click.argument('filepath', nargs=1)
@click.argument('wsgiapp', nargs=1)
@click.option('--host', '-h', type=click.STRING, default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', type=click.INT, default=8000, help='The port to bind to.')
@click.option('--reload/--no-reload', default=None, help='Enable live reloading')
@click.option('--interval', type=click.INT, default=1,
              help='Interval time to check file changed for reloading')
@click.option('--static/--no-static', default=None, help='Enable static file serving')
@click.option('--static-root', default='static', help='URL path to static files')
@click.option('--static-dirs', default=['./static/'], multiple=True,
              help='Directories for static files')
@click.option('--lineprof/--no-lineprof', help='Enable line profiler')
@click.option('--lineprof-file', multiple=True, help='The filename profiled by line-profiler')
def run(filepath, wsgiapp, host, port, reload, interval,
        static, static_root, static_dirs, lineprof, lineprof_file):
    """
    Runs a development server for WSGI Application.

    Usage:

        $ wsgicli run hello.py app -h 0.0.0.0 -p 5000

        $ wsgicli run hello.py app --reload

        $ wsgicli run hello.py app --static --static-root /static/ --static-dirs ./static/

        $ wsgicli run hello.py app --lineprof
    """
    module = SourceFileLoader('module', filepath).load_module()
    app = getattr(module, wsgiapp)

    if static:
        from wsgi_static_middleware import StaticMiddleware
        app = StaticMiddleware(app, static_root=static_root, static_dirs=static_dirs)

    if lineprof:
        # Caution: wsgi-lineprof is still pre-alpha. Except breaking API Changes.
        from wsgi_lineprof.middleware import LineProfilerMiddleware
        from wsgi_lineprof.filters import FilenameFilter, TotalTimeSorter

        if lineprof_file:
            # Now wsgi-lineprof is now supported only 1 file checking.
            lineprof_file = lineprof_file[0]
        else:
            lineprof_file = filepath.split('/')[-1] if '/' in filepath else filepath
        filters = [FilenameFilter(lineprof_file), TotalTimeSorter()]
        app = LineProfilerMiddleware(app, filters=filters)

    if reload:
        run_live_reloading_server(interval, app=app, host=host, port=port)
    else:
        run_server(app=app, host=host, port=port)


#####################################################################################
# For run shell
#####################################################################################
# Find Models
def import_from_path(import_path):
    abspath = os.path.abspath(import_path)
    if not os.path.exists(abspath):
        raise ValueError('{path} is not a python package.'.format(path=import_path))

    if os.path.isdir(abspath) and os.path.exists(os.path.join(abspath, '__init__.py')):
        name = abspath.split('/')[-1]
        return SourceFileLoader(name, os.path.join(abspath, '__init__.py')).load_module()
    elif abspath.endswith('.py'):
        name = abspath.split('/')[-1].split('.')[0]
        return SourceFileLoader(name, abspath).load_module()
    else:
        raise ValueError('{path} is not a python package.'.format(path=import_path))


def find_modules_from_path(import_path):
    base_module = import_from_path(import_path)
    base_path = getattr(base_module, '__path__', None)

    for module in sys.modules.values():
        path = getattr(module, '__file__', '')
        if path[-4:] in ('.pyo', '.pyc'):
            path = path[:-1]
        if path and os.path.exists(path):
            # Standard libraries are in lib/python3.x/...
            # And third party libraries are in lib/python3.x/site-packages/...
            if 'lib/python' not in path:
                yield module


# Get model base classes
def _sqlalchemy_model():
    from sqlalchemy.ext.declarative import DeclarativeMeta
    return DeclarativeMeta


def _peewee_model():
    from peewee import BaseModel
    return BaseModel


def get_model_base_classes():
    model_base_classes = []
    for x in (_sqlalchemy_model, _peewee_model):
        try:
            model_base = x()
        except ImportError:
            continue
        else:
            model_base_classes.append(model_base)
    return tuple(model_base_classes)


# Run shell
def run_plain(imported_objects):
    import code
    code.interact(local=imported_objects)


def run_ipython(imported_objects):
    # Start IPython >= 1.0
    from IPython import start_ipython
    start_ipython(argv=[], user_ns=imported_objects)


def run_bpython(imported_objects):
    from bpython import embed
    embed(imported_objects)


def run_ptpython(imported_objects, vi_mode=False):
    from ptpython.repl import embed, run_config
    history_filename = os.path.expanduser('~/.ptpython_history')
    embed(globals=imported_objects, history_filename=history_filename,
          vi_mode=vi_mode, configure=run_config)


def run_ptipython(imported_objects, vi_mode=False):
    from ptpython.repl import run_config
    from ptpython.ipython import embed
    history_filename = os.path.expanduser('~/.ptpython_history')
    embed(user_ns=imported_objects, history_filename=history_filename,
          vi_mode=vi_mode, configure=run_config)


interpreters = {
    'python': run_plain,
    'ipython': run_ipython,
    'bpython': run_bpython,
    'ptpython': run_ptpython,
    'ptipython': run_ptipython,
}


def run_python(interpreter, imported_objects):
    for name, _run_python in interpreters.items():
        if interpreter == name:
            _run_python(imported_objects)
    else:
        click.BadParameter('Please select from ' + ', '.join(interpreters.keys()))


@cli.command()
@click.argument('package', nargs=1)
@click.option('-i', '--interpreter', default='python',
              help="Select python interpreters (default: plain)"
              "Supported interpreters are ipython, bpython, ptpython and pyipython.")
@click.option('--models/--no-models', default=True,
              help="Automatically recursively search and import ORM table definition"
                   " from specified package. Now wsgicli supports SQLAlchemy and peewee."
                   " (default: ``--models`` )")
def shell(package, interpreter, models):
    """
    Runs a python shell.

    Usage:

        $ wsgicli shell

        $ wsgicli shell -i ipython (or bpython, ptpython, ptipython)

        $ wsgicli shell --models
    """
    imported_objects = {}
    model_base_classes = get_model_base_classes()

    if models and model_base_classes:
        for module in find_modules_from_path(package):
            for name in dir(module):
                if name.startswith('_'):
                    continue
                obj = getattr(module, name)
                if isinstance(obj, model_base_classes):
                    key = name.split('.')[-1] if '.' in name else name
                    click.secho("{} is imported!".format(name), fg='green')
                    imported_objects[key] = obj
    run_python(interpreter, imported_objects)


if __name__ == '__main__':
    cli()
