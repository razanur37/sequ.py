#!/usr/bin/python3
# Copyright (C) 2013 by Casey English

# sequ specific error types

class Error(Exception):
    def __init__(self, expression):
        self.expression = expression

class FormatError(Error):
    def __init__(self, message):
        self.message = message
