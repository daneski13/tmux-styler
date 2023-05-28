"""
Styler object for styling tmux.
"""

import json
import os
from typing import Dict, List
from enum import Enum

from .ContextVars import ContextVar
from .Statusbar.Statusbar import *


class PaneBorder(Enum):
    OFF = "off"
    TOP = "top"
    BOTTOM = "bottom"

    def __str__(self):
        return self.value


class PaneBorderLineStyle(Enum):
    """
    Pane border type/style.

    - SINGLE: single lines using ACS or UTF-8 characters
    - DOUBLE: double lines using UTF-8 characters
    - HEAVY: heavy lines using UTF-8 characters
    - SIMPLE: simple ASCII characters
    - NUMBER: the pane number

    DOUBLE and HEAVY will fall back to standard ACS line
    drawing when UTF-8 is not supported.
    """
    SINGLE = "single"
    DOUBLE = "double"
    HEAVY = "heavy"
    SIMPLE = "simple"
    NUMBER = "number"

    def __str__(self):
        return self.value


class Styler:
    """
    Styler for tmux.
    """

    status_bar: Statusbar | None = None
    """
    Statusbar object for styling the status bar.
    """

    renumber_windows: bool = True
    """
    Whether to renumber windows automatically when a window is closed. Defaults to True.
    """

    auto_rename_window: bool = True
    """
    Whether to automatically rename windows. Defaults to True.
    """

    _auto_rename_window_content: str = str(ContextVar.PANE_CURRENT_COMMAND)

    @property
    def auto_rename_window_content(cls) -> str | ContextVar | List[ContextVar | str]:
        """
        What to rename windows to. Defaults to `ContextVar.PANE_CURRENT_COMMAND`.
        """
        return cls._auto_rename_window_content

    @auto_rename_window_content.setter
    def auto_rename_window_content(cls, value: str | ContextVar | List[ContextVar | str]):
        if isinstance(value, List):
            cls._auto_rename_window_content = "".join(map(str, value))
        else:
            cls._auto_rename_window_content = str(value)

    pane_border: PaneBorder = PaneBorder.TOP
    """
    Pane border position or off. Defaults to `PaneBorder.TOP`.
    """

    pane_border_line_style: PaneBorderLineStyle = PaneBorderLineStyle.SINGLE
    """
    Pane border line type/style. Defaults to `PaneBorderLineStyle.SINGLE`.
    """

    pane_border_content: str | ContextVar | List[ContextVar | str] = [
        ContextVar.PANE_INDEX, " ", ContextVar.PANE_CURRENT_COMMAND]
    """
    Pane border content. Defaults to [ContextVar.PANE_INDEX, " ", ContextVar.PANE_CURRENT_COMMAND]
    Which will display the pane index, a space, and the currently running command e.g. "1 nvim".
    """

    current_command_max_depth: int = 1
    """
    Whenever ContextVar.PANE_CURRENT_COMMAND is used, this is the maximum depth to search for the
    currently running command in the process tree. Defaults to 1.

    Useful to change when you are commonly running processes/commands that spawn other processes
    e.g. you use fig for terminal command completion, tmux given a depth of 1 only looks at 
    first process spawned by a pane's root process. In this case tmux will see fig at depth 0
    and report it's child process, which would just be a shell (zsh/bash/etc), so tmux will always 
    show the shell as the current command. Setting this to 2 will show the command/process below 
    the shell e.g. python or node or an editor.

    If you aren't using fig than a depth of 1 is probably fine as the "root" process tmux sees will
    be the shell and the child process will be the command you are currently running.
    """

    current_command_glyph: bool = True
    """
    Whether to show a glyph corresponding to the current command whenever `ContextVar.PANE_CURRENT_COMMAND`
    is used. Requires a Nerd Font/Patched Font. Defaults to True.
    """

    current_command_glyphs: Dict[str, str] | None = None
    """
    Add or change glyphs for ContextVar.PANE_CURRENT_COMMAND. Common processes are already included by default.
    common editors (vim/neovim, emacs), common language interpreters/runtimes/compilers (clang/gcc, python, 
    node, rust, go, etc.), common tools (git, less, docker), shells (bash, zsh, fish, etc.) and more.

    If you want to add a glyph for a process or change a default, pass a dictionary mapping process names to glyphs.

    e.g. if you want to use a different icon for "node":
    ```python
    styler = Styler()
    styler.current_command_glyphs = {"node": "󰇷"}
    ```
    """

    def style(self):
        """
        Style tmux. Call at the end of your config file to style tmux.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, ".user")
        # create the .user directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)

        # Save the segment data as JSON
        if self.status_bar:
            with open(os.path.join(path, "segment_data.json"), "w") as f:
                f.write(json.dumps(self.status_bar.segment_data))

        # Pickle the statusbar object
        if self.status_bar:
            with open(os.path.join(path, "statusbar.pickle"), "wb") as f:
                f.write(self.status_bar._Statusbar__pickle())

        # Save the current command glyphs/settings as JSON
        if self.current_command_max_depth < 1:
            self.current_command_max_depth = 1
        with open(os.path.join(path, "command_settings.json"), "w") as f:
            f.write(json.dumps({
                "glyphs": self.current_command_glyphs,
                "glyph": self.current_command_glyph,
                "max_depth": self.current_command_max_depth,
            }))

        #  Pane border content to string
        if isinstance(self.pane_border_content, List):
            self.pane_border_content = "".join(
                map(str, self.pane_border_content))
        else:
            self.pane_border_content = str(self.pane_border_content)
        self.pane_border_content = f" {self.pane_border_content} "

        commands = [
            # Load commands for the statusbar
            *self.status_bar._Statusbar__commands(),

            # Auto rename windows
            f'tmux set -g automatic-rename {"on" if self.auto_rename_window else "off"}',
            # Renumber windows
            f'tmux set -g renumber-windows {"on" if self.renumber_windows else "off"}',
            # Auto rename format
            f'tmux set -g automatic-rename-format "{self._auto_rename_window_content}"',

            # Pane border
            f'tmux set -g pane-border-status "{self.pane_border}"',
            # Pane border style
            f'tmux set -g pane-border-line "{self.pane_border_line_style}"',
            # Pane border content
            f'tmux set -g pane-border-format "{self.pane_border_content}"',

            # Term Colors
            'tmux set -g default-terminal "screen-256color"',
        ]

        for command in commands:
            proc = subprocess.Popen(command, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            proc.wait()
            proc.terminate()
