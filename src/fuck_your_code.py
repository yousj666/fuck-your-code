#!/usr/bin/env python3
"""Fuck Your Code -- a shitty-code detector with a foul mouth.

This file is only a launcher shim: the real implementation lives
in the fyc package next to it, split into small modules so the
tool can pass its own inspection. Run with --help for usage.
"""

import sys

from fyc.cli import main

if __name__ == "__main__":
    sys.exit(main())
