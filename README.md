# rapidmark
Try to define a simple mark language, can be easily transfered to LaTeX code, and generage pdf document.

## System
This system is writen in python 2.7 or 3.0, I am trying to use common part so it can run ob both.

This will transfer my specied mark language text into LaTeX text.

## Language
Transfer rules:

Section titles

| Mark   | LeTeX |
|--------|-------|
|\#      | \\section |
|\#\#    | \\subsection |
|\#\#\#  | \\subsubsection |
