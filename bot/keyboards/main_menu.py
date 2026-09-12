from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


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
                InlineKeyboardButton(text="🎁 Invite & earn", callback_data="referral"),
            ]
        ]
    )


def tasks_inline(tasks_with_status: list[dict]) -> InlineKeyboardMarkup:
    """
    URL tasks: a URL button (opens Chrome) + a claim button below.
    Other tasks: a callback button that opens the detail view.
    Done tasks: a single grey 'Done' button.
    """
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
    link = f"https://t.me/{bot_username}?start=ref{telegram_id}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Copy link",
                    url=f"https://t.me/share/url?url={link}",
                )
            ],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="wallet")],
        ]
    )
