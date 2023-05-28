"""
tmux styling options.
"""

from enum import Enum
from typing import List
from tmux_styler.Colors import Color


class TextAttributes(Enum):
    """
    Text attributes to apply to text.

    Attributes:
    -----------
    `ACS`: Use the terminal alternate character set.

    `BRIGHT`: Make the text brighter.
    
    `BOLD`: Make the text bold.
    
    `DIM`: Make the text dimmer.
    
    `UNDERSCORE`: Underline the text.
    
    `BLINK`: Make the text blink.
    
    `REVERSE`: Reverse the background and text colors.
    
    `HIDDEN`: Hide the text.
    
    `ITALICS`: Make the text italicized.
    
    `OVERLINE`: Overline the text.
    
    `STRIKETHROUGH`: Draw a line through the text.
    
    `DOUBLE_UNDERSCORE`: Double underline the text.
    
    `CURLY_UNDERSCORE`: Curly underline the text.
    
    `DOTTED_UNDERSCORE`: Dotted underline the text.
    
    `DASHED_UNDERSCORE`: Dashed underline the text.
    """

    ACS = "acs"
    """The terminal alternate character set."""
    BRIGHT = "bright"
    """Make the text brighter."""
    BOLD = "bold"
    """Make the text bold."""
    DIM = "dim"
    """Make the text dimmer."""
    UNDERSCORE = "underscore"
    """Underline the text."""
    BLINK = "blink"
    """Make the text blink."""
    REVERSE = "reverse"
    """Reverse the background and text colors."""
    HIDDEN = "hidden"
    """Hide the text."""
    ITALICS = "italics"
    """Make the text italicized."""
    OVERLINE = "overline"
    """Overline the text."""
    STRIKETHROUGH = "strikethrough"
    """Draw a line through the text."""
    DOUBLE_UNDERSCORE = "double-underscore"
    """Double underline the text."""
    CURLY_UNDERSCORE = "curly-underscore"
    """Curly underline the text."""
    DOTTED_UNDERSCORE = "dotted-underscore"
    """Dotted underline the text."""
    DASHED_UNDERSCORE = "dashed-underscore"
    """Dashed underline the text."""

    def __str__(self):
        """
        Returns the string representation of the attribute.
        """
        return self.value


class Style:
    """
    Represents a tmux style.

    Attributes:
    -----------
    `fg`: Color | None
        The foreground color, none will default to the inherited color. (default: None)

    `bg`: Color | None
        The background color, none will default to the inherited color. (default: None)

    `attrs`: List[TextAttributes] | None
        The text attributes to apply to the text. (default: None)

    `unset_attrs`: List[TextAttributes] | None
        The text attributes to unset from the text. This will override any attributes
        set in attrs. You may want to unset attributes that you've set by default. (default: None)
    """

    def __init__(self, bg: Color | None = None, fg: Color | None = None,  attrs: List[TextAttributes] | None = None, unset_attrs: List[TextAttributes] | None = None):
        """
        Creates a style for use with tmux.
        """
        self.fg = fg
        self.bg = bg
        self.attrs = attrs
        self.unset_attrs = unset_attrs

    def __str__(self) -> str:
        """
        Returns the format string representation of the entire style.
        """
        bg = "" if self.bg is None else "bg={}".format(self.bg)
        fg = "" if self.fg is None else "fg={}".format(self.fg)
        attrs = "" if self.attrs is None else f"{' '.join(map(str, self.attrs))}"
        unset_attrs = "" if self.unset_attrs is None else f"{' '.join(map(lambda x: f'no{str(x)}', self.unset_attrs))}"
        return ",".join(
            filter(lambda x: x != "", [fg, bg, attrs, unset_attrs]))

    def apply(self) -> str:
        """
        Returns a string that applies all of the attributes in the style (attrs, unset_attrs, and alignment).
        """
        attrs = "" if self.attrs is None else f"{' '.join(map(str, self.attrs))}"
        unset_attrs = "" if self.unset_attrs is None else f"{' '.join(map(lambda x: f'no{str(x)}', self.unset_attrs))}"
        return ",".join(
            filter(lambda x: x != "", [attrs, unset_attrs]))
