#!/usr/bin/env python3

# Standard library imports
import sys

# Third-party imports
from rich import print
from selenium.common import exceptions

# Local application imports
from .course import Course
from .parser import parse_args


def main():
    """Main entry point for execution."""
    course_args, downloader_args = parse_args()

    # login(session, args.username, args.password)
    course = Course(course_args, downloader_args)

    try:
        course.extract()
    except exceptions.WebDriverException as exp:
        print(exp.msg)
        sys.exit(1)
    finally:
        course.dc()

    print(" DONE! ".center(80, "="))


if __name__ == "__main__":
    main()
