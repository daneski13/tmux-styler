import os
import argparse
import subprocess

import inquirer

from .process_segments import process_left_right_segments, process_window_segments
from .utils import dot_conf_path, dot_tmux_path, user_config_path
from .process_name import process_name


def main():
    parser = argparse.ArgumentParser(
        description='Tmux Styler CLI tool')

    # Internal use
    parser.add_argument('-sl', '--seg-left', type=int,
                        nargs=1, help=argparse.SUPPRESS)
    parser.add_argument('-sr', '--seg-right', type=int,
                        nargs=1, help=argparse.SUPPRESS)
    parser.add_argument('-sw', '--seg-window', type=str,
                        nargs=1, help=argparse.SUPPRESS)
    parser.add_argument('-ppid', '--pane-pid', type=int,
                        nargs=1, help=argparse.SUPPRESS)
    parser.add_argument('--config-path', action='store_true',
                        help=argparse.SUPPRESS)

    # Public use
    parser.add_argument('-v', '--version', action='store_true',
                        help='Prints the version of the CLI tool and library')
    parser.add_argument('-c', '--config', action='store_true',
                        help='tmux-styler will look in 2 directories for a config.py file, \
                         select the path to copy the default config to for customization')

    args = parser.parse_args()

    if args.seg_left:
        process_left_right_segments(True, bool(args.seg_left[0]))
        return
    if args.seg_right:
        process_left_right_segments(False, bool(args.seg_right[0]))
        return
    if args.seg_window:
        process_window_segments(
            args.seg_window[0])
        return
    if args.pane_pid:
        print(process_name(args.pane_pid[0]))
        return
    if args.config_path:
        path = user_config_path()
        print(path if path is not None else "")
        return

    if args.version:
        # Get version from the pyproject.toml file
        import toml
        with open("pyproject.toml", "r") as f:
            data = toml.load(f)
            print(data["project"]["version"])
    if args.config:
        # Prompt the user to select a choice
        choices = [dot_conf_path(), dot_tmux_path()]
        from inquirer import List
        questions = [
            List(
                'paths', message='Choose a path to store your config files', choices=choices, carousel=True)
        ]
        path = inquirer.prompt(questions)
        if path is None:
            return
        path = path["paths"]

        # Create the dir and /segments within it
        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, "segments"), exist_ok=True)
        # Copy default.py in this dir to config.py in path
        import shutil
        src = subprocess.run(
            ["tmux", "show", "-g", "@TMUX_STYLER_DIR"], stdout=subprocess.PIPE,)
        src = src.stdout.decode(
            "utf-8").strip().replace("@TMUX_STYLER_DIR ", "")

        src = os.path.join(src, "default.py")
        dst = os.path.join(path, "config.py")
        shutil.copyfile(src, dst)
