"""
سرویس دیتابیس Supabase
"""

import httpx
import json
from datetime import datetime, timezone
from config import settings

SUPA_URL = settings.SUPABASE_URL
SUPA_KEY = settings.SUPABASE_KEY

HEADERS = {
    "apikey": SUPA_KEY,
    "Authorization": f"Bearer {SUPA_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


async def _req(method: str, path: str, data: dict = None, params: dict = None) -> dict | list | None:
    url = f"{SUPA_URL}/rest/v1/{path}"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.request(method, url, headers=HEADERS, json=data, params=params)
        if r.status_code in (200, 201):
            return r.json()
        print(f"Supabase error {r.status_code}: {r.text}")
        return None


# ─── کاربران ─────────────────────────────────────────────────────────────────

async def upsert_user(user: dict) -> dict | None:
    """ذخیره یا بروزرسانی کاربر"""
    data = {
        "telegram_id": user["id"],
        "username":    user.get("username"),
        "first_name":  user.get("first_name"),
        "last_name":   user.get("last_name"),
        "last_seen":   datetime.now(timezone.utc).isoformat(),
    }
    return await _req("POST", "bot_users", data, {"on_conflict": "telegram_id"})


async def get_user(telegram_id: int) -> dict | None:
    result = await _req("GET", "bot_users", params={"telegram_id": f"eq.{telegram_id}", "limit": "1"})
    return result[0] if result else None


async def get_all_users() -> list[dict]:
    result = await _req("GET", "bot_users", params={"is_blocked": "eq.false", "select": "telegram_id,first_name"})
    return result or []


async def block_user(telegram_id: int, blocked: bool = True) -> None:
    await _req("PATCH", f"bot_users?telegram_id=eq.{telegram_id}", {"is_blocked": blocked})


async def get_user_count() -> int:
    result = await _req("GET", "bot_users", params={"select": "count", "head": "true"})
    return result if isinstance(result, int) else 0


# ─── تاریخچه مکالمه ──────────────────────────────────────────────────────────

async def get_conversation(telegram_id: int) -> list[dict]:
    result = await _req("GET", "bot_conversations", params={
        "telegram_id": f"eq.{telegram_id}",
        "limit": "1",
    })
    if result:
        return result[0].get("messages", [])
    return []


async def save_conversation(telegram_id: int, messages: list[dict]) -> None:
    # نگه داشتن آخرین N پیام
    from config import settings
    messages = messages[-settings.MAX_CONVERSATION_HISTORY:]
    data = {
        "telegram_id": telegram_id,
        "messages": messages,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    await _req("POST", "bot_conversations", data, {"on_conflict": "telegram_id"})


async def clear_conversation(telegram_id: int) -> None:
    await _req("PATCH", f"bot_conversations?telegram_id=eq.{telegram_id}", {"messages": []})


# ─── Rate Limiting ────────────────────────────────────────────────────────────

async def check_rate_limit(telegram_id: int) -> bool:
    """True = مجاز، False = تجاوز از حد"""
    from config import settings
    result = await _req("GET", "bot_rate_limits", params={
        "telegram_id": f"eq.{telegram_id}",
        "limit": "1",
    })
    now = datetime.now(timezone.utc)
    if not result:
        await _req("POST", "bot_rate_limits", {
            "telegram_id": telegram_id,
            "count": 1,
            "window_start": now.isoformat(),
        })
        return True

    row = result[0]
    window_start = datetime.fromisoformat(row["window_start"])
    diff_hours = (now - window_start).total_seconds() / 3600

    if diff_hours >= 1:
        # پنجره جدید
        await _req("PATCH", f"bot_rate_limits?telegram_id=eq.{telegram_id}", {
            "count": 1,
            "window_start": now.isoformat(),
        })
        return True

    if row["count"] >= settings.RATE_LIMIT_PER_HOUR:
        return False

    await _req("PATCH", f"bot_rate_limits?telegram_id=eq.{telegram_id}", {
        "count": row["count"] + 1,
    })
    return True


# ─── آمار ────────────────────────────────────────────────────────────────────

async def log_message(telegram_id: int, msg_type: str = "text") -> None:
    await _req("POST", "bot_message_logs", {
        "telegram_id": telegram_id,
        "type": msg_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })


async def get_stats() -> dict:
    users = await _req("GET", "bot_users", params={"select": "count"})
    return {
        "total_users": users[0]["count"] if users else 0,
    }
