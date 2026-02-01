from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

# --- Global Settings ---
class ScopeGlobalSettingsBase(BaseModel):
    internal_audit_frequency: Optional[str] = None
    last_audit_date: Optional[date] = None
    management_review_frequency: Optional[str] = None
    last_review_date: Optional[date] = None
    complete_testing_charge: Optional[str] = None

class ScopeGlobalSettingsCreate(ScopeGlobalSettingsBase):
    pass

class ScopeGlobalSettings(ScopeGlobalSettingsBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True

# --- ILC Programmes ---
class ILCProgrammeBase(BaseModel):
    programme: Optional[str] = None
    parameter: Optional[str] = None
    score: Optional[str] = None

class ILCProgrammeCreate(ILCProgrammeBase):
    pass

class ILCProgramme(ILCProgrammeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Lab Scope ---
class LabScopeBase(BaseModel):
    indian_standard: Optional[str] = None
    field_of_testing: Optional[str] = None
    optimal_testing_time: Optional[str] = None
    testing_capacity_per_month: Optional[str] = None
    product_manual: Optional[str] = None

class LabScopeCreate(LabScopeBase):
    pass

class LabScope(LabScopeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Equipment ---
class ScopeEquipmentBase(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    identification_number: Optional[str] = None
    range: Optional[str] = None
    least_count: Optional[str] = None
    calibration_date: Optional[date] = None
    validity_date: Optional[date] = None
    traceability: Optional[str] = None
    maintenance_type: Optional[str] = None
    amc_schedule: Optional[str] = None

class ScopeEquipmentCreate(ScopeEquipmentBase):
    pass

class ScopeEquipment(ScopeEquipmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Scope Tests ---
class ScopeTestBase(BaseModel):
    clause_number: Optional[str] = None
    clause_title: Optional[str] = None
    equipment: Optional[str] = None
    environmental_conditions: Optional[str] = None
    products: Optional[str] = None
    method_of_test: Optional[str] = None
    serial_no: Optional[str] = None

class ScopeTestCreate(ScopeTestBase):
    pass

class ScopeTest(ScopeTestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Facilities Available ---
class FacilityAvailableBase(BaseModel):
    clause_number: Optional[str] = None
    clause_title: Optional[str] = None
    equipment: Optional[str] = None
    environmental_conditions: Optional[str] = None
    products: Optional[str] = None
    method_of_test: Optional[str] = None
    serial_no: Optional[str] = None

class FacilityAvailableCreate(FacilityAvailableBase):
    pass

class FacilityAvailable(FacilityAvailableBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Facilities Not Available ---
class FacilityNotAvailableBase(BaseModel):
    clause_number: Optional[str] = None
    clause_title: Optional[str] = None
    method_of_test: Optional[str] = None
    facility_not_available: Optional[str] = None

class FacilityNotAvailableCreate(FacilityNotAvailableBase):
    pass

class FacilityNotAvailable(FacilityNotAvailableBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Reference Material ---
class ReferenceMaterialBase(BaseModel):
    name: Optional[str] = None
    validity: Optional[str] = None
    traceability: Optional[str] = None

class ReferenceMaterialCreate(ReferenceMaterialBase):
    pass

class ReferenceMaterial(ReferenceMaterialBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Exclusions ---
class ScopeExclusionBase(BaseModel):
    clause_number: Optional[str] = None
    test_name: Optional[str] = None
    justification: Optional[str] = None

class ScopeExclusionCreate(ScopeExclusionBase):
    pass

class ScopeExclusion(ScopeExclusionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Testing Charges ---
class TestingChargeBase(BaseModel):
    clause_number: Optional[str] = None
    clause_title: Optional[str] = None
    charge: Optional[str] = None
    remarks: Optional[str] = None

class TestingChargeCreate(TestingChargeBase):
    pass

class TestingCharge(TestingChargeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Composite Schema for getAll ---
class ScopeManagementData(BaseModel):
    global_settings: Optional[ScopeGlobalSettings] = None
    ilc_programmes: List[ILCProgramme] = []
    scopes: List[LabScope] = []
    equipments: List[ScopeEquipment] = []
    scope_tests: List[ScopeTest] = []
    facilities_available: List[FacilityAvailable] = []
    facilities_not_available: List[FacilityNotAvailable] = []
    reference_materials: List[ReferenceMaterial] = []
    exclusions: List[ScopeExclusion] = []
    testing_charges: List[TestingCharge] = []
