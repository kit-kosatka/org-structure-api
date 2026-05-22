from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.employee import EmployeeRead


class DepartmentCreate(BaseModel):
    name: str
    parent_id: int | None = None


class DepartmentRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class DepartmentDetail(DepartmentRead):
    employees: list[EmployeeRead] = Field(default_factory=list)
    children: list["DepartmentDetail"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
