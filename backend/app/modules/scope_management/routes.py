from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from . import models, schemas

router = APIRouter()

# --- Common CRUD Helpers ---
def get_or_404(db: Session, model, id: int):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def create_item(db: Session, model, schema):
    db_item = model(**schema.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, model, id: int, schema):
    db_item = get_or_404(db, model, id)
    for key, value in schema.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, model, id: int):
    db_item = get_or_404(db, model, id)
    db.delete(db_item)
    db.commit()
    return {"ok": True}


# --- Composite Data Fetch ---
@router.get("/all", response_model=schemas.ScopeManagementData)
def get_all_data(db: Session = Depends(get_db)):
    """Fetch all Scope Management data in one request"""
    # Ensure global settings exist
    settings = db.query(models.ScopeGlobalSettings).first()
    if not settings:
        settings = models.ScopeGlobalSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "global_settings": settings,
        "ilc_programmes": db.query(models.ILCProgramme).all(),
        "scopes": db.query(models.LabScope).all(),
        "equipments": db.query(models.ScopeEquipment).all(),
        "scope_tests": db.query(models.ScopeTest).all(),
        "facilities_available": db.query(models.FacilityAvailable).all(),
        "facilities_not_available": db.query(models.FacilityNotAvailable).all(),
        "reference_materials": db.query(models.ReferenceMaterial).all(),
        "exclusions": db.query(models.ScopeExclusion).all(),
        "testing_charges": db.query(models.TestingCharge).all(),
    }


# --- Global Settings ---
@router.put("/settings", response_model=schemas.ScopeGlobalSettings)
def update_settings(settings: schemas.ScopeGlobalSettingsCreate, db: Session = Depends(get_db)):
    db_settings = db.query(models.ScopeGlobalSettings).first()
    if not db_settings:
        db_settings = models.ScopeGlobalSettings(**settings.dict())
        db.add(db_settings)
    else:
        for key, value in settings.dict(exclude_unset=True).items():
            setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings


# --- ILC Programmes ---
@router.post("/ilc", response_model=schemas.ILCProgramme)
def create_ilc(item: schemas.ILCProgrammeCreate, db: Session = Depends(get_db)):
    return create_item(db, models.ILCProgramme, item)

@router.put("/ilc/{id}", response_model=schemas.ILCProgramme)
def update_ilc(id: int, item: schemas.ILCProgrammeCreate, db: Session = Depends(get_db)):
    return update_item(db, models.ILCProgramme, id, item)

@router.delete("/ilc/{id}")
def delete_ilc(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.ILCProgramme, id)


# --- Lab Scope ---
@router.post("/scope", response_model=schemas.LabScope)
def create_scope(item: schemas.LabScopeCreate, db: Session = Depends(get_db)):
    return create_item(db, models.LabScope, item)

@router.put("/scope/{id}", response_model=schemas.LabScope)
def update_scope(id: int, item: schemas.LabScopeCreate, db: Session = Depends(get_db)):
    return update_item(db, models.LabScope, id, item)

@router.delete("/scope/{id}")
def delete_scope(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.LabScope, id)


# --- Equipment ---
@router.post("/equipment", response_model=schemas.ScopeEquipment)
def create_equipment(item: schemas.ScopeEquipmentCreate, db: Session = Depends(get_db)):
    return create_item(db, models.ScopeEquipment, item)

@router.put("/equipment/{id}", response_model=schemas.ScopeEquipment)
def update_equipment(id: int, item: schemas.ScopeEquipmentCreate, db: Session = Depends(get_db)):
    return update_item(db, models.ScopeEquipment, id, item)

@router.delete("/equipment/{id}")
def delete_equipment(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.ScopeEquipment, id)


# --- Scope Tests ---
@router.post("/test", response_model=schemas.ScopeTest)
def create_test(item: schemas.ScopeTestCreate, db: Session = Depends(get_db)):
    return create_item(db, models.ScopeTest, item)

@router.put("/test/{id}", response_model=schemas.ScopeTest)
def update_test(id: int, item: schemas.ScopeTestCreate, db: Session = Depends(get_db)):
    return update_item(db, models.ScopeTest, id, item)

@router.delete("/test/{id}")
def delete_test(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.ScopeTest, id)


# --- Facilities Available ---
@router.post("/facility-available", response_model=schemas.FacilityAvailable)
def create_facility_available(item: schemas.FacilityAvailableCreate, db: Session = Depends(get_db)):
    return create_item(db, models.FacilityAvailable, item)

@router.put("/facility-available/{id}", response_model=schemas.FacilityAvailable)
def update_facility_available(id: int, item: schemas.FacilityAvailableCreate, db: Session = Depends(get_db)):
    return update_item(db, models.FacilityAvailable, id, item)

@router.delete("/facility-available/{id}")
def delete_facility_available(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.FacilityAvailable, id)


# --- Facilities Not Available ---
@router.post("/facility-not-available", response_model=schemas.FacilityNotAvailable)
def create_facility_not_available(item: schemas.FacilityNotAvailableCreate, db: Session = Depends(get_db)):
    return create_item(db, models.FacilityNotAvailable, item)

@router.put("/facility-not-available/{id}", response_model=schemas.FacilityNotAvailable)
def update_facility_not_available(id: int, item: schemas.FacilityNotAvailableCreate, db: Session = Depends(get_db)):
    return update_item(db, models.FacilityNotAvailable, id, item)

@router.delete("/facility-not-available/{id}")
def delete_facility_not_available(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.FacilityNotAvailable, id)


# --- Reference Material ---
@router.post("/reference-material", response_model=schemas.ReferenceMaterial)
def create_reference_material(item: schemas.ReferenceMaterialCreate, db: Session = Depends(get_db)):
    return create_item(db, models.ReferenceMaterial, item)

@router.put("/reference-material/{id}", response_model=schemas.ReferenceMaterial)
def update_reference_material(id: int, item: schemas.ReferenceMaterialCreate, db: Session = Depends(get_db)):
    return update_item(db, models.ReferenceMaterial, id, item)

@router.delete("/reference-material/{id}")
def delete_reference_material(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.ReferenceMaterial, id)


# --- Exclusions ---
@router.post("/exclusion", response_model=schemas.ScopeExclusion)
def create_exclusion(item: schemas.ScopeExclusionCreate, db: Session = Depends(get_db)):
    return create_item(db, models.ScopeExclusion, item)

@router.put("/exclusion/{id}", response_model=schemas.ScopeExclusion)
def update_exclusion(id: int, item: schemas.ScopeExclusionCreate, db: Session = Depends(get_db)):
    return update_item(db, models.ScopeExclusion, id, item)

@router.delete("/exclusion/{id}")
def delete_exclusion(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.ScopeExclusion, id)


# --- Testing Charges ---
@router.post("/testing-charge", response_model=schemas.TestingCharge)
def create_testing_charge(item: schemas.TestingChargeCreate, db: Session = Depends(get_db)):
    return create_item(db, models.TestingCharge, item)

@router.put("/testing-charge/{id}", response_model=schemas.TestingCharge)
def update_testing_charge(id: int, item: schemas.TestingChargeCreate, db: Session = Depends(get_db)):
    return update_item(db, models.TestingCharge, id, item)

@router.delete("/testing-charge/{id}")
def delete_testing_charge(id: int, db: Session = Depends(get_db)):
    return delete_item(db, models.TestingCharge, id)
