"""
tmux context variables.
"""
from enum import Enum
import subprocess
from typing import List


# TODO: Some context variables could be given better names and descriptions,
#       much of this was generated by ChatGPT from copy pasting directly tmux man page.
#       https://man7.org/linux/man-pages/man1/tmux.1.html#FORMATS
class ContextVar(Enum):
    """
    tmux context variables.

    Methods:
    --------
    current_value() -> str
        Returns the current value of the context variable from tmux.
    """

    ACTIVE_WINDOW_INDEX = "active_window_index"
    """
    Index of active window in session
    """

    ALTERNATE_ON = "alternate_on"
    """
    1 if pane is in alternate screen
    """

    ALTERNATE_SAVED_X = "alternate_saved_x"
    """
    Saved cursor X in alternate screen
    """

    ALTERNATE_SAVED_Y = "alternate_saved_y"
    """
    Saved cursor Y in alternate screen
    """

    BUFFER_CREATED = "buffer_created"
    """
    Time buffer created
    """

    BUFFER_NAME = "buffer_name"
    """
    Name of buffer
    """

    BUFFER_SAMPLE = "buffer_sample"
    """
    Sample of start of buffer
    """

    BUFFER_SIZE = "buffer_size"
    """
    Size of the specified buffer in bytes
    """

    CLIENT_ACTIVITY = "client_activity"
    """
    Time client last had activity
    """

    CLIENT_CELL_HEIGHT = "client_cell_height"
    """
    Height of each client cell in pixels
    """

    CLIENT_CELL_WIDTH = "client_cell_width"
    """
    Width of each client cell in pixels
    """

    CLIENT_CONTROL_MODE = "client_control_mode"
    """
    1 if client is in control mode
    """

    CLIENT_CREATED = "client_created"
    """
    Time client created
    """

    CLIENT_DISCARDED = "client_discarded"
    """
    Bytes discarded when client behind
    """

    CLIENT_FLAGS = "client_flags"
    """
    List of client flags
    """

    CLIENT_HEIGHT = "client_height"
    """
    Height of client
    """

    CLIENT_KEY_TABLE = "client_key_table"
    """
    Current key table
    """

    CLIENT_LAST_SESSION = "client_last_session"
    """
    Name of the client's last session
    """

    CLIENT_NAME = "client_name"
    """
    Name of client
    """

    CLIENT_PID = "client_pid"
    """
    PID of client process
    """

    CLIENT_PREFIX = "client_prefix"
    """
    1 if prefix key has been pressed
    """

    CLIENT_READONLY = "client_readonly"
    """
    1 if client is read-only
    """

    CLIENT_SESSION = "client_session"
    """
    Name of the client's session
    """

    CLIENT_TERMFEATURES = "client_termfeatures"
    """
    Terminal features of client, if any
    """

    CLIENT_TERMNAME = "client_termname"
    """
    Terminal name of client
    """

    CLIENT_TERMTYPE = "client_termtype"
    """
    Terminal type of client, if available
    """

    CLIENT_TTY = "client_tty"
    """
    Pseudo terminal of client
    """

    CLIENT_UID = "client_uid"
    """
    UID of client process
    """

    CLIENT_USER = "client_user"
    """
    User of client process
    """

    CLIENT_UTF8 = "client_utf8"
    """
    1 if client supports UTF-8
    """

    CLIENT_WIDTH = "client_width"
    """
    Width of client
    """

    CLIENT_WRITTEN = "client_written"
    """
    Bytes written to client
    """

    COMMAND = "command"
    """
    Name of command in use, if any
    """

    COMMAND_LIST_ALIAS = "command_list_alias"
    """
    Command alias if listing commands
    """

    COMMAND_LIST_NAME = "command_list_name"
    """
    Command name if listing commands
    """

    COMMAND_LIST_USAGE = "command_list_usage"
    """
    Command usage if listing commands
    """

    CONFIG_FILES = "config_files"
    """
    List of configuration files loaded
    """

    COPY_CURSOR_LINE = "copy_cursor_line"
    """
    Line the cursor is on in copy mode
    """

    COPY_CURSOR_WORD = "copy_cursor_word"
    """
    Word under cursor in copy mode
    """

    COPY_CURSOR_X = "copy_cursor_x"
    """
    Cursor X position in copy mode
    """

    COPY_CURSOR_Y = "copy_cursor_y"
    """
    Cursor Y position in copy mode
    """

    CURRENT_FILE = "current_file"
    """
    Current configuration file
    """

    CURSOR_CHARACTER = "cursor_character"
    """
    Character at cursor in pane
    """

    CURSOR_FLAG = "cursor_flag"
    """
    Pane cursor flag
    """

    CURSOR_X = "cursor_x"
    """
    Cursor X position in pane
    """

    CURSOR_Y = "cursor_y"
    """
    Cursor Y position in pane
    """

    HISTORY_BYTES = "history_bytes"
    """
    Number of bytes in window history
    """

    HISTORY_LIMIT = "history_limit"
    """
    Maximum window history lines
    """

    HISTORY_SIZE = "history_size"
    """
    Size of history in lines
    """

    HOOK = "hook"
    """
    Name of running hook, if any
    """

    HOOK_CLIENT = "hook_client"
    """
    Name of client where hook was run, if any
    """

    HOOK_PANE = "hook_pane"
    """
    ID of pane where hook was run, if any
    """

    HOOK_SESSION = "hook_session"
    """
    ID of session where hook was run, if any
    """

    HOOK_SESSION_NAME = "hook_session_name"
    """
    Name of session where hook was run, if any
    """

    HOOK_WINDOW = "hook_window"
    """
    ID of window where hook was run, if any
    """

    HOOK_WINDOW_NAME = "hook_window_name"
    """
    Name of window where hook was run, if any
    """

    HOST = "host"
    """
    Hostname of local host
    """

    HOST_SHORT = "host_short"
    """
    Hostname of local host (no domain name)
    """

    INSERT_FLAG = "insert_flag"
    """
    Pane insert flag
    """

    KEYPAD_CURSOR_FLAG = "keypad_cursor_flag"
    """
    Pane keypad cursor flag
    """

    KEYPAD_FLAG = "keypad_flag"
    """
    Pane keypad flag
    """

    LAST_WINDOW_INDEX = "last_window_index"
    """
    Index of last window in session
    """

    LINE = "line"
    """
    Line number in the list
    """

    MOUSE_ALL_FLAG = "mouse_all_flag"
    """
    Pane mouse all flag
    """

    MOUSE_ANY_FLAG = "mouse_any_flag"
    """
    Pane mouse any flag
    """

    MOUSE_BUTTON_FLAG = "mouse_button_flag"
    """
    Pane mouse button flag
    """

    MOUSE_HYPERLINK = "mouse_hyperlink"
    """
    Hyperlink under mouse, if any
    """

    MOUSE_LINE = "mouse_line"
    """
    Line under mouse, if any
    """

    MOUSE_SGR_FLAG = "mouse_sgr_flag"
    """
    Pane mouse SGR flag
    """

    MOUSE_STANDARD_FLAG = "mouse_standard_flag"
    """
    Pane mouse standard flag
    """

    MOUSE_UTF8_FLAG = "mouse_utf8_flag"
    """
    Pane mouse UTF-8 flag
    """

    MOUSE_WORD = "mouse_word"
    """
    Word under mouse, if any
    """

    MOUSE_X = "mouse_x"
    """
    Mouse X position, if any
    """

    MOUSE_Y = "mouse_y"
    """
    Mouse Y position, if any
    """

    NEXT_SESSION_ID = "next_session_id"
    """
    Unique session ID for next new session
    """

    ORIGIN_FLAG = "origin_flag"
    """
    Pane origin flag
    """

    PANE_ACTIVE = "pane_active"
    """
    1 if active pane
    """

    PANE_AT_BOTTOM = "pane_at_bottom"
    """
    1 if pane is at the bottom of window
    """

    PANE_AT_LEFT = "pane_at_left"
    """
    1 if pane is at the left of window
    """

    PANE_AT_RIGHT = "pane_at_right"
    """
    1 if pane is at the right of window
    """

    PANE_AT_TOP = "pane_at_top"
    """
    1 if pane is at the top of window
    """

    PANE_BG = "pane_bg"
    """
    Pane background colour
    """

    PANE_BOTTOM = "pane_bottom"
    """
    Bottom of pane
    """

    PANE_CURRENT_COMMAND = "pane_current_command"
    """
    Current command if available
    """

    PANE_CURRENT_PATH = "pane_current_path"
    """
    Current path if available
    """

    PANE_DEAD = "pane_dead"
    """
    1 if pane is dead
    """

    PANE_DEAD_SIGNAL = "pane_dead_signal"
    """
    Exit signal of process in dead pane
    """

    PANE_DEAD_STATUS = "pane_dead_status"
    """
    Exit status of process in dead pane
    """

    PANE_DEAD_TIME = "pane_dead_time"
    """
    Exit time of process in dead pane
    """

    PANE_FG = "pane_fg"
    """
    Pane foreground colour
    """

    PANE_FORMAT = "pane_format"
    """
    1 if format is for a pane
    """

    PANE_HEIGHT = "pane_height"
    """
    Height of pane
    """

    PANE_ID = "pane_id"
    """
    Unique pane ID
    """

    PANE_IN_MODE = "pane_in_mode"
    """
    1 if pane is in a mode
    """

    PANE_INDEX = "pane_index"
    """
    Index of pane
    """

    PANE_INPUT_OFF = "pane_input_off"
    """
    1 if input to pane is disabled
    """

    PANE_LAST = "pane_last"
    """
    1 if last pane
    """

    PANE_LEFT = "pane_left"
    """
    Left of pane
    """

    PANE_MARKED = "pane_marked"
    """
    1 if this is the marked pane
    """

    PANE_MARKED_SET = "pane_marked_set"
    """
    1 if a marked pane is set
    """

    PANE_MODE = "pane_mode"
    """
    Name of pane mode, if any
    """

    PANE_PATH = "pane_path"
    """
    Path of pane (can be set by application)
    """

    PANE_PID = "pane_pid"
    """
    PID of first process in pane
    """

    PANE_PIPE = "pane_pipe"
    """
    1 if pane is being piped
    """

    PANE_RIGHT = "pane_right"
    """
    Right of pane
    """

    PANE_SEARCH_STRING = "pane_search_string"
    """
    Last search string in copy mode
    """

    PANE_START_COMMAND = "pane_start_command"
    """
    Command pane started with
    """

    PANE_START_PATH = "pane_start_path"
    """
    Path pane started with
    """

    PANE_SYNCHRONIZED = "pane_synchronized"
    """
    1 if pane is synchronized
    """

    PANE_TABS = "pane_tabs"
    """
    Pane tab positions
    """

    PANE_TITLE = "pane_title"
    """
    Title of pane (can be set by application)
    """

    PANE_TOP = "pane_top"
    """
    Top of pane
    """

    PANE_TTY = "pane_tty"
    """
    Pseudo terminal of pane
    """

    PANE_WIDTH = "pane_width"
    """
    Width of pane
    """

    PID = "pid"
    """
    Server PID
    """

    RECTANGLE_TOGGLE = "rectangle_toggle"
    """
    1 if rectangle selection is activated
    """

    SCROLL_POSITION = "scroll_position"
    """
    Scroll position in copy mode
    """

    SCROLL_REGION_LOWER = "scroll_region_lower"
    """
    Bottom of scroll region in pane
    """

    SCROLL_REGION_UPPER = "scroll_region_upper"
    """
    Top of scroll region in pane
    """

    SEARCH_MATCH = "search_match"
    """
    Search match if any
    """

    SEARCH_PRESENT = "search_present"
    """
    1 if search started in copy mode
    """

    SELECTION_ACTIVE = "selection_active"
    """
    1 if selection started and changes with the cursor in copy mode
    """

    SELECTION_END_X = "selection_end_x"
    """
    X position of the end of the selection
    """

    SELECTION_END_Y = "selection_end_y"
    """
    Y position of the end of the selection
    """

    SELECTION_PRESENT = "selection_present"
    """
    1 if selection started in copy mode
    """

    SELECTION_START_X = "selection_start_x"
    """
    X position of the start of the selection
    """

    SELECTION_START_Y = "selection_start_y"
    """
    Y position of the start of the selection
    """

    SESSION_ACTIVITY = "session_activity"
    """
    Time of session last activity
    """

    SESSION_ALERTS = "session_alerts"
    """
    List of window indexes with alerts
    """

    SESSION_ATTACHED = "session_attached"
    """
    Number of clients session is attached to
    """

    SESSION_ATTACHED_LIST = "session_attached_list"
    """
    List of clients session is attached to
    """

    SESSION_CREATED = "session_created"
    """
    Time session created
    """

    SESSION_FORMAT = "session_format"
    """
    1 if format is for a session
    """

    SESSION_GROUP = "session_group"
    """
    Name of session group
    """

    SESSION_GROUP_ATTACHED = "session_group_attached"
    """
    Number of clients sessions in group are attached to
    """

    SESSION_GROUP_ATTACHED_LIST = "session_group_attached_list"
    """
    List of clients sessions in group are attached to
    """

    SESSION_GROUP_LIST = "session_group_list"
    """
    List of sessions in group
    """

    SESSION_GROUP_MANY_ATTACHED = "session_group_many_attached"
    """
    1 if multiple clients attached to sessions in group
    """

    SESSION_GROUP_SIZE = "session_group_size"
    """
    Size of session group
    """

    SESSION_GROUPED = "session_grouped"
    """
    1 if session in a group
    """

    SESSION_ID = "session_id"
    """
    Unique session ID
    """

    SESSION_LAST_ATTACHED = "session_last_attached"
    """
    Time session last attached
    """

    SESSION_MANY_ATTACHED = "session_many_attached"
    """
    1 if multiple clients attached
    """

    SESSION_MARKED = "session_marked"
    """
    1 if this session contains the marked pane
    """

    SESSION_NAME = "session_name"
    """
    Name of session
    """

    SESSION_PATH = "session_path"
    """
    Working directory of session
    """

    SESSION_STACK = "session_stack"
    """
    Window indexes in most recent order
    """

    SESSION_WINDOWS = "session_windows"
    """
    Number of windows in session
    """

    SOCKET_PATH = "socket_path"
    """
    Server socket path
    """

    START_TIME = "start_time"
    """
    Server start time
    """

    UID = "uid"
    """
    Server UID
    """

    USER = "user"
    """
    Server user
    """

    VERSION = "version"
    """
    Server version
    """

    WINDOW_ACTIVE = "window_active"
    """
    1 if window active
    """

    WINDOW_ACTIVE_CLIENTS = "window_active_clients"
    """
    Number of clients viewing this window
    """

    WINDOW_ACTIVE_CLIENTS_LIST = "window_active_clients_list"
    """
    List of clients viewing this window
    """

    WINDOW_ACTIVE_SESSIONS = "window_active_sessions"
    """
    Number of sessions on which this window is active
    """

    WINDOW_ACTIVE_SESSIONS_LIST = "window_active_sessions_list"
    """
    List of sessions on which this window is active
    """

    WINDOW_ACTIVITY = "window_activity"
    """
    Time of window last activity
    """

    WINDOW_ACTIVITY_FLAG = "window_activity_flag"
    """
    1 if window has activity
    """

    WINDOW_BELL_FLAG = "window_bell_flag"
    """
    1 if window has bell
    """

    WINDOW_BIGGER = "window_bigger"
    """
    1 if window is larger than client
    """

    WINDOW_CELL_HEIGHT = "window_cell_height"
    """
    Height of each cell in pixels
    """

    WINDOW_CELL_WIDTH = "window_cell_width"
    """
    Width of each cell in pixels
    """

    WINDOW_END_FLAG = "window_end_flag"
    """
    1 if window has the highest index
    """

    WINDOW_FLAGS = "window_flags"
    """
    Window flags with # escaped as ##
    """

    WINDOW_FORMAT = "window_format"
    """
    1 if format is for a window
    """

    WINDOW_HEIGHT = "window_height"
    """
    Height of window
    """

    WINDOW_ID = "window_id"
    """
    Unique window ID
    """

    WINDOW_INDEX = "window_index"
    """
    Index of window
    """

    WINDOW_LAST_FLAG = "window_last_flag"
    """
    1 if window is the last used
    """

    WINDOW_LAYOUT = "window_layout"
    """
    Window layout description, ignoring zoomed window panes
    """

    WINDOW_LINKED = "window_linked"
    """
    1 if window is linked across sessions
    """

    WINDOW_LINKED_SESSIONS = "window_linked_sessions"
    """
    Number of sessions this window is linked to
    """

    WINDOW_LINKED_SESSIONS_LIST = "window_linked_sessions_list"
    """
    List of sessions this window is linked to
    """

    WINDOW_MARKED_FLAG = "window_marked_flag"
    """
    1 if window contains the marked pane
    """

    WINDOW_NAME = "window_name"
    """
    Name of window
    """

    WINDOW_OFFSET_X = "window_offset_x"
    """
    X offset into window if larger than client
    """

    WINDOW_OFFSET_Y = "window_offset_y"
    """
    Y offset into window if larger than client
    """

    WINDOW_PANES = "window_panes"
    """
    Number of panes in window
    """

    WINDOW_RAW_FLAGS = "window_raw_flags"
    """
    Window flags with nothing escaped
    """

    WINDOW_SILENCE_FLAG = "window_silence_flag"
    """
    1 if window has silence alert
    """

    WINDOW_STACK_INDEX = "window_stack_index"
    """
    Index in session most recent stack
    """

    WINDOW_START_FLAG = "window_start_flag"
    """
    1 if window has the lowest index
    """

    WINDOW_VISIBLE_LAYOUT = "window_visible_layout"
    """
    Window layout description, respecting zoomed window panes
    """

    WINDOW_WIDTH = "window_width"
    """
    Width of window
    """

    WINDOW_ZOOMED_FLAG = "window_zoomed_flag"
    """
    1 if window is zoomed
    """

    WRAP_FLAG = "wrap_flag"
    """
    Pane wrap flag
    """

    def __str__(self) -> str:
        """
        Returns the format string representation of context variables for use with tmux.
        """
        if self == self.PANE_CURRENT_COMMAND:
            return "#(tmux-styler -ppid #{pane_pid})"
        else:
            return "#{{{}}}".format(self.value)

    def current_value(self) -> str:
        """
        Returns the current value of the context variable.
        """
        # run shell command to get current value
        return subprocess.run(["tmux", "display-message", "-p", f"'{str(self)}'"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()


def current_values(vars: List[ContextVar]) -> List[str]:
    """
    Returns the current values of the context variables as a list.
    More efficient than calling current_value on each variable.
    """
    # call string on each variable
    command = ["tmux", "display-message", "-p",
               "\n".join([str(var) for var in vars])]
    proc = subprocess.run(command, stdout=subprocess.PIPE)
    # split the output and ruturn
    return proc.stdout.decode("utf-8").strip().split("\n")