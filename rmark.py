#! /usr/bin/env python
"""
    This is a RapidMark Language interpreter
    Translate RapidMark to LaTeX

    Versions
        0.0  Jie 2016-07-02 Tucson
"""

import os
import sys


def _load_conf ( conf_file ) :
    """ Load configure from file.
    File priority: specified file - default file - function inside configure
    """
    return ""

def _mark_line ( line, status ) :
    """ Interprete one line
    """
    pass

def _mark_file ( file, conf ) :
    """ Interprete whole file
    """
    return []


if __name__ == "__main__" :
    # default configure
    version = """RapidMark Interpreter 0.01
    By Jie Zheng, 2016-07-02 Tucso
    (C) Seagull Softstudio"""
    helpinfo = """Syntax:
    rmark in_rmk_file [-o out_tex_file] [-c configure_file] [-h] [-v] [-w]
    -o: if no output file, default is same name but change ext to .tex
    -h: print this help info and exit
    -v: print version info and exit
    -w: overwrite if output file exists, else will fail
    """
    out_tex_file = ''
    in_rmk_file = ''
    conf_file = ''
    overwrite = False
    # command line configure
    for a in range(1, len(sys.argv)) :
        if sys.argv[a] == "-h" :
            # print help and exit
            print (helpinfo)
            exit(0)
        elif sys.argv[a] == "-v" :
            # print version and exit
            print (version)
            exit(0)
        elif sys.argv[a] == "-w" :
            # set overwrite flag
            overwrite = True
        elif sys.argv[a][0:2] == "-o" :
            # followed substring or next string is output file
            if len(sys.argv[a]) > 3 :
                out_tex_file = sys.argv[a][2:]
            elif a + 1 < len(sys.argv) :
                out_tex_file = sys.argv[a+1]
        elif sys.argv[a][0:2] == "-c" :
            # followed substring or next string is configure file
            if len(sys.argv[a]) > 3 :
                conf_file = sys.argv[a][2:]
            elif a + 1 < len(sys.argv) :
                conf_file = sys.argv[a+1]
        else :
            # if standalone string, is input, if previous arg is not closed, ignore
            if sys.argv[a-1] != "-o" and sys.argv[a-1] != "-c" :
                in_rmk_file = sys.argv[a]
    # if no input file, print help and exit
    if in_rmk_file == "" :
        print ("error: input file not specified\nUse -h for help")
        exit(1)
    if out_tex_file == "" :
        out_tex_file = os.path.splitext(in_rmk_file)[0] + '.tex'
    if not os.path.isfile(in_rmk_file) :
        print ("error: input file not exists '%s'\nUse -h for help" % in_rmk_file)
        exit(2)
    if conf_file != "" and not os.path.isfile(conf_file) :
        print ("error: configure file not exists '%s'\nUse -h for help" % conf_file)
        exit(3)
    if not overwrite and os.path.isfile(out_tex_file) :
        print ("error: output file already exists '%s'\nUse -h for help" % out_tex_file)
        exit(4)

    # all done, begin
    conf = _load_conf (conf_file)
    result = _mark_file (in_rmk_file, conf)
    f = open(out_tex_file, "w")
    for r in result:
        f.write(r + "\n")
    f.close()

    # OK!
    exit(0)