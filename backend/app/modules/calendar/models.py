from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class EventType(Base):
    """Event type model for categorizing calendar events"""
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(7), nullable=False)  # Hex color code
    icon = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("CalendarEvent", back_populates="event_type_rel")


class CalendarEvent(Base):
    """Calendar event model"""
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    all_day = Column(Boolean, default=False)
    
    # Event type - can be custom or reference to EventType
    event_type = Column(String(100), nullable=True)  # For backward compatibility
    event_type_id = Column(Integer, ForeignKey("event_types.id"), nullable=True)
    
    color = Column(String(7), nullable=True)  # Hex color code
    location = Column(String(200), nullable=True)
    attendees = Column(JSON, nullable=True)  # List of attendee emails/names
    
    # Recurrence
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String(200), nullable=True)  # RRULE format
    
    # Metadata
    created_by = Column(Integer, nullable=True)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    event_type_rel = relationship("EventType", back_populates="events")
    reminders = relationship("EventReminder", back_populates="event", cascade="all, delete-orphan")


class EventReminder(Base):
    """Event reminder model"""
    __tablename__ = "event_reminders"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("calendar_events.id"), nullable=False)
    
    # Reminder timing
    remind_at = Column(DateTime, nullable=False, index=True)
    minutes_before = Column(Integer, nullable=True)  # Minutes before event
    
    # Reminder details
    reminder_type = Column(String(50), default="notification")  # notification, email, sms
    message = Column(Text, nullable=True)
    
    # Status
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("CalendarEvent", back_populates="reminders")
