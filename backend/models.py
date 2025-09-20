"""SQLAlchemy models for the real estate domain."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base class."""


class ProjectStatus(str, Enum):
    """Lifecycle of a project."""

    PLANNING = "planning"
    APPROVED = "approved"
    CONSTRUCTION = "construction"
    SALES = "sales"
    COMPLETED = "completed"


class UnitStatus(str, Enum):
    """Lifecycle of an independent unit."""

    DESIGN = "design"
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"
    TRANSFERRED = "transferred"


class AssignmentStatus(str, Enum):
    """Status of a sales representative assignment."""

    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LandOwner(Base):
    """Land owner participating in one or more projects."""

    __tablename__ = "land_owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_info: Mapped[Optional[str]] = mapped_column(String(255))

    projects: Mapped[List["Project"]] = relationship(
        back_populates="land_owner", cascade="all, delete-orphan"
    )


class Project(Base):
    """A real estate development project."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[ProjectStatus] = mapped_column(
        SAEnum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False
    )
    land_owner_id: Mapped[int] = mapped_column(ForeignKey("land_owners.id"), nullable=False)

    land_owner: Mapped[LandOwner] = relationship(back_populates="projects")
    units: Mapped[List["Unit"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Unit(Base):
    """Independent unit (bağımsız bölüm) within a project."""

    __tablename__ = "units"
    __table_args__ = (UniqueConstraint("project_id", "unit_number", name="uq_unit_number"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    unit_number: Mapped[str] = mapped_column(String(50), nullable=False)
    floor: Mapped[Optional[int]] = mapped_column(Integer)
    area_sqm: Mapped[Optional[float]] = mapped_column(Float)
    status: Mapped[UnitStatus] = mapped_column(
        SAEnum(UnitStatus), default=UnitStatus.DESIGN, nullable=False
    )

    project: Mapped[Project] = relationship(back_populates="units")
    shares: Mapped[List["UnitShare"]] = relationship(
        back_populates="unit", cascade="all, delete-orphan"
    )
    assignments: Mapped[List["SalesAssignment"]] = relationship(
        back_populates="unit", cascade="all, delete-orphan"
    )


class Shareholder(Base):
    """An investor that owns shares of a unit."""

    __tablename__ = "shareholders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))

    unit_shares: Mapped[List["UnitShare"]] = relationship(
        back_populates="shareholder", cascade="all, delete-orphan"
    )


class UnitShare(Base):
    """Join table for unit share ownership."""

    __tablename__ = "unit_shares"
    __table_args__ = (
        UniqueConstraint("unit_id", "shareholder_id", name="uq_unit_share_owner"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    shareholder_id: Mapped[int] = mapped_column(ForeignKey("shareholders.id"), nullable=False)
    share_percentage: Mapped[float] = mapped_column(Float, nullable=False)

    unit: Mapped[Unit] = relationship(back_populates="shares")
    shareholder: Mapped[Shareholder] = relationship(back_populates="unit_shares")


class SalesRepresentative(Base):
    """Sales personnel that can be assigned to units."""

    __tablename__ = "sales_representatives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))

    assignments: Mapped[List["SalesAssignment"]] = relationship(
        back_populates="sales_representative", cascade="all, delete-orphan"
    )


class SalesAssignment(Base):
    """Assignment of a sales representative to a unit."""

    __tablename__ = "sales_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    sales_representative_id: Mapped[int] = mapped_column(
        ForeignKey("sales_representatives.id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[AssignmentStatus] = mapped_column(
        SAEnum(AssignmentStatus), default=AssignmentStatus.ACTIVE, nullable=False
    )

    unit: Mapped[Unit] = relationship(back_populates="assignments")
    sales_representative: Mapped[SalesRepresentative] = relationship(back_populates="assignments")
