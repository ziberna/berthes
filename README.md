berthes
=======

Installation
------------
1. copy the file from bin to your `$PATH` (e.g. /usr/bin)
2. copy berthes directory to your `$PYTHONPATH` (e.g. /usr/lib/python3.2/site-packages)
3. create file ~/.config/berthes
4. check configuration syntax below and edit the file ~/.config/berthes


Help message
------------

    usage: berthes [-h] [-cp | -cp!] [-acp | -acp!] [-cl | -cl!] [-arm | -arm!]
                      [-dr | -dr!] [-v | -v!]
    
    Berthes
    
    optional arguments:
      -h, --help  show this help message and exit
      -cp         copy to backup dirs
      -cp!        do NOT copy to backup dirs
      -acp        ask for each copy
      -acp!       do NOT ask for each copy
      -cl         clean backup dirs
      -cl!        do NOT clean backup dirs
      -arm        ask for each remove
      -arm!       do NOT ask for each remove
      -dr         perform a dry run
      -dr!        do NOT perform a dry run
      -v          be verbose
      -v!         do NOT be verbose



Config file syntax
------------------

    # this is a comment, it starts with a hash symbol
    [FLAGS] # default flags (which can be overridden as cmd args)
    COPY
    ASKCOPY
    CLEAN
    ASKREMOVE
    VERBOSE
    DRYRUN
    
    [ROOT] # absolute path of your backup directory
    /backup/root/path
    
    [NOCOPY] # stuff that matches pattern, but you don't want to copy
    filename
    subdir/filename
    
    [NOREMOVE] # stuff that you put manually in your backup directory
    filename
    subdir/filename
    
    [/source/root/path:target/root/path] # source:target (ROOT applied)
    /source/filename1:subdir/filename2
    /source/filename3:filename4
    /source/filename5

License
-------

    Berthes (after Russell's 5-minutes-ago hypothesis)  (C) 2011  Jure Žiberna
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under the terms of the GNU General Public License, version 3 or later.


Why Russell's 5-minutes-ago hypothesis?
---------------------------------------

Because moving backed-up configuration files to a new system makes
the system behave as if it was configured after a long period of time.
Bertrand Russell's hypothesis states that the world might have been
created 5 minutes ago together with all our memories of previous events.

