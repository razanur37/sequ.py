#!/bin/bash
# Copyright (C) 2013 by Casey English

from sequ_roman import *
from sequ_format import *

# Number each line of the file, then print the line
def number_print(start, step, f, format_word, pad_char, max_width, format_options, separator, format_string):
    i = start
    for line in f:
        num = i

        if 'roman' in format_word:
            num = int_to_roman(i).lower()
        elif 'ROMAN' in format_word:
            num = int_to_roman(i)

        padding = pad_char * (max_width - length_getter(format_string.format(num)))

        if  '-' in format_string.format(i):
            sign = '-'
            abs_i = abs(i)
        else:
            sign = ''
            abs_i = i


        final_string = format_options['prefix']
        if 'roman' in format_word.lower():
            final_string += format_string.format(num)
        elif 'alpha' in format_word.lower():
            num = chr(num)
            final_string += format_string.format(num)
        else:
            final_string += format_string.format(abs_i)
        final_string += format_options['postfix']
        print(padding + sign + final_string + separator + line.rstrip())
        i += step
