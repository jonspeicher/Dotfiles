#!/usr/bin/env python

# TBD: .vimrc vs. _vimrc, .vim vs vimfiles, Windows vs. OS X, copying vs. linking, recursive copy of
# .vim/vimfiles? Symlinking on Windows? Finding .copydot_ files when invoked from outside the dotfiles
# directory?

# TBD: Moment of clarity: .copydot_ignore and .copydot_leader or whatever are OS-specific and maybe even
# machine-specific, so they should live in ~ on each machine, and copydot should be run from ~ on each machine,
# so finding them shouldn't be hard. Or, there can be "base" versions like copydot_ignore.win that live in dotfiles
# that can be copied up when copydot is first run, and everything should be symlinked, even on Windows with mklink
# or whatever, unless and until I decide I need copying, which I should try to get by without. KISS.

import collections, glob, itertools, os, shutil, sys

COMMON_DIRECTORY = 'Dotfiles'
CURRENT_DIRECTORY = '.'

IGNORE_FILENAME = '.copydot_ignore'
LEADER_FILENAME = '.copydot_leader'
DEFAULT_LEADER = '.'

def constant_factory(value):
    return itertools.repeat(value).next

def lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def pairs(filename):
    for line in lines(filename):
        yield line.split()

def paths(directory, filenames):
    return [os.path.join(directory, filename) for filename in filenames]

def copy_from_to(source_paths, destination_paths, print_copy):
    copy_pairs = zip(source_paths, destination_paths)
    for copy_pair in copy_pairs:
        source, destination = copy_pair[0], copy_pair[1]
        print_copy(source, destination)
        shutil.copyfile(source, destination)

def print_file_copy_from_to(from_path, to_path):
    print '    ' + os.path.basename(from_path) + ' => ' + os.path.basename(to_path)

copy_out = ((len(sys.argv) > 1) and (sys.argv[1] == 'out'))
leaders = collections.defaultdict(constant_factory(DEFAULT_LEADER), pairs(LEADER_FILENAME))
ignore_filenames = lines(IGNORE_FILENAME)

filenames = os.listdir(COMMON_DIRECTORY)
common_filenames = [filename for filename in filenames if filename not in ignore_filenames]
common_paths = paths(COMMON_DIRECTORY, common_filenames)

cwd_filenames = [leaders[filename] + filename for filename in common_filenames]
cwd_paths = paths(CURRENT_DIRECTORY, cwd_filenames)

if copy_out:
    print '\nCopying out from ' + CURRENT_DIRECTORY + ' to ' + COMMON_DIRECTORY
    copy_from_to(cwd_paths, common_paths, print_file_copy_from_to)
else:
    print '\nCopying in to ' + CURRENT_DIRECTORY + ' from ' + COMMON_DIRECTORY
    copy_from_to(common_paths, cwd_paths, print_file_copy_from_to)
