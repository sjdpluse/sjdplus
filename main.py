"""
ApexTrade Telegram Bot — ربات رسمی اپکس‌ترید
Powered by: FastAPI + Groq + Supabase
Deploy: Railway.app
"""

import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from core.telegram import TelegramClient
from handlers.router import handle_update

app = FastAPI(title="ApexTrade Bot", version="2.0.0")
telegram = TelegramClient()


@app.on_event("startup")
async def startup():
    """Register webhook on startup"""
    webhook_url = f"{settings.WEBHOOK_URL}/webhook/{settings.WEBHOOK_SECRET}"
    result = await telegram.set_webhook(webhook_url)
    print(f"✅ Webhook set: {result}")
    # Set bot commands menu
    await telegram.set_my_commands([
        {"command": "start",   "description": "🚀 شروع / خوش آمدید"},
        {"command": "help",    "description": "📖 راهنما و امکانات"},
        {"command": "price",   "description": "💰 قیمت لحظه‌ای کریپتو"},
        {"command": "market",  "description": "📊 نمای کلی بازار"},
        {"command": "course",  "description": "🎓 دوره‌های ApexTrade"},
        {"command": "ask",     "description": "🤖 سوال از هوش مصنوعی"},
        {"command": "news",    "description": "📰 آخرین اخبار کریپتو"},
        {"command": "calc",    "description": "🧮 حساب‌گر P&L و ریسک"},
        {"command": "admin",   "description": "⚙️ پنل مدیریت (ادمین)"},
    ])


@app.get("/")
async def root():
    return {"status": "🟢 ApexTrade Bot is running", "version": "2.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        update = await request.json()
        asyncio.create_task(handle_update(update))
        return JSONResponse({"ok": True})
    except Exception as e:
        print(f"Webhook error: {e}")
        return JSONResponse({"ok": False})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
