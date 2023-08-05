"""
CPython 3.0 bytecode opcodes

This is used in scanner (bytecode disassembly) and parser (Python grammar).

This is a superset of Python 3.0's opcode.py with some opcodes that simplify
parsing and semantic interpretation.
"""

from copy import deepcopy

# These are used from outside this module
from xdis.bytecode import findlinestarts, findlabels

import xdis.opcodes.opcode_3x as opcode_3x

from xdis.opcodes.opcode_3x import fields2copy, rm_op

# FIXME: can we DRY this even more?

opmap = {}
opname = [''] * 256

cmp_op = list(opcode_3x.cmp_op)
hasconst = list(opcode_3x.hasconst)
hascompare = list(opcode_3x.hascompare)
hasfree = list(opcode_3x.hasfree)
hasjabs = list(opcode_3x.hasjabs)
hasjrel = list(opcode_3x.hasjrel)
haslocal = list(opcode_3x.haslocal)
hasname = list(opcode_3x.hasname)
hasnargs = list(opcode_3x.hasnargs)
hasvargs = list(opcode_3x.hasvargs)
opmap = deepcopy(opcode_3x.opmap)

for object in fields2copy:
    globals()[object] =  deepcopy(getattr(opcode_3x, object))

# These are in Python 3.2 but not in Python 3.1
rm_op('DUP_TOP_TWO', 5, locals())

def def_op(name, op):
    opname[op] = name
    opmap[name] = op

def_op('ROT_FOUR', 5)
def_op('DUP_TOPX', 99)
def_op('EXTENDED_ARG', 143)

def_op('SET_ADD', 17)
def_op('LIST_APPEND', 18)
def_op('JUMP_IF_FALSE', 111)
def_op('JUMP_IF_TRUE', 112)
# There are no opcodes to add or change.
# If there were, they'd be listed below.

rm_op('JUMP_IF_FALSE_OR_POP', 111, locals())
rm_op('JUMP_IF_TRUE_OR_POP',  112, locals())
rm_op('POP_JUMP_IF_FALSE',    114, locals())
rm_op('POP_JUMP_IF_TRUE',     115, locals())
rm_op('DELETE_DEREF',         138, locals())
rm_op('SETUP_WITH',           143, locals())
rm_op('MAP_ADD',              147, locals())

def updateGlobal():
    # JUMP_OPs are used in verification are set in the scanner
    # and used in the parser grammar
    globals().update({'python_version': 3.0})
    globals().update(dict([(k.replace('+', '_'), v) for (k, v) in opmap.items()]))
    globals().update({'JUMP_OPs': map(lambda op: opname[op], hasjrel + hasjabs)})

updateGlobal()

from xdis import PYTHON_VERSION
if PYTHON_VERSION == 3.0:
    import dis
    # print(set(dis.opmap.items()) - set(opmap.items()))
    # print(set(opmap.items()) - set(dis.opmap.items()))

    assert all(item in dis.opmap.items() for item in opmap.items())
    assert all(item in opmap.items() for item in dis.opmap.items())

# opcode_30.dump_opcodes(opmap)
