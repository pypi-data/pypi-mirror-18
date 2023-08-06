#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CrossPM (Cross Package Manager) version: {version} The MIT License (MIT)

Usage:
    crosspm download [options]
    crosspm promote [options]       * Temporarily off
    crosspm pack <OUT> <SOURCE> [options]
    crosspm cache [size | age | clear [hard]]
    crosspm -h | --help
    crosspm --version

Options:
    <OUT>                           Output file.
    <SOURCE>                        Source directory path.
    -h, --help                      Show this screen.
    --version                       Show version.
    -L, --list                      Do not load packages and its dependencies. Just show what's found.
    -v LEVEL, --verbose=LEVEL       Set output verbosity: ({verb_level}) [default: ].
    -l LOGFILE, --log=LOGFILE       File name for log output. Log level is '{log_default}' if set when verbose doesn't.
    -c=FILE, --config=FILE          Path to configuration file.
    -o OPTIONS, --options OPTIONS   Extra options.
    --depslock-path=FILE            Path to file with locked dependencies [./{deps_lock_default}]
    --out-format=TYPE               Output data format. Available formats:({out_format}) [default: {out_format_default}]
    --output=FILE                   Output file name (required if --out_format is not stdout)
    --out-prefix=PREFIX             Prefix for output variable name [default: ] (no prefix at all)
    --no-fails                      Ignore fails config if possible.

"""

import logging
from docopt import docopt
import os
from crosspm import config
from crosspm.helpers.archive import Archive
from crosspm.helpers.config import (
    CROSSPM_DEPENDENCY_LOCK_FILENAME,
    Config,
)
from crosspm.helpers.downloader import Downloader
# from crosspm.helpers.promoter import Promoter
from crosspm.helpers.output import Output
from crosspm.helpers.exceptions import *


# TODO: Upgrade exceptions handling
class CrossPM(object):
    _config = None
    _args = None
    _output = Output()

    def __init__(self, args=None):
        self._log = logging.getLogger('crosspm')
        self._args = docopt(__doc__.format(version=config.__version__,
                                           verb_level=Config.get_verbosity_level(),
                                           log_default=Config.get_verbosity_level(0, True),
                                           deps_lock_default=CROSSPM_DEPENDENCY_LOCK_FILENAME,
                                           out_format=self._output.get_output_types(),
                                           out_format_default='stdout',
                                           ),
                            argv=args,
                            version=config.__version__,)

        if type(self._args) is str:
            print(self._args)
            exit()

    def read_config(self):
        self._config = Config(self._args['--config'], self._args['--options'], self._args['--no-fails'])

    def run(self):
        self.do_run(self.check_common_args)
        self.do_run(self.read_config)

        if self._args['download']:
            self.do_run(self.download)
            # self.download()

        elif self._args['promote']:
            self.do_run(self.promote)

        elif self._args['pack']:
            self.do_run(self.pack)

        elif self._args['cache']:
            self.do_run(self.cache)

    def do_run(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except CrosspmExceptionWrongArgs as e:
            print(__doc__)
            self._log.critical(e.msg)
            sys.exit(e.error_code)

        except CrosspmException as e:
            print_stdout('')
            self._log.critical(e.msg)
            sys.exit(e.error_code)

        except Exception as e:
            print_stdout('')
            self._log.exception(e)
            self._log.critical('Unknown error occurred!')
            sys.exit(CROSSPM_ERRORCODE_UNKNOWN_ERROR)

    def check_common_args(self):
        if self._args['--output']:
            output = self._args['--output'].strip().strip("'").strip('"')
            output_abs = os.path.abspath(output)
            if os.path.isdir(output_abs):
                raise CrosspmExceptionWrongArgs(
                    '"%s" is a directory - can\'t write to it'
                )
            self._args['--output'] = output

        self.set_logging_level()

    def set_logging_level(self):
        level_str = self._args['--verbose'].strip().lower()

        log = self._args['--log']
        if log:
            log = log.strip().strip("'").strip('"')
            log_abs = os.path.abspath(log)
            if os.path.isdir(log_abs):
                raise CrosspmExceptionWrongArgs(
                    '"%s" is a directory - can\'t write log to it'
                )
            else:
                log_dir = os.path.dirname(log_abs)
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
        else:
            log_abs = None

        level = Config.get_verbosity_level(level_str or 'console')
        if level or log_abs:
            self._log.setLevel(level)
            format_str = '%(asctime)-19s [%(levelname)-9s] %(message)s'
            if level_str == 'debug':
                format_str = '%(asctime)-19s [%(levelname)-9s] %(name)-12s: %(message)s'
            formatter = logging.Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

            if level:
                sh = logging.StreamHandler(stream=sys.stderr)
                sh.setLevel(level)
                # sh.setFormatter(formatter)
                self._log.addHandler(sh)

            if log_abs:
                if not level_str:
                    level = Config.get_verbosity_level(0)
                fh = logging.FileHandler(filename=log_abs)
                fh.setLevel(level)
                fh.setFormatter(formatter)
                self._log.addHandler(fh)

    def download(self):
        if self._args['--out-format'] == 'stdout':
            if self._args['--output']:
                raise CrosspmExceptionWrongArgs(
                    "unwanted argument '--output' while argument '--out-format={}'".format(
                        self._args['--out-format'],
                    ))
        elif not self._args['--output']:
            raise CrosspmExceptionWrongArgs(
                "argument '--output' required when argument '--out-format={}'".format(
                    self._args['--out-format'],
                ))

        params = {
            'out_format': ['--out-format', ''],
            'output': ['--output', ''],
            'out_prefix': ['--out-prefix', ''],
            'depslock_path': ['--depslock-path', ''],
        }

        for k, v in params.items():
            params[k] = self._args[v[0]] if v[0] in self._args else v[1]

        do_load = not self._args['--list']
        if do_load:
            self._config.cache.auto_clear()
        cpm_downloader = Downloader(self._config, params.pop('depslock_path'), do_load)
        packages = cpm_downloader.download_packages()

        _not_found = any(_pkg is None for _pkg in packages.values())
        if _not_found:
            raise CrosspmException(
                CROSSPM_ERRORCODE_PACKAGE_NOT_FOUND,
                'Some package(s) not found.'
            )
        if do_load:
            self._output.write(params, packages)

    def promote(self):
        self._log.warning('This option is temporarily off.')
        # cpm_promoter = Promoter(self._config)
        # cpm_promoter.promote_packages()

    def pack(self):
        Archive.create(self._args['<OUT>'], self._args['<SOURCE>'])

    def cache(self):
        if self._args['clear']:
            self._config.cache.clear(self._args['hard'])
        elif self._args['size']:
            self._config.cache.size()
        elif self._args['age']:
            self._config.cache.age()
        else:
            self._config.cache.info()


if __name__ == '__main__':
    app = CrossPM()
    app.run()
