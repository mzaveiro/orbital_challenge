"""Test parsing the entry text."""
from typing import Tuple

import pytest

from lease_schedule import parser


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "21.01.2011      Parking space 166 (basement   01.12.2010      AGL226281  ",
            ((0, 10), (16, 43), (46, 56), (62, 71)),
        ),
    ],
)
def test_process_first(text: str, expected: Tuple) -> None:
    """Test processing the first line.

    Args:
        text: The text from the first line.
        expected: A tuple with expected delimiters start and end
    """
    parsed_line = parser.process_first_line(text)
    assert len(parsed_line) == 4
    for i, column in enumerate(parsed_line):
        assert column.start == expected[i][0]
        assert column.end == expected[i][1]
