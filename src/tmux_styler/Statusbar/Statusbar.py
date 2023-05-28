from enum import Enum
from typing import Any, Dict
import pickle

from .WindowList import WindowList
from ..Style import *
from ..Colors import *
from ..ContextVars import *
from .Segment import Segment


class SegmentSeparator:
    """
    A segment separator is a character that is displayed between segments.

    Attributes:
    -----------
    `left_thick`: str
        The left thick separator, used for separating between segments.

    `right_thick`: str
        The right thick separator, used for separating between segments.

    `left_thin`: str
        The left thin separator, used for separating between segments of the same background color.

    `right_thin`: str
        The right thin separator, used for separating between segments of the same background color.
    """

    def __init__(self, right_thick: str, left_thick: str, right_thin: str, left_thin: str):
        """
        Creates a SegmentSeparator object.

        Parameters:
        -----------
        `right_thick`: str
            The "pointing" right thick separator, used for separating between segments.

        `left_thick`: str
            The "pointing" left thick separator, used for separating between segments.

        `right_thin`: str
            The "pointing" right thin separator, used for separating between segments of the same background color.

        `left_thin`: str
            The "pointing" left thin separator, used for separating between segments of the same background color.
        """

        self.right_thick = right_thick
        self.left_thick = left_thick
        self.right_thin = right_thin
        self.left_thin = left_thin


class Separators(Enum):
    """
    Segment separators using nerd font's extra-powerline-separators
    https://github.com/ryanoasis/powerline-extra-symbols
    """
    NONE = SegmentSeparator("", "", "", "")
    """
    No defining separator between segments.
    """

    ORIGINAL = SegmentSeparator("", "", "", "")
    """
    Original/Arrow separators. i.e.  and , and  and .
    """

    ANGLE = SegmentSeparator("", "", "", "")
    """
    Angle separators,  and , and  and . Same as Original.
    """

    SLASH_FORWARD = SegmentSeparator("", "", "", "")
    """
    Forward slash separators,   and  , .
    """

    SLASH_BACKWARD = SegmentSeparator("", "", "", "")
    """
    Backward slash separators,   and  ,  .
    """

    ROUND = SegmentSeparator("", "", "", "")
    """
    Round separators,  and , and  and .
    """

    FLAME = SegmentSeparator(" ", " \u2588", " ", " ")
    """
    Flame separators,  and , and   and  .
    """

    PIXEL_SQUARES = SegmentSeparator(" ", " \u2588", "", " ")
    """
    Pixel square separators,  and ,  and .
    """


class Statusbar:
    """
    Represents the tmux statusbar.
    """

    segment_data: Dict[str, Dict[str, Any] | None] | None = None
    """
    Specify what functions are available to use as segments. The key is {module}.{function name} and its value is a dict
    containing the args that will be passed to it. If the value is None, then no args will be passed to the function.
    Functions included by default in this library or do not need to be prefixed by a module name. A module must be
    accessible by your python path or in a recognized segment directory.

    Example:
    ```python
    statusbar.segment_data = {
        "some_module.add_numbers": {
            "x": 1,
            "y": 2,
        },

    }
    ```
    """

    left_side: tuple[list[Segment], Style] | list[Segment]
    """
    List of Segment objects to display on the left side of the statusbar and optionally, the default style to use for the left side.
    """

    right_side: tuple[list[Segment], Style] | list[Segment]
    """
    List of Segment objects to display on the right side of the statusbar and optionally, the default style to use.
    """

    left_side_max_length: int = 60
    """
    The maximum length of the left side of the statusbar. Defaults to 60.
    """

    right_side_max_length: int = 90
    """
    The maximum length of the right side of the statusbar. Defaults to 90.
    """

    window_list: WindowList
    """
    tmux window status list.
    """

    _segment_separator: SegmentSeparator = Separators.ORIGINAL.value

    @property
    def segment_separator(cls) -> SegmentSeparator:
        """
        The segment separator to use. Defaults to the "original" powerline separators. i.e.  and ,  and .
        """
        return cls._segment_separator

    @segment_separator.setter
    def segment_separator(cls, value: SegmentSeparator | Separators) -> None:
        if isinstance(value, Separators):
            cls._segment_separator = value.value
        else:
            cls._segment_separator = value

    _left_end_separator: SegmentSeparator | None = None

    @property
    def left_end_separator(cls) -> SegmentSeparator:
        """
        The segment separator to use at the end of the left side of the statusbar. Defaults to whatever is set in segment_separator.
        """
        return cls._left_end_separator if cls._left_end_separator is not None else cls.segment_separator

    @left_end_separator.setter
    def left_end_separator(cls, value: SegmentSeparator | Separators) -> None:
        if isinstance(value, Separators):
            cls._left_end_separator = value.value
        else:
            cls._left_end_separator = value

    _right_end_separator: SegmentSeparator | None = None

    @property
    def right_end_separator(cls) -> SegmentSeparator:
        """
        The segment separator to use at the end of the right side of the statusbar. Defaults to whatever is set in segment_separator.
        """
        return cls._right_end_separator if cls._right_end_separator is not None else cls.segment_separator

    @right_end_separator.setter
    def right_end_separator(cls, value: SegmentSeparator | Separators) -> None:
        if isinstance(value, Separators):
            cls._right_end_separator = value.value
        else:
            cls._right_end_separator = value

    default_bg: Color = NamedColor.TERMINAL
    """
    The default background color for the statusbar.
    """

    default_fg: Color = NamedColor.TERMINAL
    """
    The default foreground color for the statusbar.
    """

    default_style: Style | None = None
    """
    The default style for the statusbar.

    Segments will inherit from the default style, e.g. if you set bold here, all segments will be bold unless you explictily unset it in that segment's style.
    """

    status_interval: int = 1
    """
    The interval in seconds at which the statusbar will be redrawn.
    """

    visible: bool = True
    """
    Whether the statusbar is initially visible or not .
    """

    def __init__(self, left_side: tuple[list[Segment], Style] | list[Segment], right_side: tuple[list[Segment], Style] | list[Segment], window_list: WindowList):
        """
        Creates the Statusbar object.

        Parameters:
        -----------
        `left_side`: tuple[list[Segment], Style] | list[Segment]
            List of Segment objects to display on the left side of the statusbar and optionally, the default style to use for the left side.

        `right_side`: tuple[list[Segment], Style] | list[Segment]
            List of Segment objects to display on the right side of the statusbar and optionally, the default style to use.

        `window_list`: WindowList
            tmux window list.
        """
        self.left_side = left_side
        self.right_side = right_side
        self.window_list = window_list

    def __pickle(self) -> bytes:
        """
        Pickles the Statusbar object and returns the pickled bytes.
        """
        return pickle.dumps(self)

    def __commands(self) -> list[str]:
        """
        Returns the tmux commands to be run to update the statusbar.
        """
        if self.default_style is not None:
            if self.default_style.bg is not None:
                self.default_bg = self.default_style.bg
            if self.default_style.fg is not None:
                self.default_fg = self.default_style.fg
        else:
            self.default_style = Style(self.default_bg, self.default_fg)

        return [
            *self.window_list._WindowList__commands(),
            # visible
            f'tmux set -g status {"on" if self.visible else "off"}',
            # interval
            f'tmux set -g status-interval {self.status_interval}',
            # Default Style
            f'tmux set -g status-style "{str(self.default_style)}"',
            # Lengths
            f'tmux set -g status-left-length {self.left_side_max_length}',
            f'tmux set -g status-right-length {self.right_side_max_length}',

            # Left/Right Side
            'tmux set -g status-left "#(tmux-styler -sl #{window_start_flag})"',
            f'tmux set -g status-left-style "{str(self.left_side[1]) if isinstance(self.left_side, tuple) else "default"}"',
            'tmux set -g status-right "#(tmux-styler -sr #{window_end_flag})"',
            f'tmux set -g status-right-style "{str(self.right_side[1]) if isinstance(self.right_side, tuple) else "default"}"',
        ]
