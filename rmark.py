#! /usr/bin/env python
# coding: UTF-8
"""
    This is a RapidMark Language interpreter
    Translate RapidMark to LaTeX

    Versions
        0.0  Jie 2016-07-02 Tucson
"""

import os
import sys


##########################################################################################
def _load_conf ( conf_file ) :
    """ Load configure from file.
    File priority: specified file - default file - function inside configure
    """
    cfile = conf_file if conf_file != "" else "~/.rapidmark.conf"
    if os.path.isfile(cfile) :
        f = open(cfile, "r")
        c = f.readlines()
        f.close()
    else :
        c = ["""
\documentclass[a4paper,12pt]{article}
\usepackage{graphicx}
\usepackage[top=2cm,bottom=2.5cm,left=2cm,right=2cm]{geometry}
\usepackage{xeCJK}
\usepackage{indentfirst}
\usepackage{color}
\usepackage{epsfig}
\setlength{\baselineskip}{10pt}
\setlength{\parindent}{2em}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}

\makeatletter
\renewcommand\section{\@startsection{section}{0}{\z@}%
{-2.5ex \@plus -1ex \@minus -.2ex}%
{1.3ex \@plus.2ex}%
{\normalfont\large\CJKfamily{hei}}}

\renewcommand\subsection{\@startsection{subsection}{1}{\z@}%
{-1.5ex \@plus -1ex \@minus -.2ex}%
{0.5ex \@plus.2ex}%
{\normalfont\normalsize\CJKfamily{hei}}}
\makeatother
""" ]

    return c

##########################################################################################
def _transfer_char ( line ) :
    """ Transfer escape character back to normal format
    including: \# \* \+ \- \@ \\
    """
    return line.replace('\\#', '#') \
               .replace('\\*', '*') \
               .replace('\\+', '+') \
               .replace('\\@', '@') \
               .replace('\\\\', '\\')

def _process_title ( levelname, title ) :
    """ Process title line, main purpose is process with *
    """
    if title[0] == "*" :
        outline = "\\%s*{%s}" % (levelname, _transfer_char(title[1:].strip()))
    else :
        outline = "\\%s{%s}" % (levelname, _transfer_char(title))
    return outline

##########################################################################################
def _process_line ( line, status ) :
    """ Interprete one line
    status:
        0  : initial status
        10x: table mode
            100: normal table mode
            101: inside caotion
            102: inside label
            105: inside format line
        20x: figure mode
            200: normal figure mode
            201: inside caotion
            202: inside label
            204: inside figure filename
            205: inside size
        30x: list mode
            301: itemize (*)
            302: enumerate (+)
            303: descript (-)
    """

    if line.startswith("@@") :
        outline = ""

    elif line.startswith("#####") :
        outline = _process_title ( "subparagraph", line[5:].strip() )

    elif line.startswith("####") :
        outline = _process_title ( "paragraph", line[4:].strip() )

    elif line.startswith("###") :
        outline = _process_title ( "subsubsection", line[3:].strip() )

    elif line.startswith("##") :
        outline = _process_title ( "subsection", line[2:].strip() )

    elif line.startswith("#") :
        outline = _process_title ( "section", line[1:].strip() )

    elif line.startswith("@toc") :
        outline = "\\tableofcontent"

    elif line.startswith("@newpage") :
        outline = "\\newpage"

    elif line.startswith("@maketitle") :
        outline = "\\maketitle"

    elif line.startswith("@title") :
        outline = _process_title ( "title", line[6:].strip() )

    elif line.startswith("@author") :
        outline = _process_title ( "author", line[7:].strip() )

    elif line.startswith("@date") :
        outline = _process_title ( "date", line[5:].strip() )

    return outline, status

##########################################################################################
def _process_file ( file ) :
    """ Interprete whole file
    """
    # Load file
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    # Process
    status = 0
    result = []
    for line in lines:
        r, status = _process_line(line.strip(), status)
        result.append(r)

    return result


##########################################################################################
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
    result = _process_file (in_rmk_file)
    f = open(out_tex_file, "w")
    for c in conf:
        f.write(c + "\n")
    for r in result:
        f.write(r + "\n")
    f.close()

    # OK!
    exit(0)