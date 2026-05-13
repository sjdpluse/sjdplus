"""
کیبوردهای اینلاین و ریپلای برای ربات
"""


def main_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "💰 قیمت کریپتو", "callback_data": "menu_price"},
                {"text": "📊 بازار", "callback_data": "menu_market"},
            ],
            [
                {"text": "🎓 دوره‌های ApexTrade", "callback_data": "menu_course"},
                {"text": "🤖 سوال از AI", "callback_data": "menu_ask"},
            ],
            [
                {"text": "📰 اخبار", "callback_data": "menu_news"},
                {"text": "🧮 حساب‌گر ریسک", "callback_data": "menu_calc"},
            ],
            [
                {"text": "📞 ارتباط با استاد", "callback_data": "menu_contact"},
                {"text": "ℹ️ درباره ApexTrade", "callback_data": "menu_about"},
            ],
        ]
    }


def price_menu() -> dict:
    coins = [
        ("₿ Bitcoin", "price_btc"),
        ("Ξ Ethereum", "price_eth"),
        ("◎ Solana", "price_sol"),
        ("🔵 BNB", "price_bnb"),
        ("🔴 XRP", "price_xrp"),
        ("🟡 USDT", "price_usdt"),
    ]
    rows = [[{"text": name, "callback_data": cb} for name, cb in coins[i:i+2]]
            for i in range(0, len(coins), 2)]
    rows.append([
        {"text": "🔍 جستجوی کوین دیگر", "callback_data": "price_search"},
        {"text": "🔙 برگشت", "callback_data": "back_main"},
    ])
    return {"inline_keyboard": rows}


def course_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "📚 سرفصل دوره کامل", "callback_data": "course_syllabus"}],
            [{"text": "🏁 دوره مبتدی (روز ۱-۵)", "callback_data": "course_beginner"}],
            [{"text": "📈 تحلیل تکنیکال (روز ۶-۱۲)", "callback_data": "course_technical"}],
            [{"text": "🔥 الگوهای پیشرفته (روز ۱۳+)", "callback_data": "course_advanced"}],
            [{"text": "💎 ثبت‌نام در دوره", "callback_data": "course_enroll"}],
            [{"text": "🔙 برگشت", "callback_data": "back_main"}],
        ]
    }


def market_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "📊 نمای کلی", "callback_data": "market_overview"},
                {"text": "🔥 Trending", "callback_data": "market_trending"},
            ],
            [
                {"text": "🟢 برترین‌ها", "callback_data": "market_gainers"},
                {"text": "🔴 بیشترین افت", "callback_data": "market_losers"},
            ],
            [
                {"text": "😱 Fear & Greed", "callback_data": "market_fear"},
                {"text": "🔙 برگشت", "callback_data": "back_main"},
            ],
        ]
    }


def calc_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "📉 محاسبه ریسک/ریوارد", "callback_data": "calc_rr"}],
            [{"text": "💵 محاسبه حجم پوزیشن", "callback_data": "calc_position"}],
            [{"text": "📊 محاسبه P&L", "callback_data": "calc_pnl"}],
            [{"text": "🔙 برگشت", "callback_data": "back_main"}],
        ]
    }


def back_main() -> dict:
    return {"inline_keyboard": [[{"text": "🏠 منوی اصلی", "callback_data": "back_main"}]]}


def confirm_broadcast() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "✅ تأیید ارسال", "callback_data": "broadcast_confirm"},
                {"text": "❌ لغو", "callback_data": "broadcast_cancel"},
            ]
        ]
    }


def admin_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "📢 ارسال همگانی", "callback_data": "admin_broadcast"},
                {"text": "📊 آمار ربات", "callback_data": "admin_stats"},
            ],
            [
                {"text": "👥 مدیریت کاربران", "callback_data": "admin_users"},
                {"text": "📝 دانش‌نامه", "callback_data": "admin_kb"},
            ],
            [{"text": "🔙 برگشت", "callback_data": "back_main"}],
        ]
    }
