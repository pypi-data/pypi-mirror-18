from __future__ import absolute_import, unicode_literals

from ctypes import CDLL, get_errno, Structure, POINTER, pointer, c_ushort, c_int, c_int32
from ctypes.util import find_library

from os import strerror
from sys import platform

# Derived from #define's in sys/rtprio.h
priorities = list(range(0, 32))

functions = {
    "lookup": 0,
    "set" : 1,
}

types = {
    "realtime": 2,
    "normal": 3,
    "idle": 4,
}

# Third param to rtprio(2)
class rtprio_info(Structure):
    _fields_ = [("type", c_ushort), ("prio", c_ushort)]

def rtprio_exists():
    return hasattr(libc, 'rtprio')

# Load whichever libc is available on the system
libc = find_library('c')

if libc is not None:
    libc = CDLL(libc, use_errno=True)

    if rtprio_exists():
        libc.rtprio.argtypes = [c_int, c_int32, POINTER(rtprio_info)]

def rtprio(priotype=types['realtime'], prio=None, pid=0):
    """
    rtprio(2) interface that returns a tuple describing the priority of pid following this call.

    If prio is None, an rtprio(2) lookup is done and type does not matter.

    Keyword arguments:
    priotype -- The type of priority to set, if applicable (default: 'realtime', options: 'realtime', 'normal', 'idle')
    prio -- The magnitude of the priority to set, if setting a priority, in interval [1,31]
    pid -- The pid to inspect/set priority for, or 0 for 'current thread'. (Default: 0)
    """
    if not rtprio_exists():
        raise NotImplementedError("rtprio(2) is not implemented for '{}'".format(platform))

    if priotype in types.keys():
        priotype = types[type]
    elif priotype not in types.values():
        raise ValueError('Invalid type ({}) passed in', priotype)

    func = 'lookup'

    if prio is None:
        prio = 0
    else:
        func = 'set'

        if prio not in priorities:
            raise ValueError('prio not in valid range [0,31]')

    func_value = functions[func]
    info = rtprio_info(priotype, prio)
    ret = libc.rtprio(func_value, pid, pointer(info))

    if ret != 0:
        raise OSError(get_errno(), strerror(get_errno()))

    return (list(types.keys())[list(types.values()).index(info.type)], info.prio)
