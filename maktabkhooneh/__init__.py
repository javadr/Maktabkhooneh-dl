#!/usr/bin/env python3

# Standard library imports
import textwrap

# Third-party imports

# Local application imports


__version__ = "0.7"

shell_preampble_axel = textwrap.dedent(
    r"""
    #!/usr/bin/env bash
    set -euo pipefail
    IFS=$'\n\t'

    # Where to save files
    mkdir -p "download"

    # axel options (tweak if you like)
    AXEL_OPTS=(-n 8 -a -c -v)   # 8 connections, alternate display, continue, verbose

    # One command per file (name first, then URL)
    """,
).lstrip()
