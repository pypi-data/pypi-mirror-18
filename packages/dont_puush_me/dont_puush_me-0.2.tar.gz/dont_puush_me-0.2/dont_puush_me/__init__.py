#!/usr/bin/python3
import base64
import configparser
import hashlib
import logging
import subprocess
import tempfile
import os
import shutil
import sys

import xdg.BaseDirectory


def load_config():
    files = list(xdg.BaseDirectory.load_config_paths("dont-puush-me.ini"))
    files.reverse()

    cfg = configparser.RawConfigParser()
    cfg.read(files)
    return cfg


def take_image(mode, delay, outfile):
    if mode is not None:
        subprocess.check_call([
            "scrot",
            mode,
            "-d", str(delay),
            outfile
        ])
    else:
        with open(outfile, "wb") as f:
            subprocess.check_call(
                [
                    "xclip",
                    "-t", "image/png",
                    "-selection", "clipboard",
                    "-o",
                ],
                stdout=f
            )


def calculate_digest(filename, hashfun):
    with open(filename, "rb") as f:
        BLOCKSIZE = 4096
        blob = f.read(BLOCKSIZE)
        while blob:
            hashfun.update(blob)
            blob = f.read(BLOCKSIZE)
    return hashfun.digest()


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="""\
Use scrot to create a screenshot which is either saved locally or uploaded to a
configured server.
"""
    )

    group = parser.add_argument_group("Capture settings")
    subgroup = group.add_mutually_exclusive_group(
        required=True
    )
    subgroup.add_argument(
        "-f", "--fullscreen",
        dest="mode",
        action="store_const",
        const="-m",
        help="Make a shot of the entire screen",
    )
    subgroup.add_argument(
        "-r", "-w", "--select",
        dest="mode",
        action="store_const",
        const="-s",
        help="Select a region or window to screenshot"
    )
    subgroup.add_argument(
        "-c", "--from-clipboard",
        dest="mode",
        action="store_const",
        const=None,
        help="Use the image from the clipboard"
    )
    subgroup.add_argument(
        "-l", "--from-file",
        dest="from_file",
        default=None,
        help="Use the image in the given PNG file",
    )

    group.add_argument(
        "-d", "--delay",
        type=int,
        help="Delay the screenshot by the given amount of seconds",
        metavar="SECONDS",
        default=0
    )

    group = parser.add_argument_group("Image processing")
    subgroup = group.add_mutually_exclusive_group()
    subgroup.add_argument(
        "--no-optipng",
        dest="optipng",
        action="store_false",
        help="Disable use of optipng before uploading "
        "(overrides config option)",
        default=None
    )
    subgroup.add_argument(
        "--optipng",
        dest="optipng",
        action="store_true",
        help="Enable use of optipng before uploading (overrides config option)"
    )

    group = parser.add_argument_group("Upload settings")
    group.add_argument(
        "--save-locally",
        metavar="FILE",
        help="Save the file locally instead of uploading it to a server",
        default=None
    )

    group = parser.add_argument_group("URL output settings")
    group.add_argument(
        "-z", "--zenity",
        action="store_true",
        default=False,
        help="Show the URL using zenity"
    )

    group.add_argument(
        "-p", "--to-primary",
        dest="to_selections",
        const=("primary", True),
        action="append_const",
        default=[],
        help="Save the URL in the primary X11 selection "
        "(overrides config option)."
    )
    group.add_argument(
        "--no-to-primary",
        dest="to_selections",
        const=("primary", False),
        action="append_const",
        default=[],
        help="Do not save the URL in the primary X11 selection "
        "(overrides config option)."
    )

    group.add_argument(
        "-s", "--to-secondary",
        dest="to_selections",
        const=("secondary", True),
        action="append_const",
        default=[],
        help="Save the URL in the secondary X11 selection "
        "(overrides config option)."
    )
    group.add_argument(
        "--no-to-secondary",
        dest="to_selections",
        const=("secondary", False),
        action="append_const",
        default=[],
        help="Do not save the URL in the secondary X11 selection "
        "(overrides config option)."
    )

    group.add_argument(
        "-b", "--to-clipboard",
        dest="to_selections",
        const=("clipboard", True),
        action="append_const",
        default=[],
        help="Save the URL in the clipboard X11 selection "
        "(overrides config option)."
    )
    group.add_argument(
        "--no-to-clipboard",
        dest="to_selections",
        const=("clipboard", False),
        action="append_const",
        default=[],
        help="Do not save the URL in the clipboard X11 selection "
        "(overrides config option)."
    )

    parser.add_argument(
        "-v", "--verbose",
        dest="verbosity",
        action="count",
        default=0,
        help="Increase verbosity"
    )

    args = parser.parse_args()
    if args.from_file is not None:
        args.mode = "file"

    cfg = load_config()

    logging.basicConfig(
        level={
            0: logging.ERROR,
            1: logging.WARNING,
            2: logging.INFO,
        }.get(args.verbosity, logging.DEBUG)
    )

    to_selections = {}

    try:
        SCP_FORMAT = cfg.get("upload", "scp_format")
        URL_FORMAT = cfg.get("upload", "url_format")
    except (configparser.NoSectionError,
            configparser.NoOptionError) as exc:
        print("missing vital config options", file=sys.stderr)
        print(exc, file=sys.stderr)
        sys.exit(1)

    try:
        to_selections["primary"] = cfg.getboolean(
            "to-selections",
            "primary"
        )
    except (configparser.NoSectionError,
            configparser.NoOptionError) as exc:
        pass

    try:
        to_selections["secondary"] = cfg.getboolean(
            "to-selections",
            "secondary"
        )
    except (configparser.NoSectionError,
            configparser.NoOptionError) as exc:
        pass

    try:
        to_selections["clipboard"] = cfg.getboolean(
            "to-selections",
            "clipboard"
        )
    except (configparser.NoSectionError,
            configparser.NoOptionError) as exc:
        pass

    use_optipng = cfg.getboolean("process", "optipng",
                                 fallback=True)
    if args.optipng is not None:
        use_optipng = args.optipng

    to_selections.update(args.to_selections)

    with tempfile.TemporaryDirectory() as tempdir:
        outfile = os.path.join(tempdir, "dont-puush-me.png")
        if args.save_locally:
            outfile = args.save_locally

        if args.mode != "file":
            take_image(args.mode, args.delay, outfile)
        else:
            shutil.copyfile(args.from_file, outfile)

        if args.save_locally:
            sys.exit(0)

        if use_optipng:
            subprocess.check_call(
                [
                    "optipng",
                    "-quiet",
                    outfile
                ]
            )

        digest = calculate_digest(outfile, hashlib.sha256())
        name = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

        subprocess.check_call(
            [
                "scp",
                outfile,
                SCP_FORMAT.format(name)
            ]
        )

    url = URL_FORMAT.format(name)
    print(url)
    for selection, enabled in to_selections.items():
        if not enabled:
            continue

        logging.debug("copying to %r selection",
                      selection)

        xclip = subprocess.Popen(
            [
                "xclip",
                "-selection", selection,
                "-in",
            ],
            stdin=subprocess.PIPE,
        )
        xclip.communicate(url.encode("utf-8"))
        xclip.wait()

    if args.zenity:
        subprocess.check_call(
            [
                "zenity",
                "--info",
                "--text",
                url
            ]
        )
