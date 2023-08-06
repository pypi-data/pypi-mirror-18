from ctypes import CDLL, get_errno, c_ushort, Structure, pointer
from ctypes.util import find_library

from enum import Enum
from os import strerror
from sys import platform

# The following enums are derived from #define's in sys/rtprio.h
class rtprio_func(Enum):
	RTP_LOOKUP = 0
	RTP_SET = 1

class rtprio_prio(Enum):
	RTP_PRIO_MIN = 0
	RTP_PRIO_MAX = 31

class rtprio_types(Enum):
	RTP_PRIO_REALTIME = 2
	RTP_PRIO_NORMAL = 3
	RTP_PRIO_IDLE = 4

# Third param to rtprio(2)
class rtprio_info(Structure):
	_fields_ = [("type", c_ushort), ("prio", c_ushort)]

# Load whichever libc is available on the system
libc = find_library('c')

if libc is not None:
	libc = CDLL(libc, use_errno=True)

def rtprio(type = rtprio_types.RTP_PRIO_REALTIME, prio = None, pid = 0):
	"""
	rtprio(2) interface that returns a tuple describing the priority of pid following this call.

	If prio is None, an rtprio(2) lookup is done and type does not matter.

	Keyword arguments:
	type -- The type of priority to set, if applicable (default: rtprio_types.RTP_PRIO_REALTIME)
	prio -- The magnitude of the priority to set, if setting a priority, between rtprio_prio.RTP_PRIO_{MIN,MAX} (default: None)
	pid -- The pid to inspect/set priority for, or 0 for 'current thread'. (Default: 0)
	"""
	if not hasattr(libc, 'rtprio'):
		raise NotImplementedError("rtprio(2) is not implemented for '{}'".format(platform))

	func = rtprio_func.RTP_LOOKUP

	if prio is None:
		prio = 0
	else:
		func = rtprio_func.RTP_SET
		if isinstance(prio, rtprio_prio):
			prio = prio.value
	
	info = rtprio_info(type.value, prio)
	ret = libc.rtprio(func.value, pid, pointer(info))

	if ret != 0:
		raise OSError(get_errno(), strerror(get_errno()))

	return (rtprio_types(info.type), info.prio)
