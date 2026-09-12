from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

ANNOUNCEMENT_URL = "https://sharexosialx.com/g1LXEr6xw"


def bottom_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💼 Wallet"),
                KeyboardButton(text="✅ Tasks"),
                KeyboardButton(text="👥 Invite"),
            ]
        ],
        resize_keyboard=True,
    )


def wallet_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw"),
                # Change: now a URL button, opens Chrome directly
                InlineKeyboardButton(
                    text="🎁 Invite & earn",
                    url=ANNOUNCEMENT_URL,
                ),
            ]
        ]
    )


def tasks_inline(tasks_with_status: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for t in tasks_with_status:
        if t["done"]:
            rows.append(
                [
                    InlineKeyboardButton(
                        text=f"✅ {t['title']} — Done",
                        callback_data="task_done",
                    )
                ]
            )
        elif t.get("url"):
            rows.append(
                [
                    InlineKeyboardButton(
                        text=f"{t['icon']} {t['title']}  +{t['reward']:.2f}",
                        url=t["url"],
                    )
                ]
            )
            rows.append(
                [
                    InlineKeyboardButton(
                        text="✅ I've completed this",
                        callback_data=f"task_claim:{t['id']}",
                    )
                ]
            )
        else:
            rows.append(
                [
                    InlineKeyboardButton(
                        text=f"{t['icon']} {t['title']}  +{t['reward']:.2f}",
                        callback_data=f"task_open:{t['id']}",
                    )
                ]
            )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def task_action(task_id: int, url: str) -> InlineKeyboardMarkup:
    rows = []
    if url:
        rows.append([InlineKeyboardButton(text="🔗 Open link", url=url)])
    rows.append(
        [
            InlineKeyboardButton(
                text="✅ I've completed this task",
                callback_data=f"task_claim:{task_id}",
            )
        ]
    )
    rows.append([InlineKeyboardButton(text="⬅️ Back", callback_data="tasks")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def referral_inline(bot_username: str, telegram_id: int) -> InlineKeyboardMarkup:
    """
    Invite page keyboard — now points to the same URL as the announcement.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Open link",
                    url=ANNOUNCEMENT_URL,
                )
            ],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="wallet")],
        ]
    )
