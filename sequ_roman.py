#!/usr/bin/python3
# Copyright (C) 2013 by Casey English
# Taken from http://code.activestate.com/recipes/81611-roman-numerals/

from sequ_error import *

# Converts an integer to a roman numeral
def int_to_roman(input):
    try:
        if type(input) != type(1):
            raise FormatError("expected integer, got %s" % type(input))
        if not 0 < input < 4000:
            raise FormatError("argument must be between 1 and 3999")
    except FormatError as e:
        print("sequ: " + e.message + " for type 'roman'")
        exit(1)
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = ""
    for i in range(len(ints)):
        count = int(input / ints[i])
        result += nums[i] * count
        input -= ints[i] * count
    return result


# Converts roman numerals to integers
def roman_to_int(input):
    try:
        if type(input) != type(""):
            raise FormatError("expected string, got %s" % type(input))
    except FormatError as e:
        print("sequ: " + e.message + " for type 'roman'")
        exit(1)
    input = input.upper()
    nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    ints = [1000, 500, 100, 50,  10,  5,   1]
    places = []
    for c in input:
        try:
            if not c in nums:
                raise FormatError('argument %s is not valid' % input)
        except FormatError as e:
            print("sequ: " + e.message + " for type 'roman'")
            exit(1)
    for i in range(len(input)):
        c = input[i]
        value = ints[nums.index(c)]
        # If the next place holds a larger number, this value is negative.
        try:
            nextvalue = ints[nums.index(input[i +1])]
            if nextvalue > value:
                value *= -1
        except IndexError:
            # there is no next place.
            pass
        places.append(value)
    sum = 0
    for n in places: sum += n
    # Easiest test for validity...
    try:
        if int_to_roman(sum) == input:
            return sum
        else:
            raise FormatError('argument %s is not valid' % input)
    except FormatError as e:
        print("sequ: " + e.message + " for type 'roman'")
        exit(1)
