import os
from typing import Dict
import psutil
import json

from .utils import get_user_data_path


def glyphize(process_name: str, glyphs: Dict[str, str]) -> str:
    """ Glyphs for common processes """
    process_name_lower = process_name.lower()
    SHELLS = ["sh", "zsh", "bash", "fish", "csh", "tcsh", "ksh", "dash"]

    glyph: str | None = None
    # Check if the process name is in the user provided glyphs dictionary
    if glyphs and process_name_lower in glyphs:
        glyph = glyphs[process_name_lower]

    # SHELLS
    elif process_name_lower in SHELLS:
        glyph = ""

    # Editors
    elif process_name_lower == "vim" or process_name_lower == "nvim":
        glyph = ""
    elif process_name_lower == "emacs":
        glyph = ""

    # Language interpreters/runtimes/compilers
    elif process_name_lower in ["clang", "clang++", "gcc", "g++", "cc", "c++"]:
        glyph = "/"
    elif process_name_lower.startswith("python"):
        glyph = ""
    elif process_name_lower == "node" or process_name_lower == "nodejs":
        glyph = ""
    elif process_name_lower == "ruby":
        glyph = ""
    elif process_name_lower == "java" or process_name_lower == "javac":
        glyph = ""
    elif process_name_lower in ["rust", "cargo", "rustc"]:
        glyph = ""
    elif process_name_lower.startswith("swift"):
        glyph = ""
    elif process_name_lower == "go":
        glyph = ""

    # === Tools ===
    # Git
    elif process_name_lower == "gh" or process_name_lower.startswith("git"):
        glyph = ""
    # Less pager
    elif process_name_lower == "less":
        glyph = "󰗚"
    # Docker
    elif process_name_lower == "docker":
        glyph = "󰡨"
    # rm
    elif process_name_lower == "rm":
        glyph = ""
    # SSH
    elif process_name_lower == "ssh":
        glyph = "󰷛"
    # Find and Grep
    elif process_name_lower == "find" or process_name_lower == "grep":
        glyph = ""
    # Terraform
    elif process_name_lower == "terraform":
        glyph = "󱁢"

    # Pad the glpyh with a space
    glyph = f"{glyph} " if glyph else ""
    return f"{glyph}{process_name}"


def process_name(pane_id: int) -> str:
    """ Get the name of the process running in the pane """
    # Get the path to the command_settings.json file
    path = get_user_data_path()
    # Load the settings
    with open(os.path.join(path, "command_settings.json"), "r") as f:
        settings = json.load(f)
    max_depth = settings["max_depth"]

    # Get the process
    process = psutil.Process(pane_id)

    for _ in range(max_depth):
        num_children = len(process.children())
        # May seem odd that a process with more than 1 child is considered a leaf,
        # but this is because you probably actually want the the lowest "root" process.
        # ex. neovim with a bunch of plugins will probably have several child processes
        # that are all children of the neovim process, these would be things like the lsp
        # server, linter, etc. but you probably only care about the neovim process.
        if num_children == 0 or num_children > 1:
            break
        else:
            process = process.children()[0]

    name = process.name()
    if settings["glyph"]:
        glyphs = settings["glyphs"]
        return glyphize(name, glyphs)
    else:
        return name
