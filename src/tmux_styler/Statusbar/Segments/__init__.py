from ...ContextVars import *

DefinedSegment = str | ContextVar | list[str | ContextVar]
"""
A segment is a part of the statusbar that displays some content. It is simply a python 
function that returns a "DefinedSegment" type. A segment can display a string, a ContextVar, 
or a list of strings and/or ContextVars that will get joined together.
"""

# TODO: Find a better way to do this, dynamic generation via CI?
# Default/included segments, format "segment_name": "module_name"
DEFAULT_SEGMENTS = {
    "window_info": "TmuxInfo",
    "session_name": "TmuxInfo",
    "cwd": "TmuxInfo",
    "date_day": "DateTime",
    "date": "DateTime",
    "time": "DateTime",
}
