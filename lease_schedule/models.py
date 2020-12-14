"""Data models.

All data containers we use to normalise the information from the leases
schedule.
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class ParsedText(BaseModel):
    """Lease entry after being parsed."""

    reg_date_and_ref: str
    property_desc: str
    lease_date_and_term: str
    lessees_title: str
    note: Optional[str] = None


class ScheduleEntryType(BaseModel):
    """Each entry of the lease template."""

    entry_number: int = Field(alias="entryNumber")
    entry_date: str = Field(alias="entryDate")
    entry_type: str = Field(alias="entryType")
    entry_text: List[Optional[str]] = Field(alias="entryText")
    parsed_text: Optional[ParsedText] = None


class ScheduleType(BaseModel):
    """Schedule template."""

    schedule_type: str = Field(alias="scheduleType")
    schedule_entry: List[ScheduleEntryType] = Field(alias="scheduleEntry")


class LeasesScheduleType(BaseModel):
    """Lease schedule template."""

    lease_schedule: ScheduleType = Field(alias="leaseschedule")
