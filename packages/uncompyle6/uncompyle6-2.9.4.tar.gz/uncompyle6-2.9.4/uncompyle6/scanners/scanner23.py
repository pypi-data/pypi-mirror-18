#  Copyright (c) 2016 by Rocky Bernstein
"""
Python 2.3 bytecode scanner/deparser

This overlaps Python's 2.3's dis module, but it can be run from
Python 3 and other versions of Python. Also, we save token
information for later use in deparsing.
"""

import uncompyle6.scanners.scanner24 as scan

# bytecode verification, verify(), uses JUMP_OPs from here
from xdis.opcodes import opcode_23
JUMP_OPs = opcode_23.JUMP_OPs

# We base this off of 2.5 instead of the other way around
# because we cleaned things up this way.
# The history is that 2.7 support is the cleanest,
# then from that we got 2.6 and so on.
class Scanner23(scan.Scanner24):
    def __init__(self, show_asm):
        scan.Scanner24.__init__(self, show_asm)
        self.opc = opcode_23
        self.opname = opcode_23.opname
        # These are the only differences in initialization between
        # 2.3-2.6
        self.version = 2.3
        self.genexpr_name = '<generator expression>';
        return
