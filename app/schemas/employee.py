from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


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