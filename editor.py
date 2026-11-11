"""
A simple command-line text editor module.
Provides cursor movement, text editing, and command parsing functions.
"""
import re

CURSOR_CURRENT_INDEX = 0
ROW_CURSOR_ON = True
EDITOR_LINES = [""]
ACTIVE_LINE_INDEX = 0
LINE_CURSOR_ON = False


def show_help_menu():
    """
    Display the help menu with available editor commands.
    """
    help_text = '''? - display this help info
. - toggle row cursor on and off
h - move cursor left
l - move cursor right
^ - move cursor to beginning of the line
$ - move cursor to end of the line
w - move cursor to beginning of next word
b - move cursor to beginning of current or previous word
e - move cursor to end of the word
i - insert <text> before cursor
a - append <text> after cursor
I - insert <text> from beginning
A - append <text> at the end
x - delete character at cursor
X - delete character before cursor
dw - delete to start of next word
de - delete through the next word end
db - delete to start of current or previous word
dc - delete whitespaces or entire word at cursor
sw - swap word at cursor with next word
sb - swap word at cursor with previous word
; - toggle line cursor on and off
j - move cursor up
k - move cursor down
o - insert empty line below
O - insert empty line above
dd - delete line
K - move line down
J - move line up
Line_No. - jump to specific line, first character
v - view all lines without cursor markers
q - quit program'''

    print(help_text)


def toggle_row_cursor():
    """
    Toggle the row cursor display on or off.
    """
    global ROW_CURSOR_ON
    ROW_CURSOR_ON = not ROW_CURSOR_ON


def clamp_cursor():
    """Keep the column valid after edits and line changes."""
    global CURSOR_CURRENT_INDEX
    last_column = max(len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1, 0)
    CURSOR_CURRENT_INDEX = min(max(CURSOR_CURRENT_INDEX, 0), last_column)


def render_editor_view():
    """Display the buffer with the enabled cursor markers."""
    for index, line in enumerate(EDITOR_LINES):
        active = index == ACTIVE_LINE_INDEX
        marker = ("*" if active else " ") if LINE_CURSOR_ON else ""
        if active and line and ROW_CURSOR_ON:
            column = CURSOR_CURRENT_INDEX
            line = f"{line[:column]}\033[42m{line[column]}\033[0m{line[column + 1:]}"
        print(marker + line)


def move_cursor_left():
    """
    Move the cursor one position to the left.
    """
    global CURSOR_CURRENT_INDEX
    if CURSOR_CURRENT_INDEX > 0:
        CURSOR_CURRENT_INDEX -= 1


def move_cursor_right():
    """
    Move the cursor one position to the right.
    """
    global CURSOR_CURRENT_INDEX, EDITOR_LINES, ACTIVE_LINE_INDEX
    if CURSOR_CURRENT_INDEX < len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1:
        CURSOR_CURRENT_INDEX += 1


def move_to_beginning_of_line():
    """
    Move the cursor to the beginning of the line.
    """
    global CURSOR_CURRENT_INDEX
    CURSOR_CURRENT_INDEX = 0


def move_to_end_of_line():
    """
    Move the cursor to the end of the line.
    """
    global CURSOR_CURRENT_INDEX, EDITOR_LINES, ACTIVE_LINE_INDEX
    CURSOR_CURRENT_INDEX = len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1 if EDITOR_LINES[ACTIVE_LINE_INDEX] else 0


def move_to_next_word():
    """
    Move the cursor to the beginning of the next word.
    """
    global CURSOR_CURRENT_INDEX, EDITOR_LINES, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    for item in matches:
        if item.start() > CURSOR_CURRENT_INDEX:
            CURSOR_CURRENT_INDEX = item.start()
            return
    CURSOR_CURRENT_INDEX = max(len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1, 0)


def move_to_previous_word():
    """
    Move the cursor to the beginning of the current or previous word.
    """
    global CURSOR_CURRENT_INDEX, EDITOR_LINES, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    if not EDITOR_LINES[ACTIVE_LINE_INDEX]:
        return
    while EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX].isspace():
        CURSOR_CURRENT_INDEX -= 1
        if CURSOR_CURRENT_INDEX < 0:
            CURSOR_CURRENT_INDEX = 0
            return
    for idx, item in enumerate(matches):
        if item.start() < CURSOR_CURRENT_INDEX <= item.end()-1:
            CURSOR_CURRENT_INDEX = item.start()
            return
        if item.start() == CURSOR_CURRENT_INDEX and idx > 0:
            CURSOR_CURRENT_INDEX = matches[idx - 1].start()
            return
    CURSOR_CURRENT_INDEX = 0


def move_to_end_of_current_word():
    """Advance to the first word end after the cursor."""
    global CURSOR_CURRENT_INDEX
    line = EDITOR_LINES[ACTIVE_LINE_INDEX]
    for match in re.finditer(r'\S+', line):
        if match.end() - 1 > CURSOR_CURRENT_INDEX:
            CURSOR_CURRENT_INDEX = match.end() - 1
            return
    CURSOR_CURRENT_INDEX = max(len(line) - 1, 0)


def insert_text_before_cursor(input_text):
    """
    Insert text before the current cursor position.
    Args:
        input_text (str): The text to insert.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    prefix = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
    suffix = EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX:]
    EDITOR_LINES[ACTIVE_LINE_INDEX] = prefix + input_text + suffix


def append_text_after_cursor(input_text):
    """
    Append text after the current cursor position.
    Args:
        input_text (str): The text to append.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    prefix = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX+1]
    suffix = EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX+1:]
    EDITOR_LINES[ACTIVE_LINE_INDEX] = prefix + input_text + suffix
    CURSOR_CURRENT_INDEX += len(input_text)


def insert_text_from_beginning(input_text):
    """
    Insert text at the beginning of the editor content.
    Args:
        input_text (str): The text to insert.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    EDITOR_LINES[ACTIVE_LINE_INDEX] = input_text + EDITOR_LINES[ACTIVE_LINE_INDEX]
    CURSOR_CURRENT_INDEX = 0


def append_text_at_end(input_text):
    """
    Append text at the end of the editor content.
    Args:
        input_text (str): The text to append.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    EDITOR_LINES[ACTIVE_LINE_INDEX] = EDITOR_LINES[ACTIVE_LINE_INDEX] + input_text
    CURSOR_CURRENT_INDEX = len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1


def delete_char_at_cursor():
    """
    Delete the character at the current cursor position.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    if not EDITOR_LINES[ACTIVE_LINE_INDEX]:
        return
    left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
    right = EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX + 1:]
    EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
    if not EDITOR_LINES[ACTIVE_LINE_INDEX]:
        CURSOR_CURRENT_INDEX = 0
    elif CURSOR_CURRENT_INDEX >= len(EDITOR_LINES[ACTIVE_LINE_INDEX]):
        CURSOR_CURRENT_INDEX = len(EDITOR_LINES[ACTIVE_LINE_INDEX]) - 1


def delete_char_before_cursor():
    """
    Delete the character before the current cursor position.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    if CURSOR_CURRENT_INDEX > 0 and EDITOR_LINES[ACTIVE_LINE_INDEX]:
        left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX-1]
        right = EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX:]
        EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
        CURSOR_CURRENT_INDEX -= 1


def view_editor_content():
    """Print the entire buffer without cursor markers."""
    print("\n".join(EDITOR_LINES))


def delete_to_start_of_next_word():
    """
    Delete from the current cursor position to the start of the next word.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    for item in matches:
        if item.start() > CURSOR_CURRENT_INDEX:
            left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
            right = EDITOR_LINES[ACTIVE_LINE_INDEX][item.start():]
            EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
            return
    # If no next word, delete to end of line
    left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
    EDITOR_LINES[ACTIVE_LINE_INDEX] = left


def delete_to_end_of_next_word():
    """
    Delete from the current cursor position to the end of the next word.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    for item in matches:
        if item.end()-1 > CURSOR_CURRENT_INDEX:
            left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
            right = EDITOR_LINES[ACTIVE_LINE_INDEX][item.end():]
            EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
            return
    # If no next word, delete to end of line
    left = EDITOR_LINES[ACTIVE_LINE_INDEX][:CURSOR_CURRENT_INDEX]
    EDITOR_LINES[ACTIVE_LINE_INDEX] = left


def delete_to_start_of_previous_word():
    """Delete back to the nearest word start strictly before the cursor."""
    global CURSOR_CURRENT_INDEX
    line = EDITOR_LINES[ACTIVE_LINE_INDEX]
    start = 0
    for match in re.finditer(r'\S+', line):
        if match.start() >= CURSOR_CURRENT_INDEX:
            break
        start = match.start()
    EDITOR_LINES[ACTIVE_LINE_INDEX] = line[:start] + line[CURSOR_CURRENT_INDEX + 1:]
    CURSOR_CURRENT_INDEX = start


def delete_current_word():
    """
    Delete the entire word at the current cursor position, including surrounding whitespaces.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    if not matches:
        EDITOR_LINES[ACTIVE_LINE_INDEX] = ""
        CURSOR_CURRENT_INDEX = 0
        return
    if CURSOR_CURRENT_INDEX < matches[0].start():
        # If cursor is before the first word, delete to beginning of line
        right = EDITOR_LINES[ACTIVE_LINE_INDEX][matches[0].start():]
        EDITOR_LINES[ACTIVE_LINE_INDEX] = right
        return
    if CURSOR_CURRENT_INDEX >= matches[-1].start():
        if EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX].isspace():
            # If cursor is on whitespace, delete the whitespace
            left = EDITOR_LINES[ACTIVE_LINE_INDEX][:matches[-1].end()]
            EDITOR_LINES[ACTIVE_LINE_INDEX] = left
            return
        left = EDITOR_LINES[ACTIVE_LINE_INDEX][:matches[-1].start()]
        right = EDITOR_LINES[ACTIVE_LINE_INDEX][matches[-1].end():]
        EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
        return
    for idx, item in enumerate(matches):
        if item.start() <= CURSOR_CURRENT_INDEX <= matches[idx+1].start()-1:
            if EDITOR_LINES[ACTIVE_LINE_INDEX][CURSOR_CURRENT_INDEX].isspace():
                # If cursor is on whitespace, delete the whitespace
                left = EDITOR_LINES[ACTIVE_LINE_INDEX][:item.end()]
                right = EDITOR_LINES[ACTIVE_LINE_INDEX][matches[idx+1].start():]
                EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
                return
            left = EDITOR_LINES[ACTIVE_LINE_INDEX][:item.start()]
            right = EDITOR_LINES[ACTIVE_LINE_INDEX][item.end():]
            EDITOR_LINES[ACTIVE_LINE_INDEX] = left + right
            return


def swap_word_at_cursor_with_next():
    """
    Swap the word at the current cursor position with the next word.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    for idx, item in enumerate(matches):
        if item.start() <= CURSOR_CURRENT_INDEX < item.end():
            if idx + 1 < len(matches):
                next_item = matches[idx + 1]
                left = EDITOR_LINES[ACTIVE_LINE_INDEX][:item.start()]
                middle = EDITOR_LINES[ACTIVE_LINE_INDEX][item.start():item.end()]
                blank = EDITOR_LINES[ACTIVE_LINE_INDEX][item.end():next_item.start()]
                next_middle = EDITOR_LINES[ACTIVE_LINE_INDEX][next_item.start():next_item.end()]
                right = EDITOR_LINES[ACTIVE_LINE_INDEX][next_item.end():]
                EDITOR_LINES[ACTIVE_LINE_INDEX] = left + next_middle + blank + middle + right
                CURSOR_CURRENT_INDEX += len(next_middle) + len(blank)
            return


def swap_word_at_cursor_with_previous():
    """
    Swap the word at the current cursor position with the previous word.
    """
    global EDITOR_LINES, CURSOR_CURRENT_INDEX, ACTIVE_LINE_INDEX
    matches = list(re.finditer(r'\S+', EDITOR_LINES[ACTIVE_LINE_INDEX]))
    for idx, item in enumerate(matches):
        if item.start() <= CURSOR_CURRENT_INDEX < item.end():
            if idx > 0:
                prev_item = matches[idx - 1]
                left = EDITOR_LINES[ACTIVE_LINE_INDEX][:prev_item.start()]
                prev_middle = EDITOR_LINES[ACTIVE_LINE_INDEX][prev_item.start():prev_item.end()]
                blank = EDITOR_LINES[ACTIVE_LINE_INDEX][prev_item.end():item.start()]
                middle = EDITOR_LINES[ACTIVE_LINE_INDEX][item.start():item.end()]
                right = EDITOR_LINES[ACTIVE_LINE_INDEX][item.end():]
                EDITOR_LINES[ACTIVE_LINE_INDEX] = left + middle + blank + prev_middle + right
                CURSOR_CURRENT_INDEX -= len(prev_middle) + len(blank)
            return


def toggle_line_cursor_on_and_off():
    """
    Toggle the line cursor on and off.
    """
    global LINE_CURSOR_ON
    LINE_CURSOR_ON = not LINE_CURSOR_ON


def move_cursor_up():
    global ACTIVE_LINE_INDEX
    if ACTIVE_LINE_INDEX > 0:
        ACTIVE_LINE_INDEX -= 1


def move_cursor_down():
    global ACTIVE_LINE_INDEX, EDITOR_LINES
    if ACTIVE_LINE_INDEX < len(EDITOR_LINES) - 1:
        ACTIVE_LINE_INDEX += 1


def insert_empty_line_below():
    global ACTIVE_LINE_INDEX, EDITOR_LINES
    EDITOR_LINES.insert(ACTIVE_LINE_INDEX + 1, "")
    ACTIVE_LINE_INDEX += 1


def insert_empty_line_above():
    global ACTIVE_LINE_INDEX, EDITOR_LINES
    EDITOR_LINES.insert(ACTIVE_LINE_INDEX, "")


def delete_line():
    global ACTIVE_LINE_INDEX, EDITOR_LINES, CURSOR_CURRENT_INDEX
    if len(EDITOR_LINES) > 1:
        del EDITOR_LINES[ACTIVE_LINE_INDEX]
        if ACTIVE_LINE_INDEX >= len(EDITOR_LINES):
            ACTIVE_LINE_INDEX = max(len(EDITOR_LINES) - 1, 0)
    else:
        # Keep one empty line when the last line is deleted.
        EDITOR_LINES[ACTIVE_LINE_INDEX] = ""
    CURSOR_CURRENT_INDEX = 0


def move_line_down():
    global ACTIVE_LINE_INDEX, EDITOR_LINES
    if ACTIVE_LINE_INDEX < len(EDITOR_LINES) - 1:
        EDITOR_LINES[ACTIVE_LINE_INDEX], EDITOR_LINES[ACTIVE_LINE_INDEX + 1] = EDITOR_LINES[ACTIVE_LINE_INDEX + 1], EDITOR_LINES[ACTIVE_LINE_INDEX]
        ACTIVE_LINE_INDEX += 1


def move_line_up():
    global ACTIVE_LINE_INDEX, EDITOR_LINES
    if ACTIVE_LINE_INDEX > 0:
        EDITOR_LINES[ACTIVE_LINE_INDEX], EDITOR_LINES[ACTIVE_LINE_INDEX - 1] = EDITOR_LINES[ACTIVE_LINE_INDEX - 1], EDITOR_LINES[ACTIVE_LINE_INDEX]
        ACTIVE_LINE_INDEX -= 1


def jump_to_line(line_number):
    global ACTIVE_LINE_INDEX, EDITOR_LINES, CURSOR_CURRENT_INDEX
    if 1 <= line_number <= len(EDITOR_LINES):
        ACTIVE_LINE_INDEX = line_number - 1
        CURSOR_CURRENT_INDEX = 0
    if line_number > len(EDITOR_LINES):
        ACTIVE_LINE_INDEX = len(EDITOR_LINES) - 1
        CURSOR_CURRENT_INDEX = 0


def validate_and_parse(raw_command):
    """
    Validate and parse the raw command input.
    Args:
        raw_command (str): The raw command string.
    Returns:
        tuple: (main_cmd, extra_data) if valid, else (None, None)
    """
    if not raw_command:
        return None, None
    main_cmd = raw_command[0]
    extra_data = raw_command[1:]
    if raw_command.isdecimal():
        try:
            line_number = int(raw_command)
        except ValueError:
            return None, None
        return (line_number, None) if line_number > 0 else (None, None)
    if main_cmd in "iIaA" and len(raw_command) < 2:
        return None, None
    if main_cmd in "hlwbexX$^?qv.;jkoOJK" and len(raw_command) != 1:
        return None, None
    if main_cmd not in "hlwbexX$^?qv.iIaAds;jkoOJK":
        return None, None
    if main_cmd == 'd' and raw_command[1:] not in ['w', 'e', 'b', 'c', 'd']:
        return None, None
    if main_cmd == 's' and raw_command[1:] not in ['w', 'b']:
        return None, None
    return main_cmd, extra_data


def execute_command(cmd, text):
    """
    Execute the given editor command.
    Args:
        cmd (str): The command character.
        text (str): Additional text for the command, if needed.
    """
    if cmd == 'h':
        move_cursor_left()
    elif cmd == 'l':
        move_cursor_right()
    elif cmd == 'w':
        move_to_next_word()
    elif cmd == 'i':
        insert_text_before_cursor(text)
    elif cmd == 'x':
        delete_char_at_cursor()
    elif cmd == '^':
        move_to_beginning_of_line()
    elif cmd == '$':
        move_to_end_of_line()
    elif cmd == 'b':
        move_to_previous_word()
    elif cmd == 'e':
        move_to_end_of_current_word()
    elif cmd == 'a':
        append_text_after_cursor(text)
    elif cmd == 'I':
        insert_text_from_beginning(text)
    elif cmd == 'A':
        append_text_at_end(text)
    elif cmd == 'X':
        delete_char_before_cursor()
    elif cmd == '.':
        toggle_row_cursor()
    elif cmd == 'd':
        if text == 'w':
            delete_to_start_of_next_word()
        if text == 'e':
            delete_to_end_of_next_word()
        if text == 'b':
            delete_to_start_of_previous_word()
        if text == 'c':
            delete_current_word()
        if text == 'd':
            delete_line()
    elif cmd == 's':
        if text == 'w':
            swap_word_at_cursor_with_next()
        if text == 'b':
            swap_word_at_cursor_with_previous()
    elif cmd == ';':
        toggle_line_cursor_on_and_off()
    elif cmd == 'k':
        move_cursor_down()
    elif cmd == 'j':
        move_cursor_up()
    elif cmd == 'o':
        insert_empty_line_below()
    elif cmd == 'O':
        insert_empty_line_above()
    elif cmd == 'K':
        move_line_down()
    elif cmd == 'J':
        move_line_up()
    elif isinstance(cmd, int):
        jump_to_line(cmd)
    clamp_cursor()


def run_main_loop():
    """
    Main loop to run the editor, processing user input commands.
    """
    while True:
        try:
            raw_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if raw_input == "q":
            break
        cmd, text = validate_and_parse(raw_input)
        if cmd is None:
            continue
        if cmd == "?":
            show_help_menu()
            continue
        if cmd == "v":
            view_editor_content()
            continue
        execute_command(cmd, text)
        render_editor_view()


if __name__ == "__main__":
    run_main_loop()
