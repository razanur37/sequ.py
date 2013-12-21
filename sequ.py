#!/usr/bin/python3
# Copyright (C) 2013 by Casey English

# sequ command. An extension of the 'seq' command from the GNU Coreutils.
# Currently implementing CL1 meaning the command will function identically
# to GNU seq

# Import the exit command from the sys module so that we can define our
# exit state.
# Import the argparse module to support more robust argument handling.
# Import the re module for regular expression parsing.
from sys import exit
import argparse
from os import linesep
from sequ_error import *
from sequ_format import *
from sequ_roman import *
from sequ_number_lines import *

# Define a version of range() that will accept floats
# http://www.stackoverflow.com/questions/7567556/range-for-floats
def frange(x, y, jump):
    if jump < 0:
        while x > y:
            yield x
            x+= jump
    else:
        while x < y:
            yield x
            x += jump

# Populate the help dictionary
help_strings = {}
f = open('help_strings.txt')
for line in f:
    line = line.split(' = ', 1)
    name = line[0]
    value = line[1].rstrip('\n')
    help_strings[name] = value
f.close()

help_strings['post_help'] = help_strings['post_help'].replace(' linesep ', linesep)

# Define the arguments the command will accept, along with help lines.
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=help_strings['sequ_description'],
    epilog=help_strings['post_help'])

parser.add_argument(
    '-F', '--format-word',
    nargs=1,
    default='',
    choices=['arabic', 'float', 'roman', 'ROMAN', 'alpha', 'ALPHA'],
    help=help_strings['format_word_help'])

parser.add_argument(
    '-n', '--number-lines',
    nargs=1,
    default='',
    help=help_strings['number_lines_help'])

format_group = parser.add_mutually_exclusive_group()
format_group.add_argument(
    '-f', '--format',
    help=help_strings['format_help'])
format_group.add_argument(
    '-p', '--pad',
    default='',
    help=help_strings['pad_help'])
format_group.add_argument(
    '-P', '--pad-spaces',
    action='store_true',
    help=help_strings['pad_spaces_help'])
format_group.add_argument(
    '-w', '--equal-width',
    action='store_true',
    help=help_strings['equal_width_help'])

separator_group = parser.add_mutually_exclusive_group()
separator_group.add_argument(
    '-s', '--separator',
    default='',
    help=help_strings['separator_help'])
separator_group.add_argument(
    '-W', '--words',
    action='store_true',
    help=help_strings['words_help'])

parser.add_argument(
    'numbers',
    metavar='[NUMBER]',
    nargs='+',
    help=help_strings['numbers_help'])

# By default, if the parse_args() method encoutners an error with the argument
# list, it will exit with status code '2'. According to the sequ specification,
# all errors must exit with a status code of '1', so run a try block that will
# catch if parse_args() tries to exit and force an exit status code of '1'.
try:
    args = parser.parse_args()
except SystemExit:
    exit(1)

if args.number_lines:
    number_line_file = args.number_lines[0]
else:
    number_line_file = False

# Try to open the file we were given
if number_line_file:
    try:
        f = open(number_line_file)
    except FileNotFoundError:
        print("sequ: No such file '%s'" % number_line_file)
        exit(1)

# Check the pad string to make sure it is only one character long
try:
    if len(args.pad) > 1:
        raise FormatError(args.pad)
except FormatError as e:
    print("sequ: pad string '" + e.message + "' is more than one character long")
    exit(1)

numbers = args.numbers

# If we weren't given a format-word, we have to infer it from the end argument.
# Throw an error if the end argument is not a recognized type.
if (args.format_word):
    format_word = args.format_word[0]
else:
    try:
        if float(numbers[-1]).is_integer():
            format_word = 'float'
        else:
            format_word = 'float'
    except ValueError:
        if numbers[-1].isalpha() and numbers[-1].isupper():
            format_word = 'ALPHA'
        elif numbers[-1].isalpha():
            format_word = 'alpha'
        else:
            print("sequ: Argument '" + str(numbers[-1]) + "' is not a valid type")
            exit(1)

# Try to convert everything to a number if we have a number format-word
if 'arabic' in format_word or 'float' in format_word or 'roman' in format_word.lower():
    try:
        for i in range(len(numbers)):
            numbers[i] = float(numbers[i])
    except ValueError:
        pass

# Check to see if too many numbers were entered.
try:
    if len(numbers) > 3:
        raise Error(str(numbers[3:]))
    elif number_line_file and len(numbers) > 2:
        raise Error(str(numbers[2:]))
except Error as e:
    print("sequ: extra operand(s) '" + e.expression + "'")
    exit(1)

# Check the list to make sure it is consistent with the format-word type we
# were given. If all the numbers are integers and were weren't explicitly told
# to use floats, convert everything to be an int.
if 'arabic' in format_word or 'float' in format_word or 'roman' in format_word.lower():
    ints = 0
    for i in range(len(numbers)):
        try:
            if float(numbers[i]).is_integer():
                ints += 1
            elif 'arabic' in format_word or 'roman' in format_word.lower():
                raise FormatError(str(numbers[i]))
        except ValueError:
            if not 'roman' in format_word.lower():
                print("sequ: argument '%(1)s' is not valid for type '%(2)s'" % {'1': numbers[i], '2': format_word})
                exit(1)
            numbers[i] = roman_to_int(numbers[i])
            ints += 1
            continue
        except FormatError as e:
            print("sequ: Argument '" + e.message + "' does not match type '" + format_word + "'")
            exit(1)
    if 'float' not in args.format_word and ints==len(numbers):
        all_ints = True
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
    else:
        all_ints = False
else:
    all_ints = True

# If the FIRST or INTERVAL weren't supplied, edit the list to add their default
# values of 1/a. If we're in line-numbering mode, only add an interval.
if number_line_file:
    if len(numbers) < 2:
        numbers.append(numbers[0])
        numbers[1] = 1
else:
    if len(numbers) <= 2:
        if len(numbers) == 1:
            numbers.append(numbers[0])
            if 'alpha' in format_word.lower():
                numbers[0] = 'a'
            else:
                numbers[0] = 1
        numbers.append(numbers[1])
        numbers[1] = 1

# Try to parse the string passed for the format flag.
# If the user wants hexadecimal output, convert everything in numbers to ints,
# if they aren't already
try:
    if args.format:
        if 'roman' in format_word.lower() or 'alpha' in format_word.lower():
            print("sequ: cannot use --format (-f) flag with --format-word (-F) type '" + format_word + "'")
            exit(1)
        format_set = True
        format_options = formatter(args.format)
        parsed_flags = flag_parser(format_options['flags'])
        if 'x' in format_options['specifier'].lower() and not all_ints:
            for i in range(3):
                numbers[i] = int(numbers[i])
            numbers[1] += 1
            all_ints = True
    else:
        format_set = False
        format_options = {}
        format_options['prefix'] = ''
        format_options['postfix'] = ''

except FormatError as e:
    print('sequ: ' + e.message)
    exit(1)

# If the equal-width flag was set, get the length of the ending number and
# use it as the width in the format specification
# Otherwise, pull together the format specification from the parsed
# format string
# In Python, zero-padding and left-justification work together, though in a
# wierd way. In printf() left-justification takes precedence. So check to
# see if left-justification is set before adding in zero-padding
format_string = '{:'
if format_set:
    format_string += parsed_flags['justify_flag']
    format_string += parsed_flags['sign_flag']
    format_string += parsed_flags['force_decimal_point_flag']
    if '<' not in parsed_flags['justify_flag']:
        format_string += parsed_flags['zero_padding_flag']
    format_string += format_options['width']
    format_string += '.'
    format_string += format_options['precision']
    format_string += format_options['specifier']
elif not all_ints:
    format_string += '.'
    precision = max(precision_getter(numbers[0]), precision_getter(numbers[1]))
    format_string += str(precision)
    format_string += 'f'
format_string += '}'

if args.pad or args.pad_spaces or args.equal_width or number_line_file:
    pad = True
else:
    pad = False

start = numbers[0]
step = numbers[1]
if not number_line_file:
    end = numbers[2]

# Make sure everything is a letter if we're in alpha mode.
if 'alpha' in format_word.lower():
    try:
        if not start.isalpha():
            raise FormatError("sequ: Argument '" + start + "' does not match type '" + format_word + "'")
        elif not number_line_file and not end.isalpha():
            raise FormatError("sequ: Argument '" + end + "' does not match type '" + format_word + "'")
        if len(start) > 1 or (not number_line_file and len(end) > 1):
            raise FormatError("sequ: can only use single characters with format-word %s" % format_word)
        if not float(step).is_integer():
            raise FormatError("sequ: Increment must be an integer with format-word %s" % format_word)
        step = int(step)
    except FormatError as e:
        print(e.message)
        exit(1)

# Make sure we're not going to go out of bounds if we're in roman mode.
if 'roman' in format_word.lower():
    try:
        int_to_roman(start)
        if not number_line_file:
            int_to_roman(end)
    except FormatError as e:
        print(e.message)
        exit(1)

# Figure out the longest number and store it's max width for padding use.
if pad and not number_line_file:
    if 'roman' in format_word.lower():
        max_width = 0
        if step < 0:
            end_increment = -1
        else:
            end_increment = 1
        for i in frange(start, end+end_increment, step):
            num = int_to_roman(i)
            width = len(num)
            if width > max_width:
                max_width = width
    elif start != end:
        max_width = max(
            length_getter(format_string.format(start)),
            length_getter(format_string.format(end)),
            length_getter(format_string.format(end-step)))
    else:
        max_width = length_getter(format_string.format(start))
else:
    max_width = 0

# If we're numbering a file, check to make sure we won't go out of bounds in
# case we're in alpha or roman mode, also get the max width for padding use.
if number_line_file:
    max_width = 0
    if 'alpha' in format_word.lower():
        i = ord(start)
        num = start
    else:
        i = start
    for line in f:
        if 'alpha' in format_word.lower() and ((not ord('a') < i < ord('z')) or (not ord('A') < i < ord('Z'))):
            print("sequ: file '%s' is too large for format "% number_line_file + format_word)
            exit(1)
        if 'roman' in format_word.lower():
            num = int_to_roman(i)
            width = len(num)
        else:
            width = length_getter(format_string.format(i))
        if width > max_width:
            max_width = width
        i += step
    f.seek(0)

if args.words:
    separator = ' '
elif number_line_file and not args.separator:
    separator = ' '
elif not args.separator:
    separator = '\n'
else:
    separator = args.separator

# Check to see if the step is negative and then print the sequence. Since
# frange() stops one step short of the second argument, increment (or decrement)
# it by 1 to compensate.
# Before printing, pull together the final string to be printed by
# combining the prefix with the formated number with the postfix

if args.pad_spaces:
    pad_char = ' '
elif args.equal_width:
    pad_char = '0'
elif number_line_file and not args.pad:
    pad_char = ' '
else:
    pad_char = args.pad

# Convert the bounds to their ASCII codes so we can loop over them.
if 'alpha' in format_word:
    start = ord(start.lower())
    if not number_line_file:
        end = ord(end.lower())
elif 'ALPHA' in format_word:
    start = ord(start.upper())
    if not number_line_file:
        end = ord(end.upper())

# If we're numbering a file, pass the needed values off to another function to
# print the lines for us.
if number_line_file:
    number_print(start, step, f, format_word, pad_char, max_width, format_options, separator, format_string)
    exit(0)

# Otherwise start printing the numbers
if step < 0:
    if all_ints or 'float' in args.format_word:
        end_increment = -1
    elif not number_line_file and end < 0:
        end_increment = 0
    else:
        end_increment = step
    
    for i in frange(start, end+end_increment, step):
        
        num = i
        
        if 'roman' in format_word:
            num = int_to_roman(i).lower()
        elif 'ROMAN' in format_word:
            num = int_to_roman(i)

        if pad:
            padding = pad_char * (max_width - length_getter(format_string.format(num)))
        else:
            padding = ''

        if  '-' in format_string.format(i):
            sign = '-'
            i = abs(i)
        else:
            sign = ''

        final_string = format_options['prefix']
        if 'roman' in format_word.lower():
            final_string += format_string.format(num)
        elif 'alpha' in format_word.lower():
            num = chr(num)
            final_string += format_string.format(num)
        else:
            final_string += format_string.format(i)
        final_string += format_options['postfix']

        if i+step <= end+end_increment:
            print(sign + padding + final_string)
        else:
            print(sign + padding + final_string, end=separator)
else:
    for i in frange(start, end+1, step):
        if i > end:
            continue

        num = i

        if 'roman' in format_word:
            num = int_to_roman(i).lower()
        elif 'ROMAN' in format_word:
            num = int_to_roman(i)

        if pad:
            padding = pad_char * (max_width - length_getter(format_string.format(num)))
        else:
            padding = ''

        if  '-' in format_string.format(i):
            sign = '-'
            i = abs(i)
        else:
            sign = ''

        final_string = format_options['prefix']
        if 'roman' in format_word.lower():
            final_string += format_string.format(num)
        elif 'alpha' in format_word.lower():
            num = chr(num)
            final_string += format_string.format(num)
        else:
            final_string += format_string.format(i)
        final_string += format_options['postfix']

        if i+step >= end+1:
            print(sign + padding + final_string)
        else:
            print(sign + padding + final_string, end=separator)
