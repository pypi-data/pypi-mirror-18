``dont-puush-me``
#################

Challenged by the ease of use of existing tools to capture and upload
screenshots so that they are available for the general public, this script was
made.

The only required dependencies are ``scp`` and ``scrot``. Optional dependencies
are:

* ``optipng`` (used by default, can be turned off in configuration)
* ``xclip`` (to save URLs to clipboard or to capture PNG images from clipboard)
* ``zenity`` (to display URLs in a window)

Configuration
=============

The upload URL is configured using a config file ``dont-puush-me.ini``. It can
be placed anywhere in your XDG configuration paths (usually ``~/.config`` and
``/etc/xdg``).

The config file has the following format::

    [upload]
    scp_format=user@host:/path/to/directory/{}.png
    url_format=https://host.example/directory/{}.png

    [process]
    optipng=true

    [to-selections]
    primary=false
    secondary=false
    clipboard=false

The ``scp_format`` and ``url_format`` settings are required and no default
exists for them. In those, the first occurence of ``{}`` is replaced with the
automatically generated filename for the image. You need to set those values
such that ``scp`` can be used to upload the file so that it will be reachable
at the url given by ``url_format`` afterwards.

The ``optipng`` setting is a boolean setting which enables or disables the
default use of optipng before uploading an image.

The ``to-selections`` section provides a boolean flag for each of the X11
selections. They default to false and can be overriden by command line flags.
The URL is put into each of the selections which are set to true either by
command line arguments or the configuration file.

Usage
=====

The tool features a lot of options, but the actual usage is usually simple. For
examples scroll down. Here is the full usage::

    usage: dont-puush-me [-h] (-f | -r | -c | -l FROM_FILE) [-d SECONDS]
                         [--no-optipng | --optipng] [--save-locally FILE] [-z]
                         [-p] [--no-to-primary] [-s] [--no-to-secondary] [-b]
                         [--no-to-clipboard] [-v]

    Use scrot to create a screenshot which is either saved locally or uploaded to
    a configured server.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase verbosity

    Capture settings:
      -f, --fullscreen      Make a shot of the entire screen
      -r, -w, --select      Select a region or window to screenshot
      -c, --from-clipboard  Use the image from the clipboard
      -l FROM_FILE, --from-file FROM_FILE
                            Use the image in the given PNG file
      -d SECONDS, --delay SECONDS
                            Delay the screenshot by the given amount of seconds

    Image processing:
      --no-optipng          Disable use of optipng before uploading (overrides
                            config option)
      --optipng             Enable use of optipng before uploading (overrides
                            config option)

    Upload settings:
      --save-locally FILE   Save the file locally instead of uploading it to a
                            server

    URL output settings:
      -z, --zenity          Show the URL using zenity
      -p, --to-primary      Save the URL in the primary X11 selection (overrides
                            config option).
      --no-to-primary       Do not save the URL in the primary X11 selection
                            (overrides config option).
      -s, --to-secondary    Save the URL in the secondary X11 selection (overrides
                            config option).
      --no-to-secondary     Do not save the URL in the secondary X11 selection
                            (overrides config option).
      -b, --to-clipboard    Save the URL in the clipboard X11 selection (overrides
                            config option).
      --no-to-clipboard     Do not save the URL in the clipboard X11 selection
                            (overrides config option).

Examples:

* Capture a fullscreen screenshot and copy the resulting URL to the primary X11
  selection::

      dont-puush-me -fp

* Capture a rectangle from the screen (the rectangle is picked using the mouse;
  clicking without dragging selects the rectangle of the clicked window)::

      dont-puush-me -r

  The URL is printed to the terminal.

* Capture a rectangle, do not apply optipng and display the URL in a window
  (requires zenity)::

      dont-puush-me --no-optipng -rz
