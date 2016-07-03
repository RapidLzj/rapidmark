# rapidmark
Try to define a simple mark language, can be easily transfered to LaTeX code, and generage pdf document.

This language, I call it rapidmark. With ext name `.rmk`.

## System
This system is writen in python 2.7 or 3.0, I am trying to use common part so it can run ob both.

This will transfer my specied mark language text into LaTeX text.

## Language
Transfer rules:

### Basic

All leading and tailing space or tab is omitted.

### Comment

A line start with @@ is a comment.

Comment must be write in a standalone line.

### Section titles

| Mark | LeTeX |
|:-----|:------|
| \# | section |
| \#\# | subsection |
| \#\#\# | subsubsection |
| \#\#\#\# | paragraph |
| \#\#\#\#\# | subparagraph |
| \#\* | section without number |

*For paragraph and subparagraph, the content in the \# line will be taken into { }, the following will be normal text.*

### @ Command

Used to start a rapidmark command

|  Command   | Description |
|------------|-------------|
| @inc xxx   | include file |
| @newpage   | generate a new page |
| @toc       | table of contents |
| @title     | set title for maketitle |
| @author    | set author for maketitle |
| @date      | set date for maketitle |
| @maketitle | make title |
| @table     | table command, discuss below |
| @figure    | figure command, discuss below |

*@inc will do an rapidmark include, include another rapidmark file into current place, not generate a LeTeX include command.*

### @table

@table[caption]\<label>

Label and caption can be omitted.

Format line: |c|l|r|... same as LaTeX

Body lines: also same as LaTeX, but use --- in a standlone line to stand for a horizon line. 

Difference: end of line default present a new row in table. If want to sperate a line in two or more lines, must use ... at end to present a unfinished line.

### @figure

@figure[caption]\<label>(figure file name)width\*height

Label and caption can be omitted.

You can write like this: 10cm\*? or ?\*38mm, or ?\*?.
If width and height are all omitted, size description is not necessory.

### List

Lines start with */+/- are list items.

\* stands for itemize, \+ for enumerate, \- for description.

List item must starts with \* or \+ or \-, and at least a space between tag and text.

\*, \+ and \- cannot be mixed. If mixed, the list will be seperated into different lists.

*For descript, the first word will be in [ ], if want to use more word, you need to write [ ] manually.*

### Special format

Use formater character to enclose those text with format

*No space between \*/\_ and text*

*Special format will work in same line, not good when go to next line.*

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
