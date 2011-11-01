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
#
# JunkBackup allows overriding arguments from config file via command-line
# arguments. So when the config file is parsed, I need to be able to tell
# whether argument was overridden or not. This means there are 3 states:
#  - yes
#  - no
#  - wasn't set
# argparse library doesn't support such states with mutual exclusive arguments,
# so I've written a little singleton that does all the checks for me.
#
# Yes, it's a singleton, and here's why:
#  - easier to manage
#  - clearer code
#  - and most importantly; it's global, baby
# Any change from any module is global, which allows me to separate code into
# multiple files without any hacks to keep ARG synchronized.

import re
import argparse

class Arg(object):
    def __init__(self, description='<description here>'):
        self._opt_ = {}
        self._help_ = {}
        self.parser = argparse.ArgumentParser(description=description)
    
    def description(self, description):
        self.parser.description = description
    
    def add(self, name, state=None, opt='', help=''):
        self.set(name, state)
        self.opt(name, opt)
        self.help(name, help)
        if opt:
            self.add_to_parser(name)
    
    def add_to_parser(self, name):
        opt = '-%s' % self.opt(name)
        help = self.help(name)
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(opt, action='store_true', help=help)
        group.add_argument('%s!' % opt, action='store_true', help='do NOT %s' % help)
    
    def parse(self):
        args = self.parser.parse_args().__dict__
        for name in self._opt_:
            opt = self.opt(name)
            yes = args[opt]
            no = args['%s!' % opt]
            state = yes if (yes or no) else None
            self.set(name, state)
            del args[opt]
            del args['%s!' % opt]
        for name in args:
            self.set(name.upper(), args[name])
    
    def has(self, name):
        return name in self.__dict__
    
    def set(self, name, state):
        self.__dict__[name] = state
    
    def get(self, name):
        return self.__dict__[name] if self.has(name) else None

    def set_once(self, name, state):
        if self.get(name) == None:
            self.set(name, state)
    
    def opt(self, name, opt=None):
        if opt: self._opt_[name] = opt
        else: return self._opt_[name]
    
    def help(self, name, help=None):
        if help: self._help_[name] = help
        else: return self._help_[name]

ARG = Arg()

#============================== User interaction =============================#
# this is really a specific method for JunkBackup, so change it to your liking
def write(text, force=False):
    if not force and not ARG.VERBOSE: return
    text = re.sub(r"^::", r"\033[1;32m::\033[m", text)
    # highlight file operations
    text = re.sub(r"^removed", r"  \033[1;34mremoved\033[m", text)
    if re.match(r"^copied", text):
        text = re.sub(r"^copied", r"  \033[1;33mcopied\033[m", text)
        text = re.sub(r" to ", r"\033[1;33m to \033[m", text)
    text = re.sub(r"^ignored", r"  \033[1;35mignored\033[m", text)
    text = re.sub(r"^failed", r"  \033[1;31mfailed\033[m", text)
    text = re.sub(r"^([a-zA-z0-9]+)", r"  \033[1;36m\1\033[m", text)
    print(text)

def confirm(question):
    return input(' %s ' % question).lower() in ['y','yes', 'yeah','ok']


#==================================== TEST ===================================#
if __name__ == '__main__':
    ARG.description('Testing this module...')
    ARG.add('option', opt='o', help='use option')
    ARG.add('VERBOSE', opt='v', help='be verbose')
    ARG.parse()
    print('option state:', ARG.option)
    print('VERBOSE state:', ARG.VERBOSE)
    if confirm('Is this just a test?'):
        write("Correct!")
    else:
        write("Incorrect!")
