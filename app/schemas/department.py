from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str
    parent_id: int | None

class DepartmentRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DepartmentUpdate(BaseModel):
    name: str | None
    parent_id: int | None

class EmployeeCreate(BaseModel):
    full_name: str
    position: str
    hired_at: date | None = None

class EmployeeRead(BaseModel):
    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DepartmentDetail(DepartmentRead):
    employees: list[EmployeeRead] = []
    children: list["DepartmentDetail"] = []

    model_config = ConfigDict(from_attributes=True)
