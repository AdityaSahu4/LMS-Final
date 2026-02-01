"""
Quality Assurance Module CRUD Operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date

from . import models, schemas


# ============= SOP CRUD =============

def get_sops(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None
) -> List[models.QASOP]:
    """Get all SOPs with optional filtering"""
    query = db.query(models.QASOP).filter(models.QASOP.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                models.QASOP.sop_id.ilike(f"%{search}%"),
                models.QASOP.title.ilike(f"%{search}%"),
                models.QASOP.approved_by.ilike(f"%{search}%")
            )
        )
    
    if category:
        query = query.filter(models.QASOP.category == category)
    
    if status:
        query = query.filter(models.QASOP.status == status)
    
    return query.order_by(models.QASOP.created_at.desc()).offset(skip).limit(limit).all()


def get_sop(db: Session, sop_id: int) -> Optional[models.QASOP]:
    """Get a single SOP by ID"""
    return db.query(models.QASOP).filter(
        models.QASOP.id == sop_id,
        models.QASOP.is_deleted == False
    ).first()


def create_sop(db: Session, sop: schemas.SOPCreate) -> models.QASOP:
    """Create a new SOP"""
    sop_data = sop.model_dump(by_alias=False)
    
    # Auto-generate sop_id if not provided
    if not sop_data.get('sop_id'):
        # Get count of existing SOPs to generate unique ID
        count = db.query(models.QASOP).filter(models.QASOP.is_deleted == False).count()
        sop_data['sop_id'] = f"SOP-{count + 1:04d}"
    
    # Sanitize JSON fields - convert string "null" to None
    json_fields = ['revision_history', 'linked_tests', 'linked_instruments', 'linked_departments']
    for field in json_fields:
        if field in sop_data and sop_data[field] == "null":
            sop_data[field] = None
    
    db_sop = models.QASOP(**sop_data)
    db.add(db_sop)
    db.commit()
    db.refresh(db_sop)
    return db_sop


def update_sop(db: Session, sop_id: int, sop: schemas.SOPUpdate) -> Optional[models.QASOP]:
    """Update an existing SOP"""
    db_sop = get_sop(db, sop_id)
    if not db_sop:
        return None
    
    update_data = sop.model_dump(by_alias=False, exclude_unset=True)
    
    # Sanitize JSON fields - convert string "null" to None
    json_fields = ['revision_history', 'linked_tests', 'linked_instruments', 'linked_departments']
    for field in json_fields:
        if field in update_data and update_data[field] == "null":
            update_data[field] = None
    
    for field, value in update_data.items():
        setattr(db_sop, field, value)
    
    db.commit()
    db.refresh(db_sop)
    return db_sop


def delete_sop(db: Session, sop_id: int) -> bool:
    """Soft delete an SOP"""
    db_sop = get_sop(db, sop_id)
    if not db_sop:
        return False
    
    db_sop.is_deleted = True
    db.commit()
    return True


# ============= Document CRUD =============

def get_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    document_type: Optional[str] = None
) -> List[models.QADocument]:
    """Get all documents with optional filtering"""
    query = db.query(models.QADocument).filter(models.QADocument.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                models.QADocument.document_id.ilike(f"%{search}%"),
                models.QADocument.title.ilike(f"%{search}%"),
                models.QADocument.approved_by.ilike(f"%{search}%")
            )
        )
    
    if category:
        query = query.filter(models.QADocument.category == category)
    
    if document_type:
        query = query.filter(models.QADocument.document_type == document_type)
    
    return query.order_by(models.QADocument.created_at.desc()).offset(skip).limit(limit).all()


def get_document(db: Session, document_id: int) -> Optional[models.QADocument]:
    """Get a single document by ID"""
    return db.query(models.QADocument).filter(
        models.QADocument.id == document_id,
        models.QADocument.is_deleted == False
    ).first()


def create_document(db: Session, document: schemas.DocumentCreate) -> models.QADocument:
    """Create a new document"""
    document_data = document.model_dump(by_alias=False)
    
    # Auto-generate document_id if not provided
    if not document_data.get('document_id'):
        # Get count of existing documents to generate unique ID
        count = db.query(models.QADocument).filter(models.QADocument.is_deleted == False).count()
        document_data['document_id'] = f"DOC-{count + 1:04d}"
    
    db_document = models.QADocument(**document_data)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(db: Session, document_id: int, document: schemas.DocumentUpdate) -> Optional[models.QADocument]:
    """Update an existing document"""
    db_document = get_document(db, document_id)
    if not db_document:
        return None
    
    update_data = document.model_dump(by_alias=False, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_document, field, value)
    
    db.commit()
    db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: int) -> bool:
    """Soft delete a document"""
    db_document = get_document(db, document_id)
    if not db_document:
        return False
    
    db_document.is_deleted = True
    db.commit()
    return True


def lock_document(db: Session, document_id: int) -> Optional[models.QADocument]:
    """Lock a document"""
    db_document = get_document(db, document_id)
    if not db_document:
        return None
    
    db_document.locked = True
    db.commit()
    db.refresh(db_document)
    return db_document


def unlock_document(db: Session, document_id: int) -> Optional[models.QADocument]:
    """Unlock a document"""
    db_document = get_document(db, document_id)
    if not db_document:
        return None
    
    db_document.locked = False
    db.commit()
    db.refresh(db_document)
    return db_document


# ============= QC Check CRUD =============

def get_qc_checks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None
) -> List[models.QCCheck]:
    """Get all QC checks with optional filtering"""
    query = db.query(models.QCCheck).filter(models.QCCheck.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                models.QCCheck.qc_id.ilike(f"%{search}%"),
                models.QCCheck.test_name.ilike(f"%{search}%"),
                models.QCCheck.parameter.ilike(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(models.QCCheck.status == status)
    
    return query.order_by(models.QCCheck.created_at.desc()).offset(skip).limit(limit).all()


def get_qc_check(db: Session, qc_id: int) -> Optional[models.QCCheck]:
    """Get a single QC check by ID"""
    return db.query(models.QCCheck).filter(
        models.QCCheck.id == qc_id,
        models.QCCheck.is_deleted == False
    ).first()


def create_qc_check(db: Session, qc_check: schemas.QCCheckCreate) -> models.QCCheck:
    """Create a new QC check"""
    qc_data = qc_check.model_dump(by_alias=False)
    
    # Auto-generate qc_id if not provided
    if not qc_data.get('qc_id'):
        # Get count of existing QC checks to generate unique ID
        count = db.query(models.QCCheck).filter(models.QCCheck.is_deleted == False).count()
        qc_data['qc_id'] = f"QC-{count + 1:04d}"
    
    # Sanitize trend field - convert string "null" to None
    if qc_data.get('trend') == "null":
        qc_data['trend'] = None
    
    # Extract acceptance_range
    acceptance_range = qc_data.pop('acceptance_range', {})
    qc_data['acceptance_range_min'] = acceptance_range.get('min')
    qc_data['acceptance_range_max'] = acceptance_range.get('max')
    
    db_qc = models.QCCheck(**qc_data)
    db.add(db_qc)
    db.commit()
    db.refresh(db_qc)
    return db_qc


def update_qc_check(db: Session, qc_id: int, qc_check: schemas.QCCheckUpdate) -> Optional[models.QCCheck]:
    """Update an existing QC check"""
    db_qc = get_qc_check(db, qc_id)
    if not db_qc:
        return None
    
    update_data = qc_check.model_dump(by_alias=False, exclude_unset=True)
    
    # Extract acceptance_range if present
    if 'acceptance_range' in update_data:
        acceptance_range = update_data.pop('acceptance_range')
        if acceptance_range:
            update_data['acceptance_range_min'] = acceptance_range.get('min')
            update_data['acceptance_range_max'] = acceptance_range.get('max')
    
    for field, value in update_data.items():
        setattr(db_qc, field, value)
    
    db.commit()
    db.refresh(db_qc)
    return db_qc


def delete_qc_check(db: Session, qc_id: int) -> bool:
    """Soft delete a QC check"""
    db_qc = get_qc_check(db, qc_id)
    if not db_qc:
        return False
    
    db_qc.is_deleted = True
    db.commit()
    return True


def record_qc_result(db: Session, qc_id: int, result: float, check_date: date) -> Optional[models.QCCheck]:
    """Record a QC check result"""
    db_qc = get_qc_check(db, qc_id)
    if not db_qc:
        return None
    
    # Update last result and date
    db_qc.last_result = result
    db_qc.last_check_date = check_date
    
    # Determine pass/fail status
    if db_qc.acceptance_range_min <= result <= db_qc.acceptance_range_max:
        db_qc.status = 'Pass'
        db_qc.deviation = False
    else:
        db_qc.status = 'Fail'
        db_qc.deviation = True
    
    # Add to trend data
    if db_qc.trend is None:
        db_qc.trend = []
    
    db_qc.trend.append({
        'date': check_date.isoformat(),
        'value': result
    })
    
    db.commit()
    db.refresh(db_qc)
    return db_qc


# ============= NC/CAPA CRUD =============

def get_nc_capas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None
) -> List[models.NCCAPA]:
    """Get all NC/CAPA records with optional filtering"""
    query = db.query(models.NCCAPA).filter(models.NCCAPA.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                models.NCCAPA.nc_id.ilike(f"%{search}%"),
                models.NCCAPA.description.ilike(f"%{search}%"),
                models.NCCAPA.action_owner.ilike(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(models.NCCAPA.status == status)
    
    if severity:
        query = query.filter(models.NCCAPA.severity == severity)
    
    return query.order_by(models.NCCAPA.created_at.desc()).offset(skip).limit(limit).all()


def get_nc_capa(db: Session, nc_id: int) -> Optional[models.NCCAPA]:
    """Get a single NC/CAPA by ID"""
    return db.query(models.NCCAPA).filter(
        models.NCCAPA.id == nc_id,
        models.NCCAPA.is_deleted == False
    ).first()


def create_nc_capa(db: Session, nc_capa: schemas.NCCAPACreate) -> models.NCCAPA:
    """Create a new NC/CAPA"""
    nc_data = nc_capa.model_dump(by_alias=False)
    
    # Auto-generate nc_id if not provided
    if not nc_data.get('nc_id'):
        # Get count of existing NC/CAPAs to generate unique ID
        count = db.query(models.NCCAPA).filter(models.NCCAPA.is_deleted == False).count()
        nc_data['nc_id'] = f"NC-{count + 1:04d}"
    
    db_nc = models.NCCAPA(**nc_data)
    db.add(db_nc)
    db.commit()
    db.refresh(db_nc)
    return db_nc


def update_nc_capa(db: Session, nc_id: int, nc_capa: schemas.NCCAPAUpdate) -> Optional[models.NCCAPA]:
    """Update an existing NC/CAPA"""
    db_nc = get_nc_capa(db, nc_id)
    if not db_nc:
        return None
    
    update_data = nc_capa.model_dump(by_alias=False, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_nc, field, value)
    
    db.commit()
    db.refresh(db_nc)
    return db_nc


def delete_nc_capa(db: Session, nc_id: int) -> bool:
    """Soft delete an NC/CAPA"""
    db_nc = get_nc_capa(db, nc_id)
    if not db_nc:
        return False
    
    db_nc.is_deleted = True
    db.commit()
    return True


def close_nc_capa(db: Session, nc_id: int, closure_date: date) -> Optional[models.NCCAPA]:
    """Close an NC/CAPA"""
    db_nc = get_nc_capa(db, nc_id)
    if not db_nc:
        return None
    
    db_nc.status = 'Closed'
    db_nc.closure_date = closure_date
    db.commit()
    db.refresh(db_nc)
    return db_nc


# ============= Audit CRUD =============

def get_audits(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    audit_type: Optional[str] = None,
    status: Optional[str] = None
) -> List[models.QAAudit]:
    """Get all audits with optional filtering"""
    query = db.query(models.QAAudit).filter(models.QAAudit.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                models.QAAudit.audit_id.ilike(f"%{search}%"),
                models.QAAudit.auditor_name.ilike(f"%{search}%"),
                models.QAAudit.scope.ilike(f"%{search}%")
            )
        )
    
    if audit_type:
        query = query.filter(models.QAAudit.audit_type == audit_type)
    
    if status:
        query = query.filter(models.QAAudit.status == status)
    
    return query.order_by(models.QAAudit.created_at.desc()).offset(skip).limit(limit).all()


def get_audit(db: Session, audit_id: int) -> Optional[models.QAAudit]:
    """Get a single audit by ID"""
    return db.query(models.QAAudit).filter(
        models.QAAudit.id == audit_id,
        models.QAAudit.is_deleted == False
    ).first()


def create_audit(db: Session, audit: schemas.AuditCreate) -> models.QAAudit:
    """Create a new audit"""
    audit_data = audit.model_dump(by_alias=False)
    
    # Auto-generate audit_id if not provided
    if not audit_data.get('audit_id'):
        # Get count of existing audits to generate unique ID
        count = db.query(models.QAAudit).filter(models.QAAudit.is_deleted == False).count()
        audit_data['audit_id'] = f"AUD-{count + 1:04d}"
    
    db_audit = models.QAAudit(**audit_data)
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit


def update_audit(db: Session, audit_id: int, audit: schemas.AuditUpdate) -> Optional[models.QAAudit]:
    """Update an existing audit"""
    db_audit = get_audit(db, audit_id)
    if not db_audit:
        return None
    
    update_data = audit.model_dump(by_alias=False, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_audit, field, value)
    
    db.commit()
    db.refresh(db_audit)
    return db_audit


def delete_audit(db: Session, audit_id: int) -> bool:
    """Soft delete an audit"""
    db_audit = get_audit(db, audit_id)
    if not db_audit:
        return False
    
    db_audit.is_deleted = True
    db.commit()
    return True
