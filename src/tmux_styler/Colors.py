"""
tmux supported color types.
"""

from enum import Enum
import re
import abc


class Color(metaclass=abc.ABCMeta):
    """
    An abstract base class for all colors.
    """

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Returns the string representation of the Color object.
        """
        pass


class Color256(Color):
    """
    Represents an Xterm color value in the range of 0 to 255.
    See: https://www.ditig.com/256-colors-cheat-sheet/

    Attributes:
    -----------
    `value`: int
        The integer value of the color.

    Raises:
    -------
    ValueError:
        If the value is less than 0 or greater than 255.
    """

    def __init__(self, value: int):
        """
        Initializes a new instance of Color256.

        Parameters:
        ----------
        `value`: int
            The integer value of the color.
        """
        if value < 0 or value > 255:
            raise ValueError('Color256 value must be between 0 and 255')
        self.value = value

    def __str__(self) -> str:
        """
        Returns the string representation of the Color256 object.
        """
        return f"colour{str(self.value)}"


class HexColor(Color):
    """
    Represents a hexadecimal color code in the format #RRGGBB.

    Attributes:
    -----------
    `value`: str
        The hexadecimal color code.

    Raises:
    -------
    ValueError:
        If the hex code is not in the format #RRGGBB.
    """

    def __init__(self, hex: str):
        """
        Initializes a new instance of HexColor.

        Parameters:
        ----------
        `hex`: str
            The hexadecimal color code.
        """
        HEX_COLOR_REGEX = re.compile(r'^#[0-9a-fA-F]{6}$')
        if not HEX_COLOR_REGEX.match(hex):
            raise ValueError(
                'HexColor value is not a valid hexadecimal color code')
        self.value = hex

    def __str__(self) -> str:
        """
        Returns the string representation of the HexColor object.
        """
        return "#" + self.value


class _NamedColorMeta(type(Color), type(Enum)):
    pass


class NamedColor(Color, Enum, metaclass=_NamedColorMeta):
    """
    An enumeration of valid named colors. 

    TERMINAL and DEFAULT are special values. 
    TERMINAL will appear transparent when used as a background color and as your terminal's text color when used as a foreground color.
    DEFAULT will use the default background or foreground color of the statusbar.
    """
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    TERMINAL = "terminal"
    DEFAULT = "default"

    def __str__(self) -> str:
        """
        Returns the string representation of a named color.
        """
        return self.value
