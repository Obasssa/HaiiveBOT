from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.database.session import SessionLocal
from bot.keyboards.main_menu import task_action, tasks_inline
from bot.services.task_service import (
    get_task,
    is_completed,
    list_tasks,
    mark_completed,
)
from bot.services.user_service import add_balance

router = Router()


@router.message(F.text == "✅ Tasks")
async def tasks_msg(message: Message):
    await _render_tasks(message.from_user.id, message.answer)


@router.callback_query(F.data == "tasks")
async def tasks_cb(callback: CallbackQuery):
    await _render_tasks(callback.from_user.id, callback.message.edit_text)
    await callback.answer()


async def _render_tasks(user_id: int, sender):
    async with SessionLocal() as session:
        tasks = await list_tasks(session)
        rows = []
        for t in tasks:
            rows.append(
                {
                    "id": t.id,
                    "icon": t.icon,
                    "title": t.title,
                    "reward": t.reward,
                    "done": await is_completed(session, user_id, t.id),
                }
            )

    text = (
        "🐝 <b>HaiiveBOT</b>\n\n"
        "<b>Today's tasks</b>\n"
        "Complete tasks to earn USDT instantly."
    )
    await sender(text, reply_markup=tasks_inline(rows), parse_mode="HTML")


@router.callback_query(F.data.startswith("task_open:"))
async def open_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    async with SessionLocal() as session:
        task = await get_task(session, task_id)
        done = await is_completed(session, callback.from_user.id, task_id)

    text = (
        f"{task.icon} <b>{task.title}</b>\n\n"
        f"{task.subtitle}\n\n"
        f"Reward: <b>+{task.reward:.2f} USDT</b>"
    )
    if done:
        await callback.message.edit_text(
            text + "\n\n✅ Already completed.",
            reply_markup=task_action(task_id, ""),
            parse_mode="HTML",
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=task_action(task_id, task.url),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("task_claim:"))
async def claim_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    async with SessionLocal() as session:
        if await is_completed(session, callback.from_user.id, task_id):
            await callback.answer("Already done ✅", show_alert=True)
            return
        task = await get_task(session, task_id)
        await mark_completed(session, callback.from_user.id, task_id)
        await add_balance(
            session,
            callback.from_user.id,
            task.reward,
            icon=task.icon,
            label=task.title,
        )

    await callback.answer(f"+{task.reward:.2f} USDT ✅", show_alert=True)
    await _render_tasks(callback.from_user.id, callback.message.edit_text)
