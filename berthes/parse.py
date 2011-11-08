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

import re

from berthes.cli import ARG
from berthes.tools import trim

def parse(conf_raw):
    # remove comments
    conf_raw = re.sub(r" *#.*?(\n|$)", "", conf_raw)
    # trim spaces and tabs
    conf_raw = re.sub(r"(?<=\n)( |\t)*|( |\t)*(?=\n)", "", conf_raw)
    # remove empty lines (start|middle|end)
    conf_raw = re.sub(r"^\n+|(?<=\n)\n+|\n+$", "", conf_raw)
    
    # split by lines
    conf_lines = conf_raw.split("\n")
    
    # prepare dict
    conf_dict = {
        'FLAGS':[],
        'ROOT':[],
        'NOCOPY':[],
        'NOREMOVE':[],
        'PATHS':[]
    }
    # define option variables
    opt_name = None
    opt_pair = None
    
    # parse into dict
    for conf_line in conf_lines:
        # check for an [option header]
        opt_match = re.search("(?<=\[).*?(?=\])", conf_line)
        
        if opt_match: # add new option
            opt_name = opt_match.group(0)
            # check for default option, else is path pair
            opt_pair = opt_name not in conf_dict
            if opt_pair:
                # parse path pair into list
                opt_pair = parse_dir_pattern(opt_name)
        elif opt_name: # add to current option
            if opt_pair:
                file_pair = parse_file_pattern(conf_line)
                for n in [0,1]:
                    file_pair[n] = add_root_path(file_pair[n], opt_pair[n])
                conf_dict['PATHS'].append(file_pair)
            else:
                if opt_name == 'ROOT': var = format_dir_path(conf_line)
                elif opt_name == 'FLAGS': var = conf_line
                else: var = format_file_path(conf_line)
                conf_dict[opt_name].append(var)
    # set each flag if it wasn't passed from cli
    for name in conf_dict['FLAGS']:
        if ARG.get(name) == None:
            ARG.set(name, True)
    
    return conf_dict['ROOT'], conf_dict['PATHS'], conf_dict['NOCOPY'], conf_dict['NOREMOVE']

def parse_dir_pattern(dir_pattern):
    # split dir pattern into pair
    dir_pair = [format_dir_path(dir) for dir in dir_pattern.split(':')]
    # add empty path if it's not full pair
    if len(dir_pair) == 1: dir_pair.append('')
    return dir_pair

def parse_file_pattern(file_pattern):
    # split file pattern into pair
    file_pair = [format_file_path(file) for file in file_pattern.split(':')]
    # add empty path if it's not full pair
    if len(file_pair) == 1: file_pair.append('')
    return file_pair

def format_dir_path(dir_path):
    # format slashes properly for a dir path
    dir_path = dir_path.strip()
    if dir_path == '': return dir_path
    return trim(dir_path, '/', left_most=1, right=1)

def format_file_path(file_path):
    # format slashes properly for a file path
    file_path = file_path.strip()
    file_path = trim(file_path, '/', left_most=1, right_most=1)
    # add wildcard asterisk if path points to directory
    if file_path.endswith('/'): file_path += '*'
    return file_path

def add_root_path(path, root_path):
    # add a root path to a custom path unless the latter is already root
    return path if path.startswith('/') else root_path + path
