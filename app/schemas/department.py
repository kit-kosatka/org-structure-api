from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.employee import EmployeeRead


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name не может быть пустым")
        return v


class DepartmentRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("name не может быть пустым")
        return v


class DepartmentDetail(DepartmentRead):
    employees: list[EmployeeRead] = Field(default_factory=list)
    children: list["DepartmentDetail"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
