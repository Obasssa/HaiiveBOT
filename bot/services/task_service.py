from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Task, UserTask


async def list_tasks(session: AsyncSession) -> list[Task]:
    return (
        (await session.execute(select(Task).where(Task.is_active == True)))
        .scalars()
        .all()
    )


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return (
        await session.execute(select(Task).where(Task.id == task_id))
    ).scalar_one_or_none()


async def is_completed(
    session: AsyncSession, telegram_id: int, task_id: int
) -> bool:
    """Once done, forever done (per-task)."""
    task = await get_task(session, task_id)
    if not task:
        return False

    stmt = select(UserTask).where(
        UserTask.user_id == telegram_id, UserTask.task_id == task_id
    )
    if task.once_per_day:
        cutoff = datetime.utcnow() - timedelta(hours=24)
        stmt = stmt.where(UserTask.completed_at >= cutoff)

    return (
        await session.execute(stmt)
    ).scalar_one_or_none() is not None


async def mark_completed(
    session: AsyncSession, telegram_id: int, task_id: int
):
    session.add(UserTask(user_id=telegram_id, task_id=task_id))
    await session.commit()
