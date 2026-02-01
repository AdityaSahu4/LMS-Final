from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class ScopeGlobalSettings(Base):
    """Stores global settings for the Scope Management page"""
    __tablename__ = "scope_global_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    internal_audit_frequency = Column(String(50), nullable=True)
    last_audit_date = Column(Date, nullable=True)
    management_review_frequency = Column(String(50), nullable=True)
    last_review_date = Column(Date, nullable=True)
    complete_testing_charge = Column(String(255), nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ILCProgramme(Base):
    """Inter Lab Comparison Programmes"""
    __tablename__ = "scope_ilc_programmes"
    
    id = Column(Integer, primary_key=True, index=True)
    programme = Column(String(255), nullable=True)
    parameter = Column(String(255), nullable=True)
    score = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class LabScope(Base):
    """Scope of Recognition"""
    __tablename__ = "scope_lab_scopes"
    
    id = Column(Integer, primary_key=True, index=True)
    indian_standard = Column(String(255), nullable=True)
    field_of_testing = Column(String(255), nullable=True)
    optimal_testing_time = Column(String(255), nullable=True)
    testing_capacity_per_month = Column(String(255), nullable=True)
    product_manual = Column(String(500), nullable=True) # File path/URL
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ScopeEquipment(Base):
    """Lab Equipment (Standalone for Scope Management)"""
    __tablename__ = "scope_equipments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    model = Column(String(255), nullable=True)
    identification_number = Column(String(255), nullable=True)
    range = Column(String(255), nullable=True)
    least_count = Column(String(255), nullable=True)
    calibration_date = Column(Date, nullable=True)
    validity_date = Column(Date, nullable=True)
    traceability = Column(String(255), nullable=True)
    maintenance_type = Column(String(50), nullable=True)
    amc_schedule = Column(String(500), nullable=True) # File path/URL
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ScopeTest(Base):
    """Scope for Testing (Clause-wise)"""
    __tablename__ = "scope_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(255), nullable=True)
    clause_title = Column(String(255), nullable=True)
    equipment = Column(String(255), nullable=True) # Name text
    environmental_conditions = Column(String(255), nullable=True)
    products = Column(String(255), nullable=True)
    method_of_test = Column(String(255), nullable=True)
    serial_no = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class FacilityAvailable(Base):
    """Facilities Available"""
    __tablename__ = "scope_facilities_available"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(255), nullable=True)
    clause_title = Column(String(255), nullable=True)
    equipment = Column(String(255), nullable=True)
    environmental_conditions = Column(String(255), nullable=True)
    products = Column(String(255), nullable=True)
    method_of_test = Column(String(255), nullable=True)
    serial_no = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class FacilityNotAvailable(Base):
    """Facilities Not Available"""
    __tablename__ = "scope_facilities_not_available"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(255), nullable=True)
    clause_title = Column(String(255), nullable=True)
    method_of_test = Column(String(255), nullable=True)
    facility_not_available = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ReferenceMaterial(Base):
    """Reference Material (Standalone)"""
    __tablename__ = "scope_reference_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    validity = Column(String(255), nullable=True)
    traceability = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ScopeExclusion(Base):
    """Exclusions"""
    __tablename__ = "scope_exclusions"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(255), nullable=True)
    test_name = Column(String(255), nullable=True)
    justification = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class TestingCharge(Base):
    """Sample Testing Charges"""
    __tablename__ = "scope_testing_charges"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(255), nullable=True)
    clause_title = Column(String(255), nullable=True)
    charge = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
