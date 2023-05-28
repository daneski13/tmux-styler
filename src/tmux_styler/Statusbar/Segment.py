from enum import Enum

from ..Colors import Color, NamedColor
from ..Style import Style


class SegmentType(Enum):
    """
    The type of segment.
    """
    FUNCTION = "function"
    """
    A segment that is a function and must be loaded from a module.
    """
    STRING = "str"
    """
    A segment that simply displays a static string.
    """


class Segment:
    """
    A segment is a part of the statusbar that displays some content.
    """

    def __init__(self, segment_type: SegmentType, content: str, bg: Color = NamedColor.DEFAULT, fg: Color = NamedColor.DEFAULT, separator: str | None = None, style: Style | None = None):
        """
        Creates a Segment object.

        Parameters:
        -----------
        `segment_type`: SegmentType
            The type of segment.

        `content`: str
            The content of the segment, if the segment type is a string than this is the string to display.
            If the segment type is a function, then this is the function name. If the the function is
            user defined then it must be in the format of {module}.{function name}. The module must be
            in a path that tmux-styler will search for segments, or in your python path.

        `bg`: Color
            The background color of the segment. By default this will fallback to the default background color.

        `fg`: Color
            The foreground color of the segment. By default this will fallback to the default foreground color.

        `separator`: str | None
            Optionally specify a separator to use between this segment and the next segment, overrides the default separator.

        `style`: Style
            The style of the segment (optional). Specifying a style object that has colors will override the bg and fg parameters
            with the colors from the style object.
        """
        self.type = segment_type
        self.content = content
        self.bg = bg
        self.fg = fg
        self.separator = separator

        if style is not None and style.bg is not None:
            self.bg = style.bg
        if style is not None and style.fg is not None:
            self.fg = style.fg
        self.style = style
