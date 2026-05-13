"""
سرویس هوش مصنوعی Groq — مدل llama-3.3-70b-versatile
"""

import httpx
from config import settings

GROQ_API = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """تو دستیار هوشمند رسمی <b>اپکس‌ترید (ApexTrade)</b> هستی — پیشرفته‌ترین پلتفرم آموزش ترید و کریپتو برای جامعه فارسی‌زبان، به رهبری استاد سجاد.

🎯 <b>شخصیت تو:</b>
- حرفه‌ای، دوستانه، صادق و آموزش‌محور
- از دری/فارسی روان استفاده می‌کنی
- پاسخ‌ها مختصر، کاربردی و با ایموجی مناسب
- نه سطحی، نه خیلی پیچیده — سطح مخاطب را درک می‌کنی

📚 <b>موضوعاتی که پوشش می‌دهی:</b>
- کریپتوکارنسی: بیت‌کوین، اتریوم، آلتکوین‌ها، استیبل‌کوین‌ها
- تحلیل تکنیکال: کندل‌ها، EMA/RSI/MACD، الگوهای قیمتی، support/resistance
- مدیریت ریسک: position sizing، stop-loss، R/R ratio
- روانشناسی ترید: FOMO، FUD، طمع، انضباط
- صرافی‌ها: CEX (بایننس، کوینکس)، DEX (یونیسواپ)، KYC
- والت‌ها: seed phrase، hardware wallet، امنیت
- DeFi، NFT، Web3، استیکینگ
- بازارهای اسپات و فیوچرز

🎓 <b>درباره دوره‌های ApexTrade:</b>
- دوره جامع مبتدی تا پیشرفته (۱۵+ روز)
- تدریس زنده از طریق Google Meet
- تمرکز بر روانشناسی + تکنیکال + مدیریت سرمایه
- فلسفه آموزش: ۸۰٪ روانشناسی، ۲۰٪ استراتژی
- برای ثبت‌نام: با استاد سجاد تماس بگیرید

⚠️ <b>قوانین مهم:</b>
1. هرگز سیگنال مستقیم خرید/فروش نده
2. همیشه تأکید کن که ترید ریسک دارد
3. توصیه‌های مالی شخصی نده
4. اگر سوالی خارج از حوزه بود، صادقانه بگو
5. اطلاعات دوره ApexTrade را معرفی کن

پاسخ‌هایت در تلگرام نمایش داده می‌شوند، از HTML formatting استفاده کن (<b>bold</b>, <i>italic</i>, <code>code</code>) اما Markdown نه."""


async def get_ai_response(
    user_message: str,
    conversation_history: list[dict],
    user_name: str = "کاربر"
) -> str:
    """
    دریافت پاسخ از Groq AI
    conversation_history: لیست دیکشنری‌های {role, content}
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # اضافه کردن تاریخچه مکالمه
    for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # پیام جدید کاربر
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": messages,
        "max_tokens": settings.GROQ_MAX_TOKENS,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(GROQ_API, headers=headers, json=payload)
            data = response.json()

        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"].strip()
        else:
            error = data.get("error", {}).get("message", "خطای ناشناخته")
            print(f"Groq error: {error}")
            return "⚠️ در این لحظه مشکلی پیش آمد. لطفاً دوباره امتحان کنید."

    except httpx.TimeoutException:
        return "⏱️ پاسخ طولانی شد. لطفاً دوباره بپرسید."
    except Exception as e:
        print(f"Groq exception: {e}")
        return "⚠️ خطا در اتصال به هوش مصنوعی. لطفاً چند لحظه دیگر امتحان کنید."


async def analyze_market_context(coin: str, price_data: dict) -> str:
    """تحلیل ساده بازار برای یک کوین"""
    prompt = f"""
    داده‌های فعلی {coin}:
    - قیمت: ${price_data.get('price', 'N/A')}
    - تغییر ۲۴ ساعته: {price_data.get('change_24h', 'N/A')}%
    - بالاترین ۲۴ ساعت: ${price_data.get('high_24h', 'N/A')}
    - پایین‌ترین ۲۴ ساعت: ${price_data.get('low_24h', 'N/A')}
    - حجم بازار: ${price_data.get('market_cap', 'N/A')}
    
    یک تحلیل کوتاه آموزشی (۳-۴ جمله) از وضعیت فعلی بازار ارائه بده. 
    تأکید کن که این تحلیل آموزشی است، نه توصیه سرمایه‌گذاری.
    """
    messages = [{"role": "user", "content": prompt}]
    return await get_ai_response(prompt, [], "تحلیلگر")
