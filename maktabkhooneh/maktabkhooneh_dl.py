#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys

from .course import Course
from .parser import parse_args
from selenium.common import exceptions


def main():
    """
    Main entry point for execution.
    """

    args = parse_args()

    #login(session, args.username, args.password)
    course = Course(
        args.class_name,  #e.g. q
        args.username,
        args.password,
        args)

    try:
        _ = course.extract()
    except exceptions.WebDriverException as exp:
        print(exp.msg)
        sys.exit(1)
    finally:
        course.dc()

    print(" DONE! ".center(80, '='))


if __name__ == '__main__':
    main()
