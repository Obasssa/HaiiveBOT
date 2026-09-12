FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy EVERYTHING (including the bot/ folder)
COPY . .

# Debug: list files so you can see what's inside the container
RUN ls -la /app && ls -la /app/bot

CMD ["python", "-m", "bot.main"]
