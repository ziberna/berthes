# JunkBackup
# Copyright (C) 2011 Kantist
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with this program.
#     If not, see http://www.gnu.org/licenses/gpl-3.0.html

import os
import re
import glob
import subprocess

from junkbackup.cli import ARG, write, confirm

# wildcards don't work when quoted (e.g. rm "/dir/path/*"), so single strings
# are necessary
def file_op(cmd):
    if ARG.DRYRUN:
        retcode, output = 0, ''
    else:
        # TODO: make injection prevention not-shitty
        cmd = cmd.split(';')[0]
        retcode, output = subprocess.getstatusoutput(cmd)
    return retcode, output

def clean(root, dir=None, ignore_list=[]):
    # set dir paths
    dir_orig = os.getcwd()
    if not dir: dir = root
    # change dir, get contents, set counter
    os.chdir(dir)
    items = os.listdir()
    counter = 0
    # process every item in current dir
    for item in items:
        # get absolute path and turn it into relative from root
        item_abspath = os.path.abspath(item)
        item_path = re.sub("^%s" % re.escape(root), '', item_abspath)
        # check noremoves
        if item_path not in ignore_list:
            # if dir, search recursively, remove dir if empty
            if os.path.isdir(item) and not os.path.islink(item):
                count, empty = clean(root, item_abspath, ignore_list)
                counter += count
                if empty:
                    remove(item_abspath, item_path, isdir=True)
            # else, remove item
            elif remove(item_abspath, item_path):
                counter += 1
            else:
                write('ignored %s' % item_path)
        else:
            write('ignored %s' % item_path)
    # get empty-state
    empty = len(os.listdir()) == 0
    # change dir back
    os.chdir(dir_orig)
    # return counter and empty-state
    return counter, empty

def remove(path, path_short=None, isdir=False):
    # set shortened path if not given
    if not path_short: path_short = path
    # remove file, but ask first (if set)
    if not ARG.ASKREMOVE or confirm('Remove '+path_short+'?'):
        # create arg list
        args = ['rm']
        if isdir: args.append('-r')
        args.append(path)
        # combine into command, execute
        cmd = ' '.join(args)
        retcode, output = file_op(cmd)
        # check return code
        if retcode == 0:
            write('removed '+path_short)
        else:
            write('failed: '+cmd)
            write(output)
        return (retcode == 0)
    return False

def create_dir(path):
    retcode, output = file_op('mkdir -p '+path)
    return (retcode == 0)

def copy(src, trg, src_short=None, trg_short=None):
    if not src_short: src_short = src
    if not trg_short: trg_short = trg
    # ask first (if set)
    if ARG.ASKCOPY and not confirm('Copy '+src+' to '+trg_short+'?'):
        write('ignored %s' % src_short)
        return 0
    # check if target dir tree exists
    trg_tree = '/'.join(trg.split('/')[:-1])
    if not os.path.exists(trg_tree) and not create_dir(trg_tree):
        return 0
    # get items matching pattern, set counter
    src_items = glob.glob(src)
    counter = 0
    # copy each matched item
    for src_item in src_items:
        counter += copy_item(src_item, trg, trg_short=trg_short)
    return counter

def copy_item(src, trg, src_short=None, trg_short=None):
    if not src_short: src_short = src
    if not trg_short: trg_short = trg
    # create arg list
    args = ['cp', '-v']
    # add recursive option if source is dir
    if os.path.isdir(src):
        args.append('-r')
    # add source and target args
    args.extend([src, trg])
    # finally, copy
    cmd = ' '.join(args)
    retcode, output = file_op(cmd)
    # check return code
    if retcode == 0:
        write('copied '+src+' to '+trg_short)
        # count all copied files
        files = len(output.split('\n'))
        return files
    else:
        write('failed: '+cmd)
        write(output)
        return 0
