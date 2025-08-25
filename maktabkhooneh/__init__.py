#!/usr/bin/env python3

# Standard library imports
import textwrap

# Third-party imports

# Local application imports


__version__ = "0.8"

shell_preampble = textwrap.dedent(
    r"""
    #!/usr/bin/env bash
    set -euo pipefail
    IFS=$'\n\t'

    # Where to save files
    mkdir -p "download"
    {}
    # One command per file
    """,
).lstrip()


axel_option = textwrap.dedent(
    r"""
    # axel options (tweak if you like)
    AXEL_OPTS=(-n 8 -a -c -v -o)   # 8 connections, alternate display, continue, verbose
    """,
)

wget_option = textwrap.dedent(
    r"""
    # wget options
    WGET_OPTS=(-c --show-progress --progress=bar:force:noscroll -O)
    """,
)

curl_option = textwrap.dedent(
    r"""
    # curl options (tweak if you like)
    # -L follow redirects
    # -C - resume interrupted downloads
    # -O save with original filename (we'll override with -o when needed)
    # --retry 5 try up to 5 times on transient errors
    CURL_OPTS=(-L -C - --retry 5 -o)
    """,
)
