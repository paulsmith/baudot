import sys
from enum import Enum
from itertools import cycle, chain

class Shift(Enum):
    FIGURES = 0x1B
    LETTERS = 0x1F

f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin

letters = {}
figures = {}

for line in f:
    if not line.startswith('#'):
        code, letter_shift, figure_shift = line.rstrip('\n').split('\t')
        number = 0
        for i, bit in enumerate(reversed(code)):
            if bit == '1':
                number |= 1 << i
        if letter_shift.startswith('\\'):
            letter_shift = bytes(letter_shift, 'utf-8').decode('unicode_escape')
        if figure_shift.startswith('\\'):
            figure_shift = bytes(figure_shift, 'utf-8').decode('unicode_escape')
        if letter_shift == 'FIGS':
            letter_shift = figure_shift = Shift.FIGURES
        if letter_shift == 'LTRS':
            letter_shift = figure_shift = Shift.LETTERS
        letters[number] = letter_shift
        figures[number] = figure_shift

escaped_control_chars = {'\0': '\\0', '\a': '\\a', '\n': '\\n', '\r': '\\r'}

def fmt_char(char):
    if char in escaped_control_chars:
        return "'" + escaped_control_chars[char] + "'"
    elif ord(char) < 0x20:
        return '0x{:02x}'.format(ord(char))
    else:
        if char == "'":
            return "'\\''"
        else:
            return "'" + char + "'"
        
def c_include_ita2_to_ascii(var_name, chars):
    print('unsigned char {}[{}] = {{'.format(var_name, len(chars)))
    l = len(chars)-1
    row_entry = 0
    for i, (n, char) in enumerate(chars.items()):
        if char == Shift.FIGURES or char == Shift.LETTERS:
            l = l-1
            continue
        print('\t[0x{:02x}] = {}'.format(n, fmt_char(char)), end='')
        if i < l:
            sys.stdout.write(',')
        if row_entry > 3:
            print()
            row_entry = 0
        else:
            row_entry += 1
    print('};')

def c_include_ascii_to_ita2():
    print('ITA2Char ita2_ascii[128] = {')
    chars = chain(
        zip(cycle([Shift.FIGURES]), figures.items()),
        zip(cycle([Shift.LETTERS]), letters.items()),
    )
    row_entry = 0
    for i, (shift, (n, char)) in enumerate(chars):
        if char == Shift.FIGURES or char == Shift.LETTERS:
            continue
        shift = 'LTRS' if shift == Shift.LETTERS else 'FIGS'
        print('\t[{}] = {{{}, {}}}'.format(fmt_char(char), fmt_char(chr(n)), shift), end='')
        if i < 62:
            sys.stdout.write(',')
        if row_entry == 2:
            print()
            row_entry = 0
        else:
            row_entry += 1
    print('};')

if __name__ == '__main__':
    c_include_ita2_to_ascii('ita2_ltrs2ascii', letters)
    print()
    c_include_ita2_to_ascii('ita2_figs2ascii', figures)
    print()
    c_include_ascii_to_ita2()
