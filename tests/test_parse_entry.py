"""Test parsing the entry text."""
from typing import List, Tuple

import pytest

from lease_schedule import parser
from lease_schedule import models


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


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "21.01.2011      Parking space 166 (basement   01.12.2010      AGL226281  ",
                "98 in blue on   level)                        999 years from             ",
                "supplementary                                 and including              ",
                "plan 1                                        01.01.2009                 ",
                "until and                  ",
                "including                  ",
                "31.12.3007",
            ],
            models.ParsedText(
                reg_date_and_ref="21.01.2011 98 in blue on supplementary plan 1 until and including 31.12.3007",
                property_desc="Parking space 166 (basement level)",
                lease_date_and_term="01.12.2010 999 years from and including 01.01.2009",
                lessees_title="AGL226281",
            ),
        ),
        (
            [
                "29.11.2010      Flat 2007 Landmark East       01.10.2010      AGL220787  ",
                "Edged and       Tower (twentieth floor        999 years from             ",
                "numbered 5 in   flat)                         1.1.2009                   ",
                "blue (part of)                                                           ",
                "NOTE: See entry in the Charges register relating to a Deed of Variation dated 29/07/2016.",
            ],
            models.ParsedText(
                reg_date_and_ref="29.11.2010 Edged and numbered 5 in blue (part of)",
                property_desc="Flat 2007 Landmark East Tower (twentieth floor flat)",
                lease_date_and_term="01.10.2010 999 years from 1.1.2009",
                lessees_title="AGL220787",
                note="NOTE: See entry in the Charges register relating to a Deed of Variation dated 29/07/2016.",
            ),
        ),
    ],
)
def test_process_entries(lines: List, expected: models.ParsedText) -> None:
    """Test processing the first line.

    Args:
        lines: The entry text lines.
        expected: A tuple with expected delimiters start and end
    """
    parsed_text = parser.process_text(lines)
    assert parsed_text == expected
