#!/usr/bin/env python3

# Standard library imports
import os
import time
import textwrap
from typing import List

# Third-party imports
from rich.table import Table, box
from rich.live import Live
from rich.console import Console


# Local application imports


__version__ = "1.0"


def clear_screen():
    # for mac and linux(here, os.name is 'posix')
    if os.name == "posix":
        os.system("clear")
    else:  # for windows platfrom
        os.system("cls")


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


class TableStreamer:
    """A streaming table for live row-by-row updates without clearing other console output."""

    def __init__(self, console=None):
        self.console = console or Console()
        self.table = None
        self.live = None
        self.header = True
        self.reverse = False

    def create_table(self, data:List , header: bool = True, reverse: bool = False):
        """Initialize the table structure from the first dataset.

        Parameters:
            data (list): Initial data to define columns.
            header (bool): Whether to show table headers.
            reverse (bool): If True, swaps column order when adding rows.
        """
        self.header = header
        self.reverse = reverse

        self.table = Table(show_header=header, header_style="bold", row_styles=["none", "dim"], box=box.DOUBLE)

        # Add columns depending on data length
        if len(data) > 1:
            for col, style, justify in zip(
                ("Description", "Lesson"),
                ("green", "bold cyan"),
                ("right", "center"),
            ):
                self.table.add_column(f"[{style}]{col}", style=style, no_wrap=False, justify=justify)
        else:
            self.table.add_column("[green]Description", style="green", no_wrap=False, justify="right")

        # Start Live display
        self.live = Live(self.table, console=self.console, refresh_per_second=4)
        self.live.start()

        # Optionally populate initial rows
        for i, row in enumerate(data, 1):
            self.add_row(row, index=i)

    def add_row(self, row, index=None):
        """Add a single row to the table.

        Parameters:
            row (list or str): The row data to add.
            index (int, optional): Row number for display if needed.
        """
        if self.table is None or self.live is None:
            raise RuntimeError("Table has not been created yet. Call create_table first.")

        # Handle row format based on header and reverse
        if isinstance(row, str):
            row = [row]
        if self.header:
            if self.reverse:
                table_row = [str(index), *row]
            else:
                table_row = [*row, str(index)]
        else:
            table_row = row

        self.table.add_row(*table_row)
        self.live.update(self.table)
        time.sleep(0.02)

    def stop(self):
        """Stop live rendering (call at the end)."""
        if self.live is not None:
            self.live.stop()
