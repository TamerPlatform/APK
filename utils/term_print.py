#!/usr/bin/env python
""" Just a module to print colorful messages on terminal.
"""

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def print_success(msg):
    print OKGREEN + msg + ENDC

def print_err(msg):
    print FAIL + msg + ENDC

def print_warning(msg):
    print WARNING + msg + ENDC