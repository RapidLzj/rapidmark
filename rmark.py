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
        c = ["""\\documentclass[a4paper,12pt]{article}
\\usepackage{graphicx}
\\usepackage[top=2cm,bottom=2.5cm,left=2cm,right=2cm]{geometry}
\\usepackage{xeCJK}
\\usepackage{indentfirst}
\\usepackage{color}
\\usepackage{epsfig}
\\setlength{\\baselineskip}{10pt}
\\setlength{\\parindent}{2em}
\\renewcommand{\\figurename}{图}
\\renewcommand{\\tablename}{表}

\\makeatletter
\\renewcommand\\section{\\@startsection{section}{0}{\\z@}%
{-2.5ex \\@plus -1ex \\@minus -.2ex}%
{1.3ex \\@plus.2ex}%
{\\normalfont\\large\\CJKfamily{hei}}}

\\renewcommand\\subsection{\\@startsection{subsection}{1}{\\z@}%
{-1.5ex \\@plus -1ex \\@minus -.2ex}%
{0.5ex \\@plus.2ex}%
{\\normalfont\\normalsize\\CJKfamily{hei}}}
\\makeatother

\\begin{document}
""" ]

    return c

##########################################################################################
def _load_file ( file ) :
    """ Load file content, do simple line process
    Include file, join continual line
    """
    # check file
    if not os.path.isfile(file) :
        print ("error: file not found '%s'" % file)
        exit(1)
    # read file into list
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    # preprocess file
    outlines = []
    cont_line = False
    for line in lines :
        # skip comment
        if not line.strip().startswith("@@") :
            # if is continued line, merge with previous
            if cont_line :
                aline += line.strip()
            else :
                aline = line.strip()
            # if this will continue, remove ... and continue, else process line
            if aline.endswith("...") :
                cont_line = True
                aline = aline[:-3]
            else :
                cont_line = False
                if aline.startswith("@inc") :
                    included = _load_file ( aline[4:].strip() )
                    outlines += included
                else :
                    outlines.append(aline)

    return outlines

##########################################################################################
def _process_format_one ( line, formatchar, formatstr ) :
    """ Process one format, line already preprocessed
    """
    pp = line.split(formatchar)
    inmode = False
    lp = "\n"
    res = []
    for p in pp:
        if not inmode :
            if p != "" and not p[0].isspace() and lp != "\n" :
                inmode = True
                res.append("\\"+formatstr+"{")
            elif lp != "\n" :
                res.append(formatchar)
            res.append(p)
        else :
            if lp != "" and not lp[-1].isspace() :
                inmode = False
                res.append("}")
            else :
                res.append(formatchar)
            res.append(p)
        lp = p
    if inmode : res.append("}")

    return "".join(res)

##########################################################################################
def _process_format ( line ) :
    """ Process emph, bold, underline format
    """
    xline = line.replace("\\*", "\x81").replace("\\_", "\x82").replace("**", "\x83")
    xline = _process_format_one(xline, "*", "emph")
    xline = _process_format_one(xline, "_", "underline")
    xline = _process_format_one(xline, "\x83", "textbf")
    xline = xline.replace("\x81", "*").replace("\x82", "\\_").replace("\x83", "**") \
                 .replace("\\+", "+").replace("\\@", "@").replace("\\#", "#")
    return xline

##########################################################################################
def _process_title ( levelname, title, enclose=True) :
    """ Process title line, main purpose is process with *
    """
    if not enclose :
        outline = "%s %s" % (levelname, _process_format(title))
    elif title[0] == "*" :
        outline = "%s*{%s}" % (levelname, _process_format(title[1:].strip()))
    else :
        outline = "%s{%s}" % (levelname, _process_format(title))
    return outline

##########################################################################################
def _process_tabfig_head ( line, tabfig ) :
    """ Process table or figure head, extract caption, label, file and size
    caption in [], label in <>, file in (), size at last
    If want to use []<>(), should add \ before. Second present of them will not be valid
    All part can be omitted. For figure, file must present, but not check here
    return a 5-item tuple: caption, label, file, width, height
    """
    xline = line.replace("\\[", "\x91").replace("\\]", "\x92") \
                .replace("\\<", "\x93").replace("\\>", "\x94") \
                .replace("\\(", "\x95").replace("\\)", "\x96")
    # caption
    p1, p2 = xline.find("["), xline.find("]")
    if p1 > -1 and p2 > p1 :
        cap = xline[p1+1:p2].replace("\x91", "\\[").replace("\x92", "\\]") \
                            .replace("\x93", "\\<").replace("\x94", "\\>") \
                            .replace("\x95", "\\(").replace("\x96", "\\)")
    else :
        cap = ""
    # label
    p1, p2 = xline.find("<"), xline.find(">")
    if p1 > -1 and p2 > p1 :
        lbl = xline[p1+1:p2].replace("\x91", "\\[").replace("\x92", "\\]") \
                            .replace("\x93", "\\<").replace("\x94", "\\>") \
                            .replace("\x95", "\\(").replace("\x96", "\\)")
    else :
        lbl = ""

    # for table, is enough
    if tabfig == "t" : return cap, lbl

    # else is figure, continue
    # figure file
    p1, p2 = xline.find("("), xline.find(")")
    if p1 > -1 and p2 > p1 :
        fig = xline[p1+1:p2].replace("\x91", "\\[").replace("\x92", "\\]") \
                            .replace("\x93", "\\<").replace("\x94", "\\>") \
                            .replace("\x95", "\\(").replace("\x96", "\\)")
    else :
        fig = ""
    # figure size
    if p2 > -1 and p2+1 < len(xline):
        siz = xline[p2+1:]
        pp = siz.split("*")
        if len(pp) == 1 :
            wid, hgh = siz.strip(), ""
        else :
            wid, hgh = pp[0].strip(), pp[1].strip()
    else :
        wid, hgh = "", ""
    if wid == "?" : wid = ""
    if hgh == "?" : hgh = ""

    return cap, lbl, fig, wid, hgh

##########################################################################################
def _process_figure ( line ) :
    """ Process figure, extract caption, label, size
    """
    cap, lbl, fig, wid, hgh = _process_tabfig_head(line, "f")
    if wid and hgh :
        siz = "[width=%s,height=%s]" % (wid, hgh)
    elif wid and not hgh :
        siz = "[width=%s]" % (wid)
    elif not wid and hgh :
        siz = "[height=%s]" % (hgh)
    else :
        siz = ""
    return ( "\\begin{figure}[htbp]\n" +
             "  \\begin{center}\n"
             "    \\includegraphics" + siz + "{" + fig + "}\n"
             "    \\caption{" + _process_format(cap) + "}\n"
             "    \\label{" + lbl + "}\n"
             "  \\end{center}\n"
             "\\end{figure}" )

##########################################################################################
def _process_table_head ( line ) :
    """ Process table head, extract caption, label
    """
    cap, lbl = _process_tabfig_head(line, "t")
    return ( "\\begin{table}\n" +
             "  \\caption{" + _process_format(cap) + "}\n" +
             "  \\label{" + lbl + "}\n" +
             "  \\begin{center}\n" +
             "    \\begin{tabular}" )

##########################################################################################
def _process_table_line ( line ) :
    """ Proess table lines. Divide line into cells, and format seperatedly
    """
    if line.endswith("---") :
        xline = line[:-3]
        hline = "\\\\ \\hline"
    else :
        xline = line
        hline = "\\\\"

    cell = xline.replace("\\&", "\x80").split("&")
    xline = _process_format(cell[0])
    for c in cell[1:] :
        xline += " & " + _process_format(c)

    return "      " + xline.replace("\x80", "\\&") + hline

##########################################################################################
def _process_line ( line, status ) :
    """ Interprete one line
    """

    if status == 0 :

        if line.startswith("#####") :
            outline = _process_title ( "\\subparagraph",  line[5:].strip() )

        elif line.startswith("####") :
            outline = _process_title ( "\\paragraph",     line[4:].strip() )

        elif line.startswith("###") :
            outline = _process_title ( "\\subsubsection", line[3:].strip() )

        elif line.startswith("##") :
            outline = _process_title ( "\\subsection",    line[2:].strip() )

        elif line.startswith("#") :
            outline = _process_title ( "\\section",       line[1:].strip() )

        elif line.startswith("* ") :
            status = 301
            outline = "\\begin{itemize}\n"   + _process_title ("  \\item", line[1:].strip(), False)

        elif line.startswith("+ ") :
            status = 302
            outline = "\\begin{enumerate}\n" + _process_title ("  \\item", line[1:].strip(), False)

        elif line.startswith("- ") :
            status = 303
            outline = "\\begin{descript}\n"  + _process_title ("  \\item", line[1:].strip(), False)

        elif line.startswith("@table") :
            status = 101
            outline = _process_table_head(line[6:].strip())

        elif line.startswith("@figure") :
            outline = _process_figure(line[6:].strip())

        elif line.startswith("@toc") :
            outline = "\\tableofcontent"

        elif line.startswith("@newpage") :
            outline = "\\newpage"

        elif line.startswith("@maketitle") :
            outline = "\\maketitle"

        elif line.startswith("@title") :
            outline = _process_title ( "\\title", line[6:].strip() )

        elif line.startswith("@author") :
            outline = _process_title ( "\\author", line[7:].strip() )

        elif line.startswith("@date") :
            outline = _process_title ( "\\date", line[5:].strip() )

        else :
            outline = _process_format(line.strip())

    elif status == 100 :
        if line == "" :
            outline = ("    \\end{tabular}\n" +
                       "  \\end{center}\n" +
                       "\\end{table}\n")
            status = 0
        else :
            outline = _process_table_line(line)

    elif status == 101 :
        status = 100
        outline = "      {" + line + "}"

    elif status == 301 :
        if line.startswith("* ") :
            outline = _process_title ("  \\item",line[1:].strip(), False)
        else :
            outline = "\\end{itemize}"
            status = -1

    elif status == 302 :
        if line.startswith("+ ") :
            outline = _process_title ("  \\item",line[1:].strip(), False)
        else :
            outline = "\\end{enumerate}"
            status = -1

    elif status == 303 :
        if line.startswith("-") :
            outline = _process_title ("  \\item",line[1:].strip(), False)
        else :
            outline = "\\end{descript}"
            status = -1

    else :
        outline = line

    return outline, status

##########################################################################################
def _process_file ( file ) :
    """ Interprete whole file
    """
    # Load file
    lines = _load_file(file)

    # Process
    status = 0
    result = []
    for line in lines:
        r, status = _process_line(line, status)
        result.append(r)
        if status == -1 :
            r, status = _process_line(line, 0)
            result.append(r)

    if status > 0 :
        # if last line did not close status, add an empty line
        r, status = _process_line("", status)
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
    out_tex_file = ""
    in_rmk_file = ""
    conf_file = ""
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
        out_tex_file = os.path.splitext(in_rmk_file)[0] + ".tex"
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
    f.write("\n\\end{document}\n")
    f.close()

    # OK!
    exit(0)