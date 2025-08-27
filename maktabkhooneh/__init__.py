#!/usr/bin/env python3

# Standard library imports
import textwrap

# Third-party imports

# Local application imports


__version__ = "0.9"

shell_script = textwrap.dedent(
    r"""
    #!/usr/bin/env bash
    set -euo pipefail
    IFS=$'\n\t'

    # Where to save files
    mkdir -p "videos"

    # Options
    AXEL_OPTS=(-n 8 -a -c -v)   # 8 connections, alternate display, continue, verbose
    WGET_OPTS=(-c --show-progress --progress=bar:force:noscroll) # continue, quiet with progress bar
    # -L follow redirects
    # -C - resume interrupted downloads
    # -O save with original filename (we'll override with -o when needed)
    # --retry 5 try up to 5 times on transient errors
    CURL_OPTS=(-L -C - --retry 5)      # follow redirects, resume, output file
    ARIA2C_OPTS=(-x 8 -s 8 -c --console-log-level=warn --summary-interval=0) # 8 connections, resume, quiet

    # Ask user for downloader preference
    echo "Choose a downloader:"
    echo "1) axel"
    echo "2) wget"
    echo "3) curl"
    echo "4) aria2c"
    read -rp "Enter choice [1-4]: " choice

    case $choice in
        1) DOWNLOADER="axel";   OPTS=("${{AXEL_OPTS[@]}}") ;;
        2) DOWNLOADER="wget";   OPTS=("${{WGET_OPTS[@]}}") ;;
        3) DOWNLOADER="curl";   OPTS=("${{CURL_OPTS[@]}}") ;;
        4) DOWNLOADER="aria2c"; OPTS=("${{ARIA2C_OPTS[@]}}") ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac

    echo "Using: $DOWNLOADER"

    # Example download list
    files=(
        {}
    )

    # Loop through files and download
    for entry in "${{files[@]}}"; do
        name="${{entry%%|*}}"
        url="${{entry##*|}}"
        out="videos/$name.mp4"

        case $DOWNLOADER in
            axel) "$DOWNLOADER" "${{OPTS[@]}}" -o "$out" "$url" ;;
            wget) "$DOWNLOADER" "${{OPTS[@]}}" -O "$out" "$url" ;;
            curl) "$DOWNLOADER" "${{OPTS[@]}}" -o "$out" "$url" ;;
            aria2c) "$DOWNLOADER" "${{OPTS[@]}}" -o "$out" "$url" ;;
        esac
    done
    """,
).lstrip()
