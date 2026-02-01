"""
Quality Assurance Module Database Models
"""
from sqlalchemy import Column, Integer, String, Text, Date, Float, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class QASOP(Base):
    """Standard Operating Procedure Model"""
    __tablename__ = "qa_sops"

    id = Column(Integer, primary_key=True, index=True)
    sop_id = Column(String(50), unique=True, nullable=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100))  # Testing, Calibration, Sample Management, Quality Assurance
    version = Column(String(20), nullable=False)
    status = Column(String(50), default='Active')  # Active, Under Review, Obsolete
    effective_date = Column(Date, nullable=False)
    next_review_date = Column(Date)
    approved_by = Column(String(255))
    document_url = Column(Text)
    linked_tests = Column(JSON)  # Array of test IDs
    linked_instruments = Column(JSON)  # Array of instrument IDs
    linked_departments = Column(JSON)  # Array of department names
    revision_history = Column(JSON)  # Array of {version, date, changedBy, changes}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class QADocument(Base):
    """Document Control Model"""
    __tablename__ = "qa_documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), unique=True, nullable=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100))  # Policy, Certificate, Report, Procedure
    document_type = Column(String(100))
    version = Column(String(20), nullable=False)
    status = Column(String(50), default='Active')
    effective_date = Column(Date, nullable=False)
    approved_by = Column(String(255))
    access_level = Column(String(50))  # Public, Restricted, Confidential
    locked = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)
    document_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class QCCheck(Base):
    """Quality Control Check Model"""
    __tablename__ = "qa_qc_checks"

    id = Column(Integer, primary_key=True, index=True)
    qc_id = Column(String(50), unique=True, nullable=True, index=True)
    test_name = Column(String(255), nullable=False)
    parameter = Column(String(255), nullable=False)
    target_value = Column(Float, nullable=False)
    unit = Column(String(50))
    acceptance_range_min = Column(Float, nullable=False)
    acceptance_range_max = Column(Float, nullable=False)
    last_result = Column(Float)
    status = Column(String(50))  # Pass, Fail
    frequency = Column(String(100))  # Daily, Weekly, Monthly
    last_check_date = Column(Date)
    deviation = Column(Boolean, default=False)
    trend = Column(JSON)  # Array of {date, value}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class NCCAPA(Base):
    """Non-Conformance and Corrective/Preventive Action Model"""
    __tablename__ = "qa_nc_capa"

    id = Column(Integer, primary_key=True, index=True)
    nc_id = Column(String(50), unique=True, nullable=True, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # High, Medium, Low
    status = Column(String(50), default='Open')  # Open, In Progress, Closed
    impacted_area = Column(String(255))
    action_owner = Column(String(255))
    due_date = Column(Date, nullable=False)
    closure_date = Column(Date)
    root_cause = Column(Text)
    corrective_action = Column(Text)
    preventive_action = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class QAAudit(Base):
    """Audit and Compliance Model"""
    __tablename__ = "qa_audits"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(String(50), unique=True, nullable=True, index=True)
    audit_type = Column(String(50), nullable=False)  # Internal, External
    date = Column(Date, nullable=False)
    auditor_name = Column(String(255), nullable=False)
    auditor_organization = Column(String(255))
    scope = Column(Text, nullable=False)
    status = Column(String(50), default='Scheduled')  # Scheduled, In Progress, Completed
    findings = Column(JSON)  # Array of {severity, status, description}
    total_findings = Column(Integer, default=0)
    open_findings = Column(Integer, default=0)
    closed_findings = Column(Integer, default=0)
    compliance_score = Column(Float)
    report_url = Column(Text)
    next_audit_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
