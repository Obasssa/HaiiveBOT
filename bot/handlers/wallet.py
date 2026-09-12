import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.models import Withdrawal
from bot.database.session import SessionLocal
from bot.keyboards.main_menu import wallet_inline
from bot.services.user_service import get_user

router = Router()

MIN_WITHDRAW = 1.0


class WithdrawFlow(StatesGroup):
    waiting_address = State()


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
async def withdraw_start(callback: CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, callback.from_user.id)

    if user.balance < MIN_WITHDRAW:
        await callback.answer(
            f"⚠️ Minimum withdrawal is {MIN_WITHDRAW:.2f} USDT",
            show_alert=True,
        )
        return

    await state.set_state(WithdrawFlow.waiting_address)
    await callback.message.answer(
        f"💸 <b>Withdraw</b>\n\n"
        f"Balance: <b>{user.balance:.2f} USDT</b>\n"
        f"Minimum: <b>{MIN_WITHDRAW:.2f} USDT</b>\n\n"
        f"Please send your USDT wallet address (TRC20):",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(WithdrawFlow.waiting_address)
async def withdraw_receive_address(message: Message, state: FSMContext):
    address = (message.text or "").strip()

    # Basic validation — Tron addresses start with T and are 34 chars
    if not re.fullmatch(r"T[1-9A-HJ-NP-Za-km-z]{33}", address):
        await message.answer(
            "❌ That doesn't look like a valid USDT (TRC20) address.\n"
            "It should start with <b>T</b> and be 34 characters long.\n\n"
            "Please send it again:",
            parse_mode="HTML",
        )
        return

    async with SessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        amount = user.balance  # withdraw everything

        w = Withdrawal(
            user_id=message.from_user.id,
            amount=amount,
            address=address,
            status="pending",
        )
        session.add(w)
        user.balance = 0.0
        await session.commit()

    await state.clear()
    await message.answer(
        f"✅ <b>Withdrawal request received</b>\n\n"
        f"Amount: <b>{amount:.2f} USDT</b>\n"
        f"Address: <code>{address}</code>\n\n"
        f"Status: <b>Pending review</b>\n"
        f"We'll process it shortly.",
        parse_mode="HTML",
    )
