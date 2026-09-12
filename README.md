# 🐝 HaiiveBOT

Telegram wallet + tasks + referral bot. Built with aiogram 3, PostgreSQL, Railway.

## Features
- 💰 Wallet with balance
- 🎯 Tasks with rewards
- 🎁 Referral program
- 👤 User profiles
- 🛠 Admin panel

## Deploy on Railway

1. Push this repo to GitHub.
2. Create a new Railway project → **Deploy from GitHub repo**.
3. Add a **PostgreSQL** plugin to your project.
4. In Railway → **Variables**, add:
   - `BOT_TOKEN` — from @BotFather
   - `DATABASE_URL` — copy from Postgres plugin (change `postgresql://` to `postgresql+asyncpg://`)
   - `ADMIN_IDS` — your Telegram user ID
   - `REFERRAL_BONUS` — e.g. `0.10`
5. Railway auto-deploys. Check logs for `🐝 HaiiveBOT is live!`

## Local Run
```bash
pip install -r requirements.txt
cp .env.example .env  # fill values
python -m bot.main
