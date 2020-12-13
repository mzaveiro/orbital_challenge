"""Data models.

All data containers we use to normalise the information from the leases
schedule.
"""
from typing import List

from pydantic import BaseModel, Field


class ScheduleEntryType(BaseModel):
    """Each entry of the lease template."""

    entry_number: int = Field(alias="entryNumber")
    entry_date: str = Field(alias="entryDate")
    entry_type: str = Field(alias="entryType")
    entry_text: List[str] = Field(alias="entryText")


class ScheduleType(BaseModel):
    """Schedule template."""

    schedule_type: str = Field(alias="scheduleType")
    schedule_entry: List[ScheduleEntryType] = Field(alias="scheduleEntry")


class LeasesScheduleType(BaseModel):
    """Lease schedule template."""

    lease_schedule: ScheduleType = Field(alias="leaseschedule")
