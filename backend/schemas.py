"""Pydantic schemas for request and response payloads."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .models import AssignmentStatus, ProjectStatus, UnitStatus


class LandOwnerCreate(BaseModel):
    name: str = Field(..., description="Full name of the land owner")
    contact_info: Optional[str] = Field(None, description="Email or phone")


class LandOwnerRead(LandOwnerCreate):
    id: int

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    location: Optional[str]
    land_owner_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectRead(ProjectCreate):
    id: int
    status: ProjectStatus

    class Config:
        from_attributes = True


class UnitCreate(BaseModel):
    project_id: int
    unit_number: str
    floor: Optional[int]
    area_sqm: Optional[float]


class UnitUpdate(BaseModel):
    floor: Optional[int] = None
    area_sqm: Optional[float] = None
    status: Optional[UnitStatus] = None


class UnitRead(UnitCreate):
    id: int
    status: UnitStatus

    class Config:
        from_attributes = True


class ShareholderCreate(BaseModel):
    name: str
    email: Optional[str]


class ShareholderRead(ShareholderCreate):
    id: int

    class Config:
        from_attributes = True


class UnitShareCreate(BaseModel):
    unit_id: int
    shareholder_id: int
    share_percentage: float


class UnitShareRead(UnitShareCreate):
    id: int

    class Config:
        from_attributes = True


class SalesRepresentativeCreate(BaseModel):
    name: str
    email: Optional[str]


class SalesRepresentativeRead(SalesRepresentativeCreate):
    id: int

    class Config:
        from_attributes = True


class AssignmentCreate(BaseModel):
    unit_id: int
    sales_representative_id: int


class AssignmentRead(BaseModel):
    id: int
    unit_id: int
    sales_representative_id: int
    assigned_at: datetime
    status: AssignmentStatus

    class Config:
        from_attributes = True


class AssignmentStatusUpdate(BaseModel):
    status: AssignmentStatus


class UnitStatusTransition(BaseModel):
    next_status: UnitStatus


class BulkUnitStatusUpdate(BaseModel):
    unit_ids: List[int]
    next_status: UnitStatus
