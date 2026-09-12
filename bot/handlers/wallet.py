from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.database.session import SessionLocal
from bot.keyboards.main_menu import bottom_menu, wallet_inline
from bot.services.user_service import get_user

router = Router()


@router.message(F.text == "💼 Wallet")
async def wallet_msg(message: Message):
    async with SessionLocal() as session:
        user = await get_user(session, message.from_user.id)

    text = (
        f"🐝 <b>HaiiveBOT</b>\n\n"
        f"<b>Available balance</b>\n"
        f"<b>{user.balance:,.2f} USDT</b>\n"
        f"▲ {user.today_earned:.2f} today"
    )
    await message.answer(text, reply_markup=wallet_inline(), parse_mode="HTML")


@router.callback_query(F.data == "wallet")
async def wallet_cb(callback: CallbackQuery):
    async with SessionLocal() as session:
        user = await get_user(session, callback.from_user.id)

    text = (
        f"🐝 <b>HaiiveBOT</b>\n\n"
        f"<b>Available balance</b>\n"
        f"<b>{user.balance:,.2f} USDT</b>\n"
        f"▲ {user.today_earned:.2f} today"
    )
    await callback.message.edit_text(
        text, reply_markup=wallet_inline(), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery):
    await callback.message.answer(
        "💸 <b>Withdraw</b>\n\nMinimum: 1.00 USDT\nSend your wallet address:",
        parse_mode="HTML",
    )
    await callback.answer()
