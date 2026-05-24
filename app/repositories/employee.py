from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


async def get_department_employees(
    department_id: int, session: AsyncSession
) -> list[Employee]:
    result = await session.execute(
        select(Employee).where(Employee.department_id == department_id)
    )
    return result.scalars().all()


async def create(
    employee: EmployeeCreate, department_id: int, session: AsyncSession
) -> Employee:
    new_employee = Employee(
        full_name=employee.full_name,
        position=employee.position,
        hired_at=employee.hired_at,
        department_id=department_id,
    )
    session.add(new_employee)
    await session.commit()
    await session.refresh(new_employee)
    return new_employee
