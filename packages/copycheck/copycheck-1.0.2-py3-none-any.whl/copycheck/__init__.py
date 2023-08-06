#!/usr/bin/env python

# Copyright 2016 Janus Friis Nielsen. All rights reserved.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''
    The *copycheck* package provides a way to check files for missing
    copyright headers.

    See "README.rst" or <https://github.com/janusdn/copycheck>
    for more information.
'''

import os
import sys
import argparse
from enum import Enum

import collections
import types

import pathspec

from .__about__ import __version__

COPYRIGHT_IGNORE_FILENAME = ".copyrightignore"

MODULE = sys.modules[__name__]

MODULE.is_verbose = False
MODULE.is_debug = False


def verbose(message):
    '''
        Print message if *verbose* output is enabled.
    '''
    if MODULE.is_verbose:
        print(message)


def debug(message):
    '''
        Print message if *debug* output is enabled.
    '''
    if MODULE.is_debug:
        print(message)


def has_copyright(file):
    '''
        Returns true if the word *copyright* appears
        in the first 10 lines.
    '''
    for _ in range(10):
        line = file.readline()
        if not line == "":
            if "copyright" in line.lower():
                return True
    return False


def print_files(files):
    '''
        Print name of files without copyright header.
    '''
    print("Found", len(files), "files without copyright notices:")
    for filename in files:
        print(str(filename))


def util_diff_files(patterns, files):
    '''
        Matches the files to the patterns.
        *patterns* (``collections.Iterable`` of ``pathspec.Pattern``) contains
        the patterns to use.
        *files* (``collections.Iterable`` of ``str``) contains the normalized
        file paths to be matched against *patterns*.
        Returns the matched files (``set`` of ``str``).
    '''
    all_files = files if isinstance(files, collections.Container) else list(files)
    return_files = set()
    return_files.update(all_files)
    for pattern in patterns:
        if pattern.include is not None:
            result_files = pattern.match(all_files)
            if pattern.include:
                return_files.difference_update(result_files)

    return return_files


def patch_pathspec(target):
    '''
        Add methods to pathspec for computing the files not matched by the
        patterns.
    '''
    def diff_files(self, files, separators=None):
        '''
            Matches the files to this path-spec.
            *files* (``collections.Iterable`` of ``str``) contains the file
            paths to be matched against *patterns*.
            *separators* (``collections.Container`` of ``str``) optionally
            contains the path separators to normalize. This does not need to
            include the POSIX path separator (`/`), but including it will not
            affect the results. Default is ``None`` to determine the separators
            based upon the current operating system by examining `os.sep` and
            `os.altsep`. To prevent normalization, pass an empty container
            (e.g., an empty tuple `()`).
            Returns the files which do not match the path-spec(``collections.Iterable`` of ``str``).
        '''
        file_map = pathspec.util.normalize_files(files, separators=separators)
        diffed_files = util_diff_files(self.patterns, file_map.keys())
        for path in diffed_files:
            yield file_map[path]

    def diff_tree(self, root):
        '''
            Walks the specified root path for all files and matches them to this
            path-spec.
            *root* (``str``) is the root directory to search for files.
            Returns all non-matching files (``collections.Iterable`` of ``str``).
        '''
        files = pathspec.util.iter_tree(root)
        return self.diff_files(files)

    target.diff_files = types.MethodType(diff_files, target)
    target.diff_tree = types.MethodType(diff_tree, target)


class BashColors(Enum):
    '''
        Values used for coloring of output in bash.
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def find_no_copyright_files(path, spec):
    '''
        Examine all files recursively reachable from path,
        but not matching spec. For each file check if the file
        has a copyright header.

        Returns a list of all files missing a copyright header.
    '''
    no_copyright_files = []
    verbose("Examining files:")
    verbose(' - ' + str(path))
    patch_pathspec(spec)
    diff_files = spec.diff_tree(path)
    for filename in diff_files:
        full_path = os.path.join(path, filename)
        try:
            with open(full_path, 'rt') as file:
                if not has_copyright(file):
                    no_copyright_files.append(filename)
                    verbose(BashColors.FAIL.value + ' \u274C ' +
                            str(full_path) + BashColors.ENDC.value)
                else:
                    verbose(BashColors.OKGREEN.value + ' \u2705 ' +
                            str(full_path) + BashColors.ENDC.value)
        except (UnicodeDecodeError, IOError) as ex:
            debug(ex)
    return no_copyright_files


def find_missing_copyright(paths):
    '''
        Find all files missing a copyright header from each of the paths.

        Returns a list of all files missing a copyright header.
    '''
    no_copyright_files = []
    for path in paths:
        path = os.path.abspath(path)
        debug(path)
        pattern_factory_name = 'gitwildmatch'
        try:
            with open(os.path.join(path, COPYRIGHT_IGNORE_FILENAME), 'r') as filehandle:
                verbose('Using "{}" file from "{}"'.format(COPYRIGHT_IGNORE_FILENAME, path))
                spec = pathspec.PathSpec.from_lines(pattern_factory_name, filehandle)
        except (OSError, IOError):
            spec = pathspec.PathSpec.from_lines(pattern_factory_name, '')

        pattern_factory = pathspec.util.lookup_pattern(pattern_factory_name)
        ignore_file_pattern = pattern_factory(COPYRIGHT_IGNORE_FILENAME)
        spec.patterns.append(ignore_file_pattern)
        no_copyright_files += find_no_copyright_files(path, spec)
    return no_copyright_files


def check(arguments):
    '''
        Check files for missing copyright header as specified in the arguments.

        Print all files with missing headers to standard out.
    '''
    args = []
    if not arguments.paths:
        current_working_dir = os.path.normpath(os.getcwd())
        verbose("Current working directory: {}".format(current_working_dir))
        args = [current_working_dir]
    else:
        args = arguments.paths

    no_copyright_files = find_missing_copyright(args)

    if no_copyright_files:
        print_files(no_copyright_files)
        sys.exit(1)
    else:
        print("Found no files without copyright notice.")
        sys.exit(0)


def main():
    '''
        Main entrypoint. Define arguments and pass on to specific subcommand.
    '''

    # Argument parser.
    # Main parser.
    parser = argparse.ArgumentParser(description='Check source files for missing copyright headers')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--debug',
                        action="store",
                        default=False,
                        dest="debug",
                        help='Enable debug output')

    # Parsers for subcommands.
    subparsers = parser.add_subparsers(help='sub-commands')

    # Parser for start command.
    parser_start = subparsers.add_parser('check', help='check for missing copyright headers')
    parser_start.add_argument('paths',
                              action="append",
                              default=[],
                              help='a number of paths to check')

    parser_start.set_defaults(command=check)

    args = parser.parse_args()

    MODULE.is_verbose = args.verbose
    MODULE.is_debug = args.debug
    if MODULE.is_debug:
        MODULE.is_verbose = True

    if 'command' in args:
        args.command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
