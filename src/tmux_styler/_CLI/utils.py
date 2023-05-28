import os
import sys


def get_user_data_path() -> str:
    """
    Returns the path to the stored user information.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "..", ".user")
    return os.path.normpath(path)


def dot_conf_path() -> str:
    """
    Returns the XDG_CONFIG_HOME, ~/.config path
    """
    config_dir = os.environ.get('XDG_CONFIG_HOME') or os.path.join(
        os.path.expanduser('~'), '.config')
    return os.path.join(config_dir, 'tmux', 'tmux-styler')


def dot_tmux_path() -> str:
    """
    Returns the .tmux path
    """
    return os.path.join(os.path.expanduser('~'), '.tmux', 'tmux-styler')


def real_path_exists(path: str) -> bool:
    """
    Whether or not a path exists using real path
    """
    return os.path.exists(os.path.realpath(os.path.normpath(path)))


def user_config_path() -> str | None:
    """
    Returns the path where the user has defined the config.py file if it exists.
    """
    dot_config = os.path.join(dot_conf_path(), "config.py")
    if real_path_exists(dot_config):
        return dot_config
    else:
        dot_tmux = os.path.join(dot_tmux_path(), "config.py")
        return dot_tmux if real_path_exists(dot_tmux) else None


def user_segments_path() -> str | None:
    """
    Returns the path where the user has defined custom segments if it exists.
    """

    dot_config = os.path.join(dot_conf_path(), "segments")
    dot_config = os.path.realpath(dot_config)
    if real_path_exists(dot_config):
        return dot_config
    else:
        dot_tmux = os.path.join(dot_tmux_path(), "segments")
        return dot_tmux if real_path_exists(dot_tmux) else None


def user_segments_to_path():
    """
    Adds the user segments path to sys.path for importing
    """
    path = user_segments_path()
    if path:
        sys.path.append(path)
