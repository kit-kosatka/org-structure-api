from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentDetail,
    DepartmentUpdate,
)
from app.services import department as department_service
from app.services.department import (
    DepartmentNotFound,
    DepartmentNameConflict,
    DepartmentCycleError,
)

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/", response_model=DepartmentRead)
async def create_department(
    department: DepartmentCreate, db: AsyncSession = Depends(get_db)
):
    try:
        return await department_service.create_department(department, db)
    except DepartmentNotFound:
        raise HTTPException(status_code=404, detail="Parent department not found")
    except DepartmentNameConflict:
        raise HTTPException(
            status_code=409, detail="Department with this name already exists"
        )


@router.get("/{dept_id}", response_model=DepartmentDetail)
async def get_department(
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    depth: int = 1,
    include_employees: bool = True,
    sort_by: str = "created_at",
):
    try:
        return await department_service.get_department(
            dept_id, db, depth, include_employees, sort_by
        )
    except DepartmentNotFound:
        raise HTTPException(status_code=404, detail="Department not found")


@router.patch("/{dept_id}", response_model=DepartmentRead)
async def update_department(
    dept_id: int, data: DepartmentUpdate, session: AsyncSession = Depends(get_db)
):
    try:
        return await department_service.update_department(dept_id, data, session)
    except DepartmentNotFound:
        raise HTTPException(status_code=404, detail="Department not found")
    except DepartmentCycleError:
        raise HTTPException(status_code=409, detail="Department cycle")


@router.delete("/{dept_id}", status_code=204)
async def delete_department(
    dept_id: int,
    mode: str,
    session: AsyncSession = Depends(get_db),
    reassign_to_id: int | None = None,
):
    try:
        return await department_service.delete_department(
            dept_id, mode, session, reassign_to_id
        )
    except DepartmentNotFound:
        raise HTTPException(status_code=404, detail="Department not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
