from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


# Event Type Schemas
class EventTypeBase(BaseModel):
    name: str = Field(..., max_length=100)
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EventTypeResponse(EventTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Event Reminder Schemas
class EventReminderBase(BaseModel):
    minutes_before: Optional[int] = Field(None, ge=0)
    reminder_type: str = Field(default="notification", max_length=50)
    message: Optional[str] = None


class EventReminderCreate(EventReminderBase):
    pass


class EventReminderResponse(EventReminderBase):
    id: int
    event_id: int
    remind_at: datetime
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Calendar Event Schemas
class CalendarEventBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    all_day: bool = False
    event_type: Optional[str] = Field(None, max_length=100)
    event_type_id: Optional[int] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    location: Optional[str] = Field(None, max_length=200)
    attendees: Optional[List[str]] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = Field(None, max_length=200)

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class CalendarEventCreate(CalendarEventBase):
    reminders: Optional[List[EventReminderCreate]] = None


class CalendarEventUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    all_day: Optional[bool] = None
    event_type: Optional[str] = Field(None, max_length=100)
    event_type_id: Optional[int] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    location: Optional[str] = Field(None, max_length=200)
    attendees: Optional[List[str]] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = Field(None, max_length=200)

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if v and 'start_time' in values and values['start_time'] and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class CalendarEventResponse(CalendarEventBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    reminders: List[EventReminderResponse] = []

    class Config:
        from_attributes = True


# Query Schemas
class EventsQueryParams(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_type: Optional[str] = None
    event_type_id: Optional[int] = None
    search: Optional[str] = None
    all_day: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)
