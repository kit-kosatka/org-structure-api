from sqlalchemy import ForeignKey, String, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    parent: Mapped["Department | None"] = relationship(
        "Department", remote_side="Department.id", back_populates="children"
    )
    children: Mapped[list["Department"]] = relationship(
        "Department", back_populates="parent", cascade="all"
    )
    employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="department", cascade="all, delete-orphan"
    )
