from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentDetail
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import department as department_repo
from app.repositories import employee as employee_repo


class DepartmentNotFound(Exception):
    pass


class DepartmentNameConflict(Exception):
    pass


class DepartmentCycleError(Exception):
    pass


async def create_department(
    department: DepartmentCreate, session: AsyncSession
) -> Department:
    if department.parent_id is not None:
        parent = await department_repo.get_by_id(department.parent_id, session)
        if parent is None:
            raise DepartmentNotFound()
    existing = await department_repo.get_by_name_and_parent(
        name=department.name, parent_id=department.parent_id, session=session
    )
    if existing is not None:
        raise DepartmentNameConflict()
    return await department_repo.create(department=department, session=session)


async def get_department(
    dept_id: int, session: AsyncSession, depth: int = 1, include_employees: bool = True
) -> DepartmentDetail:
    depth = min(depth, 5)
    department = await department_repo.get_by_id(dept_id=dept_id, session=session)
    if department is None:
        raise DepartmentNotFound()
    employees = []
    if include_employees:
        employees = await employee_repo.get_by_department_id(dept_id, session)
    children = []
    if depth > 0:
        children_departments = await department_repo.get_children(
            parent_id=dept_id, session=session
        )
        for child in children_departments:
            child_detail = await get_department(
                dept_id=child.id,
                session=session,
                depth=depth - 1,
                include_employees=include_employees,
            )
            children.append(child_detail)
    return DepartmentDetail(
        id=department.id,
        name=department.name,
        parent_id=department.parent_id,
        created_at=department.created_at,
        employees=employees,
        children=children,
    )


async def update_department(
    dept_id: int, data: DepartmentUpdate, session: AsyncSession
):
    department = await department_repo.get_by_id(dept_id, session)
    if department is None:
        raise DepartmentNotFound()
    if data.parent_id is not None:
        if data.parent_id == dept_id:
            raise DepartmentCycleError()
        new_parent = await department_repo.get_by_id(data.parent_id, session)
        if new_parent is None:
            raise DepartmentNotFound()
        current = new_parent
        while current is not None:
            if current.id == dept_id:
                raise DepartmentCycleError()
            current = await department_repo.get_by_id(current.parent_id, session)
    return await department_repo.update(department, data, session)


async def delete_department(
    dept_id: int, mode: str, session: AsyncSession, reassign_to_id: int | None = None
) -> None:
    department = await department_repo.get_by_id(dept_id, session)
    if department is None:
        raise DepartmentNotFound()
    if mode == "reassign":
        if reassign_to_id is None:
            raise ValueError("reassign_to_id обязателен")
        target = await department_repo.get_by_id(reassign_to_id, session)
        if target is None:
            raise DepartmentNotFound()
        await employee_repo.reassign(dept_id, reassign_to_id, session)
        await department_repo.delete(department, session)
    elif mode == "cascade":
        return await department_repo.delete(department, session)
