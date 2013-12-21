#!/usr/bin/python3
# Copyright (C) 2013 by Casey English

import re
from sequ_error import *

# This function parses the format options string and returns the
# options as a dictionary object. At each stage of the parsing,
# the function takes a regular expression and compares it to the string,
# if there is a match, the matching part of the string is split off
# and stored in the dictionary, if there is not a match (meaning the
# user didn't enable that option) set a default, usually the empty string.
def formatter(input_string):

    format_options = {}

    working_string = input_string
    prefix = ''

# Make sure the string contains the necessary %, and store any prefix
    if not re.match('%', working_string):
        percent_re = re.search('%', working_string)
        if not percent_re:
            raise FormatError("format '" + working_string + "' has no % directive")
        else:
            prefix = working_string[:percent_re.start()]
        working_string = working_string[percent_re.start():]

    format_options['prefix'] = prefix

    working_string = working_string[1:]

# Check for (and store) any flags (as defined in the printf() spec)
# If there are none, store the empty string
    flag_string = re.match('[-+#0 ]*', working_string).group()
    if flag_string:
        working_string = working_string[len(flag_string):]
    else:
        flag_string = ''
    format_options['flags'] = flag_string

# Check for (and store) a width specifier
# Store 0 if there isn't one
# Note this is stored as a string because format() uses a string for
# it's format specifier
    width = re.match('\d*', working_string).group()
    if width:
        working_string = working_string[len(width):]
    else:
        width = '0'

    format_options['width'] = width

# Check for (and store) a precision specifier
# If they entered a '.' but no value, store 0 as a default
# Otherwise store 6 (the default used by both Python and printf())
    if re.match('[.]', working_string):
        working_string = working_string[1:]

        precision_re = re.match('\d+', working_string)

        if precision_re:
            precision = precision_re.group()
            working_string = working_string[len(precision):]
        else:
            precision = '0'
    else:
        precision = '6'

    format_options['precision'] = precision

# If there's no more string left, they didn't give a specifier,
# so throw the error
    if not working_string:
        raise FormatError("format '" + input_string + "' ends in %")

# Try to find the specifier
# Note that in Python differs from printf() in that Python uses the
# x and X flags to denote hex output instead of the a and A flags
# If the specifier doesn't match, throw an error
    if re.match('[aefgAEFG]', working_string):
        specifier = working_string[0]
        working_string = working_string[1:]
        format_options['specifier'] = specifier
        if 'a' in format_options['specifier']:
            format_options['specifier'] = 'x'
        elif 'A' in format_options['specifier']:
            format_options['specifier'] = 'X'
    else:
        raise FormatError("format '" + input_string + "' has unknown %" + working_string[0] + " directive")

# If there's still some string left, store it as a postfix
    if working_string:
        format_options['postfix'] = working_string
    else:
        format_options['postfix'] = ''

    return format_options

# This function parses the string of flags from the format string (flags
# being defined as any characters from the set [-+#0 ] that preceed the
# width value in the format string), and returns a dictionary of format
# options that are recognized by Python's format() method.
def flag_parser(input_flags):
    parsed_flags = {}
    
    if re.search('-', input_flags):
        parsed_flags['justify_flag'] = '<'
    else:
        parsed_flags['justify_flag'] = ''

    if re.search(' ', input_flags):
        parsed_flags['sign_flag'] = ' '
    else:
        parsed_flags['sign_flag'] = ''

    if re.search('#', input_flags):
        parsed_flags['force_decimal_point_flag'] = '#'
    else:
        parsed_flags['force_decimal_point_flag'] = ''

    if re.search('0', input_flags):
        parsed_flags['zero_padding_flag'] = '0'
    else:
        parsed_flags['zero_padding_flag'] = ''

    if re.search('[+]', input_flags):
        parsed_flags['sign_flag'] = '+'
    else:
        parsed_flags['sign_flag'] = ''

    return parsed_flags

# This function takes a number, converts it to a float (in case the number
# passed was in scientific notation or was an int), chops off the decimal point
# and everything to the left of it, then finds how many digits are in the new
# number. This is returned as the precision of that number.
def precision_getter(input_number):
    if 'e' in str(input_number):
        exponent = str(input_number).split('e')[1]
        exponent = int(exponent)
        exponent = abs(exponent)
        format_string = '{:.' + str(exponent) + 'f}'
        input_number = format_string.format(input_number)
    else:
        input_number = float(input_number)
    number_post_decimal = str(input_number).split('.')[1]
    precision = len(number_post_decimal)

    return precision

# This function takes a number, converts it to a string, and returns the length
# of that string.
def length_getter(input_number):
    
    length = len(str(input_number))

    return length
