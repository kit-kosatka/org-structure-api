from sqlalchemy.ext.asyncio import AsyncSession



async def reassign(from_dept_id: int, to_dept_id: int, session: AsyncSession) -> None:
