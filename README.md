# rapidmark
Try to define a simple mark language, can be easily transfered to LaTeX code, and generage pdf document.

## System
This system is writen in python 2.7 or 3.0, I am trying to use common part so it can run ob both.

This will transfer my specied mark language text into LaTeX text.

## Language
Transfer rules:

###Section titles

| Mark   | LeTeX |
|--------|-------|
| \# | section |
| \#\# | subsection |
| \#\#\# | subsubsection |
| \#\#\#\# | paragraph |
| \#\#\#\#\# | subparagraph |
| \#* | section without number |

###@

Used to start a rapidmark command

| Command | Description |
|---------|-------------|
| @inc xxx | include file |
| @newpage | generate a new page |
| @toc     | table of contents |
| @title   | make title |
| @table   | table command, discuss below |
| @figure  | figure command, discuss below |

###Special format

Use formater character to enclose those text with format

| formater | format |
|----------|--------|
| \*xxx\*     | emphasis (italic) |
| \*\*xxx\*\* | bold |
| \_xxx\_     | underlined |

Other text transfered directly to LaTeX command or text.

## Note

This system is just for myself, make me easy when write LaTeX file.
Not response for others.

If any suggestions, tell me at lzj@lzj.name
