from tmux_styler import *


def main():
    styler = Styler()

    # Window list
    active = Segment(SegmentType.FUNCTION, "window_info",
                     NamedColor.WHITE, NamedColor.BLACK)
    inactive = Segment(SegmentType.FUNCTION, "window_info",
                       HexColor("#555555"), NamedColor.WHITE)
    window_list = WindowList(active, inactive)

    # Left side
    left_side = [
        Segment(SegmentType.FUNCTION, "session_name",
                Color256(220), Color256(234), style=Style(attrs=[TextAttributes.BOLD])),
    ]
    # Right side
    right_side = [
        Segment(SegmentType.FUNCTION, "cwd", Color256(105), Color256(
            233)),
        Segment(SegmentType.FUNCTION, "date_day", separator=""),
        Segment(SegmentType.FUNCTION, "date", separator="|"),
        Segment(SegmentType.FUNCTION, "time", separator="|"),
    ]

    # Statusbar
    styler.status_bar = Statusbar(left_side, right_side, window_list)
    styler.status_bar.segment_data = {
        "cwd": {
            "max_length": 35,
        }
    }
    styler.status_bar.segment_separator = Separators.ORIGINAL
    styler.status_bar.left_end_separator = Separators.PIXEL_SQUARES
    styler.status_bar.right_end_separator = Separators.PIXEL_SQUARES

    styler.style()


if __name__ == '__main__':
    main()
