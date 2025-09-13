#!/usr/bin/env python3


# Standard library imports
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Third-party imports
import configargparse as argparse

# Local application imports
from maktabkhooneh import __version__


LOCAL_CONF_FILE_NAME = "maktabkhooneh-dl.conf"


@dataclass
class CourseConfig:
    class_name: str
    username: str
    password: str

    # Derived fields initialized in __post_init__
    course_name: str = field(init=False)
    course_url: str = field(init=False)

    # runtime state – initially empty, filled later
    chapter_urls: list[str] = field(default_factory=list)  # url for each chapters
    chapter_titles: list[str] = field(default_factory=list)  # title of each chapters
    chapter_downloadlinks: list[str] = field(default_factory=list)  # download link of the chapter's video
    exclude_list: set = field(default_factory=set)  # saves the list of lessons to be included

    def __post_init__(self):
        self.course_name = re.sub(r"http.*://.*?/.*?/", "", self.class_name)
        self.course_url = f"https://maktabkhooneh.org/course/{self.course_name}"


@dataclass
class DownloaderConfig:
    interactive: bool
    quality: str
    path: str
    axel: str | None
    downloader_arguments: list[str]
    overwrite: bool


def parse_args(args=None):
    """Parse the arguments/options passed to the program on the command line."""
    parse_kwargs = {
        "description": "Download maktabkhooneh.ir lecture videos.",
    }
    conf_file_path = Path(".") / f"{LOCAL_CONF_FILE_NAME}"
    if conf_file_path.exists():
        parse_kwargs["default_config_files"] = [conf_file_path]
    parser = argparse.ArgParser(**parse_kwargs)

    # Basic options
    group_basic = parser.add_argument_group("Basic options")

    group_basic.add_argument(
        "class_name",
        action="store",
        help='name of the class (e.g. "آموزش-رایگان-تحلیل-هوشمند-تصاویر-زیست-پزشکی-mk1070/")',
    )

    group_basic.add_argument(
        "-u",
        "--username",
        dest="username",
        action="store",
        help="username (email/tel) that you use to login to Maktabkhooneh",
    )

    group_basic.add_argument("-p", "--password", dest="password", action="store", help="maktabkhooneh password")

    parser.add_argument(
        "-i",
        "--interactive",
        dest="interactive",
        action="store_true",
        default=False,
        help="Interactively asks the user which lesson(s) to download",
    )

    parser.add_argument(
        "-q",
        "--quality",
        dest="quality",
        action="store",
        default="H",
        help="H for high quality and L for low quality video ",
    )

    parser.add_argument(
        "--path",
        dest="path",
        action="store",
        default=".",
        help="path to where to save the file. (Default: current directory)",
    )

    # Parameters related to external downloaders
    group_external_dl = parser.add_argument_group("External downloaders")

    group_external_dl.add_argument(
        "--axel",
        dest="axel",
        action="store",
        nargs="?",
        const="axel",
        default=None,
        help="use axel for downloading, optionally specify axel bin",
    )

    group_external_dl.add_argument(
        "--downloader-arguments",
        dest="downloader_arguments",
        default="",
        help="additional arguments passed to the downloader",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=False,
        help="whether existing files should be overwritten (default: False)",
    )

    parser.add_argument(
        "--version", dest="version", action="store_true", default=False, help="display version and exit"
    )

    # Final parsing of the options
    args = parser.parse_args(args)

    if not args.class_name or not args.username or not args.password:
        parser.print_usage()
        sys.exit(1)

    # show version?
    if args.version:
        print(__version__)
        sys.exit(0)

    # turn list of strings into list
    args.downloader_arguments = args.downloader_arguments.split()

    return CourseConfig(
        class_name=args.class_name,
        username=args.username,
        password=args.password,
    ), DownloaderConfig(
        interactive=args.interactive,
        quality=args.quality,
        path=args.path,
        axel=args.axel,
        downloader_arguments=args.downloader_arguments,
        overwrite=args.overwrite,
    )
