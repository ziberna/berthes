# Berthes (after Russell's 5-minutes-ago hypothesis)
# Copyright (C) 2011 Jure Žiberna
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see http://www.gnu.org/licenses/gpl-3.0.html

import os
import re

from berthes.parse import parse, add_root_path
from berthes.file_op import copy, clean
from berthes.cli import ARG, write

#============================== Global variables =============================#
CONF_PATH = os.environ['HOME'] + "/.config/berthes"

#=============================== Working  class ==============================#
class Berthes(object):
    def __init__(self, root=[], paths=[], nocopy=[], noremove=[]):
        self.root = root
        self.paths = paths
        self.nocopy = nocopy
        self.noremove = noremove
    
    def run(self):
        try:
            for root in self.root:
                # clean root directory (if set)
                if ARG.CLEAN:
                    write(':: Cleaning files from %s' % root)
                    rm_count, empty = clean(root, ignore_list=self.noremove)
                    write('%i files removed' % rm_count)
                # copy to root directory (if set)
                if ARG.COPY:
                    write(':: Copying files to %s' % root)
                    cp_count = self.copy(root)
                    write('%i files copied' % cp_count)
        
        except KeyboardInterrupt:
            print('')
        finally:
            final_msg = ':: Done'
            if ARG.DRYRUN: final_msg += ' (note: this was just a DRYRUN)'
            write(final_msg) 
    
    def copy(self, root):
        # set counter
        counter = 0
        for src, trg in self.paths:
            # turn pair into absolute paths
            src_abs, trg_abs = [add_root_path(file, root) for file in [src, trg]]
            # copy and increment copy-counter
            counter += copy(src_abs, trg_abs, trg_short=trg)
        return counter

#================================= Parse file ================================#
def parse_file(conf_path=CONF_PATH):
    if ARG.CONF: conf_path = ARG.CONF
    # read configuration file
    try:
        conf_raw = open(conf_path).read()
    except IOError:
        write("failed: file '%s' doesn't exist" % conf_path, force=True)
        return None
    # parse text, pass arguments to Berthes
    return Berthes(*parse(conf_raw))

#=============================== User interface ==============================#
def cli_init():
    global ARG;
    ARG.description('Berthes')
    ARG.add('COPY', opt='cp', help='copy to backup dirs')
    ARG.add('ASKCOPY', opt='acp', help='ask for each copy')
    ARG.add('CLEAN', opt='cl', help='clean backup dirs')
    ARG.add('ASKREMOVE', opt='arm', help='ask for each remove')
    ARG.add('DRYRUN', opt='dr', help='perform a dry run')
    ARG.add('VERBOSE', opt='v', help='be verbose')
    ARG.parser.add_argument('-conf', metavar='conf_path', help='path to config file')
    ARG.parse()
    
#==================================== TEST ===================================#
if __name__ == '__main__':
    cli_init()
    BT = parse_file()
    if BT: BT.run()
