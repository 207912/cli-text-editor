# Command-Line Text Editor in Python

A small editor for a multi-line text buffer. It supports character and word
navigation, inserting and deleting text, swapping words, and moving whole
lines. Commands are case-sensitive and run when you press Enter.

## Run locally

From the repository root with Python 3:

```sh
python editor.py
```

The editor uses only the Python standard library. The buffer lives in memory
for the session. Use `v` to print all lines as plain text.

## Example session

Type these commands one at a time, pressing Enter after each one:

```text
ihello world
sw
o
isecond line
J
v
q
```

The `v` command prints:

```text
second line
world hello
```

## Commands

| Commands | Action |
| --- | --- |
| `?`, `v`, `q` | Show help, print all lines, quit |
| `h`, `l`, `^`, `$` | Move left, right, to line start, or to line end |
| `w`, `b`, `e` | Move to the next word start, a previous word start, or the next word end |
| `iTEXT`, `aTEXT`, `ITEXT`, `ATEXT` | Insert before or after the cursor, or at the start or end of the line |
| `x`, `X`, `dw`, `de`, `db`, `dc` | Delete characters or word ranges |
| `sw`, `sb` | Swap the current word with the next or previous word |
| `j`, `k`, positive line number | Move up, down, or jump to a line |
| `o`, `O`, `dd`, `J`, `K` | Insert a line below or above, delete a line, or move it up or down |
| `.`, `;` | Toggle the highlighted character or the active-line marker |

The editor finds words as runs of non-whitespace characters. The cursor points
to a character on the active line and resets to column zero on an empty line.

## Tests

```sh
python -m unittest discover -s tests -v
```

The tests exercise the command-line interface, including empty lines, word
navigation and deletion, line movement, invalid input and end-of-input handling.
