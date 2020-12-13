#!/usr/bin/env python
"""Extract Schedule of notices of lease data.

Usage:
    ./extract.py --json-file <file-name>
"""
import logging
from logging import config as log_config
from pathlib import Path
from typing import Dict, Optional

import ijson
import typer

from lease_schedule import models


def process_entry(lease_schedule: Dict) -> None:
    """Process each lease schedule.

    Args:
        lease_schedule: Each lease schedule data for the property.
    """
    lease_data = models.LeasesScheduleType.parse_obj(lease_schedule)
    print(lease_data)


def process_file(json_file: Path) -> None:
    """Process a json file.

    Parse the file for all schedule of notices entries.

    Args:
        json_file: The JSON file we want to parse.
    """
    with open(json_file) as fd:
        title_register_data = ijson.items(fd, "")
        for all_leases in title_register_data:
            for lease_entry in all_leases:
                process_entry(lease_entry)


def main(
    json_file: Optional[Path] = typer.Option(None, show_default=False),
) -> None:
    """Parse arguments and extract info.

    Args:
        json_file: A file with tests and test details.

    Raises:
        Abort: For missing command line arguments
    """
    logging.basicConfig(level=logging.INFO)
    log_config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
            },
        },
    )
    logger = logging.getLogger()
    logger.info("Start extracting info.")

    if json_file is None:
        typer.echo("No json file specified.")
        raise typer.Abort()

    process_file(json_file)


if __name__ == "__main__":
    typer.run(main)
