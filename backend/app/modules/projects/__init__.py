"""
Projects and Customers module
"""

from .models import Customer, Project
from .schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    ProjectCreate, ProjectUpdate, ProjectResponse
)
from . import crud, routes

__all__ = [
    "Customer", "Project",
    "CustomerCreate", "CustomerUpdate", "CustomerResponse",
    "ProjectCreate", "ProjectUpdate", "ProjectResponse",
    "crud", "routes"
]
