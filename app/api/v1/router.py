from fastapi import APIRouter
from app.api.v1.endpoints.department import router as department_router
from app.api.v1.endpoints.employee import router as employee_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(department_router)
api_router.include_router(employee_router)