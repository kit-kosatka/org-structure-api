from sqlalchemy import select
from app.models.department import Department, Employee
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentRead, DepartmentDetail

from sqlalchemy.ext.asyncio import AsyncSession


class DepartmentNotFound(Exception):
    pass

class DepartmentNameConflict(Exception):
    pass

async def create_department(department: DepartmentCreate, session: AsyncSession) -> Department:
    if department.parent_id is not None:
        result = await session.execute(select(Department).where(Department.id == department.parent_id))
        parent = result.scalar_one_or_none()
        if parent is None:
            raise DepartmentNotFound()
    result = await session.execute(select(Department).where(Department.name == department.name, Department.parent_id == department.parent_id))
    existing = result.scalar_one_or_none()
    if existing is not None:
        raise DepartmentNameConflict()
    new_department = Department(name=department.name, parent_id=department.parent_id)
    session.add(new_department)
    await session.commit()
    await session.refresh(new_department)
    return new_department


async def get_department(dept_id: int, session: AsyncSession, depth: int = 1, include_employees: bool = True) -> DepartmentDetail:
    result = await session.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if dept is None:
        raise DepartmentNotFound()
    if include_employees:
        result = await session.execute(select(Employee).where(Employee.department_id == dept_id))
        employees = result.scalars().all()
    if depth > 0:
        result = await session.execute(select(Department).where(Department.parent_id == dept_id))
        children_depts = result.scalars().all()
    children = []
    for child in children_depts:
        child_detail = await get_department(child.id, session, depth - 1, include_employees=include_employees)
        children.append(child_detail)




