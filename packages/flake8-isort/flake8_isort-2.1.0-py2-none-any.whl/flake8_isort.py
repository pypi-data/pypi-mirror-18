# -*- coding: utf-8 -*-
from difflib import Differ
from flake8_polyfill import stdin
from isort import SortImports
from testfixtures import OutputCapture

import os
import pycodestyle


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


stdin.monkey_patch('pycodestyle')


class Flake8Isort(object):
    name = 'flake8_isort'
    version = '2.1.0'
    isort_unsorted = (
        'I001 isort found an import in the wrong position'
    )
    no_config_msg = (
        'I002 no configuration found (.isort.cfg or [isort] on setup.cfg)'
    )
    isort_blank_req = (
        'I003 isort expected 1 blank line in imports, found 0'
    )
    isort_blank_unexp = (
        'I004 isort found an unexpected blank line in imports'
    )

    config_file = None

    def __init__(self, tree, filename):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--no-isort-config',
            action='store_true',
            parse_from_config=True,
            help='Do not require explicit configuration to be found'
        )

    @classmethod
    def parse_options(cls, options):
        if options.no_isort_config is None:
            cls.config_file = True
        else:
            cls.config_file = False

    def run(self):
        if self.config_file and not self.search_isort_config():
            yield 0, 0, self.no_config_msg, type(self)
        else:
            with OutputCapture():
                if self.filename == 'stdin':
                    sort_result = SortImports(
                        file_contents=pycodestyle.stdin_get_value(),
                        check=True,
                    )
                else:
                    sort_result = SortImports(self.filename, check=True)

            for line_num, message in self.sortimports_linenum_msg(sort_result):
                yield line_num, 0, message, type(self)

    def search_isort_config(self):
        """Search for isort configuration all the way up to the root folder

        Either on ``.isort.cfg`` file or an ``[isort]`` section on
        ``setup.cfg``.
        """
        full_path = os.path.abspath(self.filename)
        path_parts = full_path.split(os.path.sep)
        dirs_missing = len(path_parts)

        while dirs_missing > 0:
            dirs_missing -= 1
            partial_parts = path_parts[:dirs_missing]
            partial_path = os.sep.join(partial_parts)

            isort_file = '{0}{1}.isort.cfg'.format(partial_path, os.sep)
            if os.path.exists(isort_file):
                return True

            # If the setup file exists and has an "isort" section,
            # then we've found the configuration.
            setup_file = '{0}{1}setup.cfg'.format(partial_path, os.sep)
            if os.path.exists(setup_file):
                config = ConfigParser()
                config.read(setup_file)
                if 'isort' in config.sections():
                    return True

        return False

    def sortimports_linenum_msg(self, sort_result):
        """Parses isort.SortImports for line number changes and message.

        Uses a diff.Differ comparison of SortImport `in_lines`:`out_lines` to
        yield the line numbers of import lines that have been moved or blank
        lines added.

        Args:
            sort_imports (isort.SortImports): The isorts results object.

        Yields:
            tuple: A tuple of the specific isort line number and message.

        """

        self._fixup_sortimports_eof(sort_result)

        differ = Differ()
        diff = differ.compare(sort_result.in_lines, sort_result.out_lines)

        line_num = 0
        for line in diff:
            if line.startswith('  ', 0, 2):
                line_num += 1  # Ignore unchanged lines but increment line_num.
            elif line.startswith('- ', 0, 2):
                line_num += 1
                if line.strip() == '-':
                    yield line_num, self.isort_blank_unexp
                else:
                    yield line_num, self.isort_unsorted
            elif line.strip() == '+':
                # Include newline additions but do not increment line_num.
                yield line_num + 1, self.isort_blank_req

    @staticmethod
    def _fixup_sortimports_eof(sort_imports):
        """Ensure single end-of-file newline in `isort.SortImports.in_lines`.

        isort attempts to fix EOF blank lines but Flake8 will also flag them.
        So that these EOF changes are ignored in the diff comparison ensure
        that SortImports `in_lines` list has just the single EOF newline to
        match `out_lines` list.

        Args:
            sort_imports (isort.SortImports): The isorts results object.

        Returns:
            isort.SortImports: The modified isort results object.

        """

        for line in reversed(sort_imports.in_lines):
                if not line.strip():
                    sort_imports.in_lines.pop()
                else:
                    sort_imports.in_lines.append('')
                    return sort_imports
