import os
import pickle
import importlib
import importlib.util

from ..Statusbar.Statusbar import SegmentSeparator, Statusbar, Segment
from ..Statusbar.WindowList import *
from ..Statusbar.Segments import DEFAULT_SEGMENTS
from .utils import get_user_data_path, user_segments_to_path


def __get_default_segment_module(segment):
    """Path to the included Segments directory"""
    return f".Statusbar.Segments.{DEFAULT_SEGMENTS[segment]}"


def __depickle_statusbar() -> Statusbar:
    """
    Reads the pickled Statusbar object and returns it.
    """
    path = get_user_data_path()
    with open(os.path.join(path, "statusbar.pickle"), "rb") as f:
        return pickle.load(f)


statusbar = __depickle_statusbar()


def __get_segment_content(segment: Segment) -> str:
    """
    Returns the content of the segment.
    """
    # TODO: Proper error handling/logging

    # String segment
    if segment.type == SegmentType.STRING:
        return " " + segment.content + " "

    # Function segment
    try:
        # User defined segments
        if "." in segment.content:
            module, func = segment.content.split(".")
            module = importlib.import_module(module)

        # Default/Included segments
        else:
            # Skip when the segment is not a default segment
            if segment.content not in DEFAULT_SEGMENTS:
                return ""

            # Import the module from .Statusbar.Segments.{module name}
            module = importlib.import_module(
                __get_default_segment_module(segment.content), package="tmux_styler")
            func = segment.content

        # Get the args
        args = {}
        if statusbar.segment_data is not None and func in statusbar.segment_data:
            args = statusbar.segment_data[func]

        # Execute the function
        content = getattr(module, func)(**args)
        # Handle the content
        if isinstance(content, list):
            content = "".join(map(str, content))
        else:
            content = str(content)

        if segment.style is not None:
            content = f"#[{segment.style.apply()}] {content} #[default]"
        else:
            content = f" {content} "
        return content
    except Exception as e:
        return str(e)


def __get_separator(segment: Segment, next_segment: Segment | None, left_side: bool) -> str:
    """
    Returns the proper separator + formatting for between the segments.
    """

    # If the next segment is the last segment on that side
    if next_segment is None:
        end = statusbar.left_end_separator if left_side else statusbar.right_end_separator
        separator_str = end.right_thick if left_side else end.left_thick
        return f'#[bg=default,fg={segment.bg}]' + separator_str if left_side else f'#[bg=default,fg={segment.bg}]' + separator_str

    # If the user has a separator defined
    if segment.separator is not None:
        separator_str = segment.separator
        return f'#[bg={next_segment.bg},fg={segment.bg}]' + separator_str if left_side else f'#[bg={next_segment.bg},fg={segment.bg}]' + separator_str

    separator = statusbar.segment_separator
    # Segments with same bg color use a thin separator
    if str(segment.bg) == str(next_segment.bg):
        separator_str = separator.right_thin if left_side else separator.left_thin
        return f'#[bg={segment.bg},fg={segment.fg}]' + separator_str if left_side else f'#[bg={segment.bg},fg={segment.fg}]' + separator_str
    else:
        separator_str = separator.right_thick if left_side else separator.left_thick
        return f'#[bg={next_segment.bg},fg={segment.bg}]' + separator_str if left_side else f'#[bg={next_segment.bg},fg={segment.bg}]' + separator_str


def __seg_if(if_: str, then: str, else_: str):
    """
    if statement in the form of tmux format string.
    """
    return f"#{{?{if_},{then},{else_}}}"


def process_left_right_segments(left_side: bool, active_flag: bool):
    """
    Processes the segments passed in from the CLI.

    :param left_side: Whether the segments are on the left side or not.
    :param active_flag: Whether the active window is first, for the left side, or last, for the right side.
    """
    # Add user defined segments to sys.path
    user_segments_to_path()

    # Get the segments from the Statusbar object
    segments = statusbar.left_side if left_side else statusbar.right_side
    if isinstance(segments, tuple):
        segments = segments[0]

    format = []
    length = len(segments)
    # Iterate over each segment
    for idx, segment in enumerate(segments):
        # Get the content of the segment, skip if empty
        content = __get_segment_content(segment)
        if content == "":
            continue

        if left_side:
            next_segment: Segment | None = segments[idx +
                                                    1] if idx < length - 1 else None
            # If the window list is on the left side, than the next segment will actually be the first segment part of the window list
            if statusbar.window_list.alignment == WindowListAlignment.LEFT and next_segment is None:
                # If the active window is the first window
                if active_flag:
                    next_segment = statusbar.window_list.active
                else:
                    next_segment = statusbar.window_list.inactive

            # Get the separator
            separator = __get_separator(
                segment, next_segment, left_side)

            # Build the segment
            format.append(f"#[fg={segment.fg},bg={segment.bg}]")
            format.append(content)
            format.append(f"{separator}")

        else:
            next_segment: Segment | None = segments[idx -
                                                    1] if idx > 0 else None
            # If the window list is on the right side, than the first segment in the right side's next segment is part of the window list
            if statusbar.window_list.alignment == WindowListAlignment.RIGHT and next_segment is None:
                # If the active window is the last window
                if active_flag:
                    next_segment = statusbar.window_list.active
                else:
                    next_segment = statusbar.window_list.inactive

            separator = __get_separator(
                segment, next_segment, left_side)

            # Build the segment
            format.append(f"{separator}")
            format.append(f"#[fg={segment.fg},bg={segment.bg}]")
            format.append(content)

    # Print segment to stdout
    print("".join(format))


def process_window_segments(which: str):
    active_segment = statusbar.window_list.active
    inactive_segment = statusbar.window_list.inactive
    # Get the segment from the Statusbar object
    if which == "active":
        segment = active_segment
    else:
        segment = inactive_segment

    # Get the content of the segment
    content = __get_segment_content(segment)

    # Build the segment
    format = []

    alignment = statusbar.window_list.alignment

    # The separator for each window in the list needs some additional logic
    # which we'll implement using tmux format stings to be fast rather than
    # using python logic
    is_last = "#{window_end_flag}"
    is_first = "#{window_start_flag}"
    is_one_less_than_active = "#{==:#I,#{e|-:#{active_window_index},1}}"
    is_one_more_than_active = "#{==:#I,#{e|+:#{active_window_index},1}}"

    separator: SegmentSeparator = statusbar.segment_separator
    match alignment:
        case WindowListAlignment.LEFT:
            end_separator: SegmentSeparator = statusbar.left_end_separator

            format.append(f"#[fg={segment.fg},bg={segment.bg}]")
            format.append(content)
            format.append(f"#[fg={segment.bg},bg=default]")

            if which == "active":
                format.append(
                    __seg_if(is_last, f'#[fg={active_segment.bg}]' + end_separator.right_thick, f'#[fg={active_segment.bg},bg={inactive_segment.bg}]' + separator.right_thick))
            else:
                when_last = f'#[fg={inactive_segment.bg}]' + \
                    end_separator.right_thick
                when_not_last = f'#[fg={inactive_segment.fg},bg={inactive_segment.bg}]' + \
                    separator.right_thin

                format.append(
                    __seg_if(is_last, when_last, __seg_if(is_one_less_than_active, f'#[bg={active_segment.bg}]' + separator.right_thick, when_not_last)))

        case WindowListAlignment.RIGHT:
            end_separator: SegmentSeparator = statusbar.right_end_separator

            if which == "active":
                format.append(
                    __seg_if(is_first, f'#[fg={active_segment.bg}]' + end_separator.left_thick, f'#[fg={active_segment.bg},bg={inactive_segment.bg}]' + separator.left_thick))
            else:
                format.append(f"#[fg={inactive_segment.bg}]")
                when_first = end_separator.left_thick
                when_not_first = f'#[fg={inactive_segment.fg},bg={inactive_segment.bg}]' + \
                    separator.left_thin

                format.append(
                    __seg_if(is_first, when_first, __seg_if(is_one_more_than_active, f'#[bg={active_segment.bg}]' + separator.left_thick, when_not_first)))

            format.append(f"#[fg={segment.fg},bg={segment.bg}]")
            format.append(content)

        case _:
            # TODO: More elegant solution for the center alignments?
            format.append(f"#[fg={segment.fg},bg={segment.bg}]")
            if segment.style is not None:
                format.append(f"#[{segment.style.apply()}]")
            format.append(content)
            format.append("#[default]")
            format.append(
                __seg_if(is_last, "", f"#[fg={active_segment.fg},bg={active_segment.bg}] "))

    # Print segment to stdout
    print("".join(format))
