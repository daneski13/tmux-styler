from enum import Enum
from .Segment import *


class WindowListAlignment(Enum):
    """
    Alignment/justification of the window list.

    Attributes:
    -----------
        `LEFT` (str): Left justify window list (place on the left part of the status line)

        `RIGHT` (str): Right justify window list (place on the right part of the status line)

        `CENTER` (str): Center the window list, relative center of the status line left/right

        `ABS_CENTER` (str): Center the window list, but absolute center of the status line
    """

    LEFT = "left"
    """
    Left justify window list (place on the left part of the status line)
    """

    RIGHT = "right"
    """
    Right justify window list (place on the right part of the status line)
    """

    CENTER = "centre"
    """
    Center the window list, relative center of the status line left/right
    """

    ABS_CENTER = "absolute-centre"
    """
    Center the window list, but absolute center of the status line
    """

    def __str__(self):
        """
        String representation of the alignment
        """
        return self.value


class WindowList:
    """
    The tmux window list
    """

    active: Segment
    """
    Segment to use for the currently active window
    """

    inactive: Segment
    """
    Segment to use for inactive windows
    """

    alignment: WindowListAlignment = WindowListAlignment.LEFT
    """
    Alignment/justification of the window list.
    """

    style: Style | None

    def __init__(self, active: Segment, inactive: Segment):
        """
        Style the window list
        """
        self.active = active
        self.inactive = inactive

    def __commands(self) -> list[str]:
        """
        Returns the commands to run to get the window list
        """
        return [
            # Justify
            f'tmux set -g status-justify {str(self.alignment)}',
            # Active
            'tmux set -g window-status-current-format "#(tmux-styler -sw active)"',
            # Inactive
            'tmux set -g window-status-format "#(tmux-styler -sw inactive)"',
            # Handle separators myself
            f'tmux set -g window-status-separator ""',
        ]
