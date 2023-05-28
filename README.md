# Tmux Styler

A hackable way to style tmux. Tmux Styler is a tmux [tpm](https://github.com/tmux-plugins/tpm)
plugin and python library that provides an easy and intuitive way to RICE your
tmux setup.

Why use python you might ask? 
* Bash is really annoying 
* Leverage the existing python package ecosystem to create powerful new segments
* Write a config file with an API, has type hints and documentation rather than digging through the tmux man pages

## Features

- [x] Customizable and hackable [Powerline](https://github.com/powerline/powerline) inspired status bar. Inspired by [tmux-powerline](https://github.com/erikw/tmux-powerline).
  - [x] Includes segments for common use cases and/or write your own in Python.
- [x] Documented Python API for interacting with tmux settings, styling options, and creating segments.
- [x] Customizable pane style.
- [x] Glyphize current running command.

## Requirments

- Python 3.10+
- bash 3.2+
- tmux 2.1+
- A patched font / [Nerd Font](https://github.com/ryanoasis/nerd-fonts) for your terminal emulator (necessary for glyphs)

## Installation

1. Install [tpm](https://github.com/tmux-plugins/tpm) and make sure it's working.
2. Install tmux-powerline as a plugin by adding a line to `tmux.conf`:

   ```conf
    set -g @plugin 'daneski13/tmux-styler'
   ```

3. Install the plugin with `<prefix>I`, unless you changed [tpm's keybindings](https://github.com/tmux-plugins/tpm#key-bindings).
   - The default configuration should now be visible.
4. Continue to the [Configuration](#configuration) section below to customize your tmux setup.

## Configuration

Tmux Styler is configured using a python file. You can generate and output the
default configuration file using the CLI tool that is included in the
installation. Run the following in your shell:

```sh
tmux-styler -c
```

You will be given a choice between "\~/.config/tmux/tmux-styler" and
"\~/.tmux/tmux-styler/" to save the configuration file. Please note that this
will be the same directory that the tool will use to search for your custom segments.

Navigate to the directory you chose and open the file in your favorite editor.

### Configuration File

The configuration file is a python file that is executed by tmux-styler. You will notice that it first instantiates a `Styler` object.

See the documentation for the `Styler` class for more information on the available class variables.

Next we build the segments for the Window List, the defaults are most likely fine, but feel free to change the colors. See the documentation for the `Segment` class for more information and the `Colors` class for the available colors.

We build segments for the left and right side of the status bar. The order of the segments is important, as they will be displayed in the order they are added. The first segment will be the leftmost segment and the last segment will be the rightmost segment.

Now you can pass the segments into the `Statusbar` object within the `Styler` object. See the documentation for the `Statusbar` class for more advanced options and information.

Finally, calls `styler.style()` to apply the configuration.

### Custom Segments

You can create a segment that displays a string of your choice by creating a `Segment` object and adding it to the `left_segments` or `right_segments` list in your configuration file.

```python
left_side = [
   # ... Your other segments
   Segment(SegmentType.STRING, "Hello I am a Segment", <Some Background Color>, <Some Foreground Color>)
]
```

You can create custom function segments by creating a python file in the `/segments` directory that is located in the same directory as your configuration file. Custom segments are delineated by their module name, so make sure to name your file something unique. The module name is the filename without the extension. You could use a separate file for each segment.

For example, if you wanted to create a custom segment that displayed the current time, you could create a file called `time.py` in the `/segments` directory. The module name would be `time`.

The module must contain a function, we could call this function `current_time`. The function can take arbitrary arguments, but it must return a `DefinedSegment` object. A `DefinedSegment` can be either a string, a context variable, or a list of strings and/or context variables.

In this example we will be returning a string:

```python
from tmux_styler import DefinedSegment

def current_time(format="%H:%M") -> DefinedSegment:
    import datetime
    current_date = datetime.datetime.now()
    return current_date.strftime(format)
```

Now we can add this segment to our status bar by adding it to the `left_segments` or `right_segments` list in our configuration file.

```python
left_side = [
   # ... Your other segments
   Segment(SegmentType.FUNCTION, "time.current_time", <Some Background Color>, <Some Foreground Color>)
]
```

## Contributing

If you would like to contribute to this project, please read the [CONTRIBUTING.md](./CONTRIBUTING.md) files.
