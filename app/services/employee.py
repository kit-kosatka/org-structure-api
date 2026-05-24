from sqlalchemy.ext.asyncio import AsyncSession
from app.services.department import DepartmentNotFound
from app.repositories import department as department_repo
from app.repositories import employee as employee_repo
from app.schemas.employee import EmployeeCreate
from app.models.employee import Employee


async def create_employee(
    dept_id: int, employee: EmployeeCreate, session: AsyncSession
) -> Employee:
    department = await department_repo.get_by_id(dept_id=dept_id, session=session)
    if not department:
        raise DepartmentNotFound()
    return await employee_repo.create(
        department_id=dept_id, employee=employee, session=session
    )
