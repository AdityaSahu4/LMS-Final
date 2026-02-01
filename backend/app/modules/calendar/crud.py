from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
from . import models, schemas


# Event Type CRUD
def create_event_type(db: Session, event_type: schemas.EventTypeCreate) -> models.EventType:
    """Create a new event type"""
    db_event_type = models.EventType(**event_type.dict())
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return db_event_type


def get_event_type(db: Session, event_type_id: int) -> Optional[models.EventType]:
    """Get event type by ID"""
    return db.query(models.EventType).filter(models.EventType.id == event_type_id).first()


def get_event_types(db: Session, skip: int = 0, limit: int = 100) -> List[models.EventType]:
    """Get all event types"""
    return db.query(models.EventType).offset(skip).limit(limit).all()


def update_event_type(
    db: Session, event_type_id: int, event_type: schemas.EventTypeUpdate
) -> Optional[models.EventType]:
    """Update an event type"""
    db_event_type = get_event_type(db, event_type_id)
    if not db_event_type:
        return None
    
    update_data = event_type.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event_type, field, value)
    
    db_event_type.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_event_type)
    return db_event_type


def delete_event_type(db: Session, event_type_id: int) -> bool:
    """Delete an event type"""
    db_event_type = get_event_type(db, event_type_id)
    if not db_event_type:
        return False
    
    db.delete(db_event_type)
    db.commit()
    return True


# Calendar Event CRUD
def create_event(db: Session, event: schemas.CalendarEventCreate, user_id: Optional[int] = None) -> models.CalendarEvent:
    """Create a new calendar event"""
    event_data = event.dict(exclude={'reminders'})
    db_event = models.CalendarEvent(**event_data, created_by=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Create reminders if provided
    if event.reminders:
        for reminder in event.reminders:
            remind_at = db_event.start_time - timedelta(minutes=reminder.minutes_before or 0)
            db_reminder = models.EventReminder(
                event_id=db_event.id,
                remind_at=remind_at,
                **reminder.dict()
            )
            db.add(db_reminder)
        db.commit()
        db.refresh(db_event)
    
    return db_event


def get_event(db: Session, event_id: int) -> Optional[models.CalendarEvent]:
    """Get event by ID"""
    return db.query(models.CalendarEvent).filter(
        and_(
            models.CalendarEvent.id == event_id,
            models.CalendarEvent.is_deleted == False
        )
    ).first()


def get_events(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    event_type: Optional[str] = None,
    event_type_id: Optional[int] = None,
    search: Optional[str] = None,
    all_day: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.CalendarEvent]:
    """Get events with filtering"""
    query = db.query(models.CalendarEvent).filter(models.CalendarEvent.is_deleted == False)
    
    # Date range filter
    if start_date:
        query = query.filter(models.CalendarEvent.end_time >= start_date)
    if end_date:
        query = query.filter(models.CalendarEvent.start_time <= end_date)
    
    # Event type filter
    if event_type:
        query = query.filter(models.CalendarEvent.event_type == event_type)
    if event_type_id:
        query = query.filter(models.CalendarEvent.event_type_id == event_type_id)
    
    # All day filter
    if all_day is not None:
        query = query.filter(models.CalendarEvent.all_day == all_day)
    
    # Search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.CalendarEvent.title.ilike(search_pattern),
                models.CalendarEvent.description.ilike(search_pattern),
                models.CalendarEvent.location.ilike(search_pattern)
            )
        )
    
    return query.order_by(models.CalendarEvent.start_time).offset(skip).limit(limit).all()


def update_event(
    db: Session, event_id: int, event: schemas.CalendarEventUpdate
) -> Optional[models.CalendarEvent]:
    """Update a calendar event"""
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    
    update_data = event.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db_event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int, soft_delete: bool = True) -> bool:
    """Delete a calendar event (soft or hard delete)"""
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    
    if soft_delete:
        db_event.is_deleted = True
        db_event.deleted_at = datetime.utcnow()
        db.commit()
    else:
        db.delete(db_event)
        db.commit()
    
    return True


def get_events_by_date_range(
    db: Session, start_date: datetime, end_date: datetime
) -> List[models.CalendarEvent]:
    """Get all events within a date range"""
    return get_events(db, start_date=start_date, end_date=end_date, limit=1000)


def search_events(db: Session, query: str, limit: int = 50) -> List[models.CalendarEvent]:
    """Search events by title, description, or location"""
    return get_events(db, search=query, limit=limit)
