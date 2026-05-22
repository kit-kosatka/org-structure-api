from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


async def get_by_id(dept_id: int, session: AsyncSession) -> Department | None:
    result = await session.execute(select(Department).where(Department.id == dept_id))
    return result.scalars().first()

async def get_children(parent_id: int, session: AsyncSession) -> list[Department]:
    result = await session.execute(select(Department).where(Department.parent_id == parent_id))
    return result.scalars().all()

async def get_by_name_and_parent(name: str, parent_id: int | None, session: AsyncSession) -> Department | None:
    result = await session.execute(select(Department).where(Department.name == name, Department.parent_id == parent_id))
    return result.scalars().first()

async def create(department: DepartmentCreate, session: AsyncSession) -> Department:
    new_department = Department(name=department.name, parent_id=department.parent_id)
    session.add(new_department)
    await session.commit()
    await session.refresh(new_department)
    return new_department

async def update(department: Department, data: DepartmentUpdate, session: AsyncSession) -> Department:
    if data.name is not None:
        department.name = data.name
    if data.parent_id is not None:
        department.parent_id = data.parent_id
    await session.commit()
    await session.refresh(department)
    return department

async def delete(department: Department, session: AsyncSession) -> None:
    await session.delete(department)
    await session.commit()
