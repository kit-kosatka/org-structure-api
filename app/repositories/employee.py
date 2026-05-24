from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


async def get_by_department_id(
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


async def reassign(from_dept_id: int, to_dept_id: int, session: AsyncSession) -> None:
    await session.execute(
        update(Employee)
        .where(Employee.department_id == from_dept_id)
        .values(department_id=to_dept_id)
    )
    await session.commit()