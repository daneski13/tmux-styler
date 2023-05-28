#!/usr/bin/env bash

# Get current directory
export TMUX_STYLER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $TMUX_STYLER_DIR
tmux set -g @TMUX_STYLER_DIR "$TMUX_STYLER_DIR"

# Current version of tmux-styler from pyproject.toml
version=$(grep version pyproject.toml | cut -d '"' -f 2)

# Ensure tmux-styler installed and up-to-date
pip=$(python -m pip show tmux-styler 2>/dev/null | grep Version)
if [ -z "$pip" ] || [ "$pip" != "Version: $version" ]; then
    python -m pip install --upgrade . 1>/dev/null
fi

# Get directory of tmux-styler config if it exists
tmux_styler_config=$(tmux-styler --config-path)
if [ -z "$tmux_styler_config" ]; then
    # Execute the default.py config in this dir
    python "$TMUX_STYLER_DIR/default.py"
else
    # Execute the config in the config dir
    echo "User Config: $tmux_styler_config"
    python "$tmux_styler_config"
fi
