from . import DefinedSegment
from ...ContextVars import ContextVar


def window_info() -> DefinedSegment:
    """
    Segment that displays window information, the window index, flags, and name.
    """
    return [ContextVar.WINDOW_INDEX, ContextVar.WINDOW_FLAGS, " | ", ContextVar.WINDOW_NAME]


def session_name() -> DefinedSegment:
    """
    The name of the current session.
    """
    return [ContextVar.SESSION_NAME]


def cwd(max_length: int = 30) -> DefinedSegment:
    """
    The current/present working directory.

    Parameters:
    -----------
    `max_length` (int):
        The maximum length of the path. Defaults to 30.
    """
    path = ContextVar.PANE_CURRENT_PATH.current_value()[1:-1]
    if len(path) > max_length:
        path = path[-max_length+3:]
        index = path.find("/")
        if index != -1:
            path = "..." + path[index:]
        else:
            path = "..." + path

    return path
