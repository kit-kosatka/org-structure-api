from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services import employee as employee_service
from app.services.department import DepartmentNotFound

router = APIRouter(prefix="/departments", tags=["employees"])

@router.post("/{dept_id}/employees/", response_model=EmployeeRead)
async def create_employee(dept_id: int, employee: EmployeeCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await employee_service.create_employee(dept_id, employee, session)
    except DepartmentNotFound:
        raise HTTPException(status_code=404, detail="Department not found")