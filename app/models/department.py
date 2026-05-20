from sqlalchemy import ForeignKey, String, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date

class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column( String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('departments.id', ondelete='CASCADE'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    children: Mapped[list["Department"]] = relationship("Department", cascade="all, delete-orphan")
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="department", cascade="all, delete-orphan")

class Employee(Base):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id', ondelete='CASCADE'), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    department: Mapped[Department] = relationship("Department", back_populates="employees")