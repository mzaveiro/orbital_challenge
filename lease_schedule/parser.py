"""Parse lease schedule entries from a JSON file."""
import logging
from pathlib import Path
from typing import Dict

import ijson
import pydantic

from lease_schedule import models


def process_entry(lease_schedule: Dict) -> None:
    """Process each lease schedule.

    Args:
        lease_schedule: Each lease schedule data for the property.
    """
    try:
        lease_data = models.LeasesScheduleType.parse_obj(lease_schedule)
    except pydantic.ValidationError as err:
        logger = logging.getLogger()
        logger.exception(err)
        return


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
