from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.database.session import SessionLocal
from bot.keyboards.main_menu import main_menu
from bot.services.wallet_service import generate_deposit_address, get_balance

router = Router()


@router.callback_query(F.data == "wallet")
async def show_wallet(callback: CallbackQuery):
    async with SessionLocal() as session:
        balance = await get_balance(session, callback.from_user.id)
        address = await generate_deposit_address(callback.from_user.id)

    await callback.message.edit_text(
        f"💰 <b>Your Wallet</b>\n\n"
        f"Balance: <b>{balance:.2f} USDT</b>\n\n"
        f"Deposit address:\n<code>{address}</code>\n\n"
        f"⚠️ Deposits are credited after network confirmation.",
        parse_mode="HTML",
    )
    await callback.answer()
