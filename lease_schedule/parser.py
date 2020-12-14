"""Parse lease schedule entries from a JSON file."""
import dataclasses
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import ijson
import pydantic

from lease_schedule import models

logger = logging.getLogger()


WHTESPACE_DELIMETER = re.compile(r"[ ]{2,}")  # 2 or more white spaces.


@dataclasses.dataclass
class Column:
    """Start and end points in a a string for a given column."""

    start: int
    end: int


def process_first_line(text: str) -> List[Column]:
    """Process the first line of a text entry.

    The first line seems to be the only one always complete. It can also give
    the delimiters for each column.

    Since matching the words can be complicate, it's safer to search for
    start and end of the sequence of white characters. It also can also help
    parsing the other lines as the start position of each column remains the
    same on the subsequential lines, helping when the column is skipped.

    Args:
        text: The text of the first line.

    Returns:
        A list with all columns start and end positions inside the string.
    """
    def find_delimiters(substring: str, start_pos) -> Tuple[int, int]:
        """Find the whitespace delimiters.

        Here we are not finding the column text but the start and end position
        of the white spaces delimiters.

        Since we do a search in a substring from the last column end position
        it shifts then start and end with the substring start position so we
        can get an absolute position in the string.

        Args:
            substring: The text string from the first line.
            start_pos: The start of the substring.

        Returns:
            A tuple with start and end position of the delimeters, if found.
        """
        match = re.search(WHTESPACE_DELIMETER, substring[start_pos:])
        if match:
            return match.start() + start_pos, match.end() + start_pos

    all_columns: List[Column] = []
    start_pos = 0
    while True:
        delimeters = find_delimiters(text, start_pos)
        if delimeters is None:
            break

        # start and end of a white space character.
        start_delimeter, end_delimeter = delimeters
        all_columns.append(Column(start=start_pos, end=start_delimeter))
        start_pos = end_delimeter

    return all_columns


def process_text(entry_text: List[str]) -> Optional[models.ParsedText]:
    """Parse the information from the entry text field.

    The information is structured as an array of strings with whitespace as
    delimiter with occasional empty columns.

    Args:
        entry_text: A list of strings that contains the entry data.

    Returns:
        The parsed columns from the text entry, if successful.
    """
    columns = process_first_line(entry_text[0])
    first_line = entry_text[0]
    if len(columns) < 4:
        logger.error(f"Too few columns parsed: {first_line}")
        return None

    parsed_text = models.ParsedText(
        reg_date_and_ref=first_line[columns[0].start : columns[0].end],
        property_desc=first_line[columns[1].start : columns[1].end],
        lease_date_and_term=first_line[columns[2].start : columns[2].end],
        lessees_title=first_line[columns[3].start : columns[3].end],
    )
    return parsed_text


def process_entry(lease_schedule: Dict) -> None:
    """Process each lease schedule.

    Args:
        lease_schedule: Each lease schedule data for the property.
    """
    try:
        lease_data = models.LeasesScheduleType.parse_obj(lease_schedule)
    except pydantic.ValidationError as err:
        logger.exception(err)
        return

    # now parse the columns of the entry text.
    for schedule_entry in lease_data.lease_schedule.schedule_entry:
        parsed_text = process_text(schedule_entry.entry_text)
        schedule_entry.parsed_text = parsed_text

    logger.debug(lease_data)


def process_file(json_file: Path) -> None:
    """Process a json file.

    Parse the file for all schedule of notices entries.

    Args:
        json_file: The JSON file we want to parse.
    """
    with open(json_file) as fd:
        # parses all json data and transforms into python types
        title_register_data = ijson.items(fd, "")
        # data from title registry is a list of dictionaries.
        for all_leases in title_register_data:

            # parse data from each lease schedule entry
            for lease_entry in all_leases:
                process_entry(lease_entry)
