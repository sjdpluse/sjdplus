"""
سرویس داده‌های بازار کریپتو — CoinGecko API (رایگان)
"""

import httpx
from config import settings

COIN_IDS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "usdt": "tether",
    "ada": "cardano",
    "doge": "dogecoin",
    "avax": "avalanche-2",
    "dot": "polkadot",
    "link": "chainlink",
    "matic": "matic-network",
    "ton": "the-open-network",
    "shib": "shiba-inu",
    "trx": "tron",
    "ltc": "litecoin",
    "near": "near",
    "op": "optimism",
    "arb": "arbitrum",
}

COIN_SYMBOLS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "binancecoin": "BNB",
    "ripple": "XRP",
    "tether": "USDT",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "avalanche-2": "AVAX",
    "polkadot": "DOT",
    "chainlink": "LINK",
    "matic-network": "MATIC",
    "the-open-network": "TON",
    "shiba-inu": "SHIB",
    "tron": "TRX",
    "litecoin": "LTC",
    "near": "NEAR",
    "optimism": "OP",
    "arbitrum": "ARB",
}


def format_price(price: float) -> str:
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.4f}"
    elif price >= 0.0001:
        return f"${price:.6f}"
    else:
        return f"${price:.8f}"


def format_change(change: float) -> str:
    if change > 0:
        return f"🟢 +{change:.2f}%"
    elif change < 0:
        return f"🔴 {change:.2f}%"
    return f"⚪ {change:.2f}%"


def format_volume(val: float) -> str:
    if val >= 1e9:
        return f"${val/1e9:.2f}B"
    elif val >= 1e6:
        return f"${val/1e6:.2f}M"
    elif val >= 1e3:
        return f"${val/1e3:.2f}K"
    return f"${val:.2f}"


async def get_coin_price(coin_key: str) -> dict | None:
    """دریافت قیمت یک کوین"""
    coin_id = COIN_IDS.get(coin_key.lower(), coin_key.lower())
    url = f"{settings.COINGECKO_API}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d",
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            data = r.json()
        if data:
            c = data[0]
            return {
                "id": c.get("id"),
                "name": c.get("name"),
                "symbol": c.get("symbol", "").upper(),
                "price": c.get("current_price", 0),
                "change_1h": c.get("price_change_percentage_1h_in_currency", 0) or 0,
                "change_24h": c.get("price_change_percentage_24h", 0) or 0,
                "change_7d": c.get("price_change_percentage_7d_in_currency", 0) or 0,
                "high_24h": c.get("high_24h", 0),
                "low_24h": c.get("low_24h", 0),
                "market_cap": c.get("market_cap", 0),
                "volume": c.get("total_volume", 0),
                "rank": c.get("market_cap_rank", 0),
                "ath": c.get("ath", 0),
                "ath_change": c.get("ath_change_percentage", 0) or 0,
            }
    except Exception as e:
        print(f"CoinGecko error: {e}")
    return None


async def get_market_overview() -> dict | None:
    """نمای کلی بازار"""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{settings.COINGECKO_API}/global")
            data = r.json().get("data", {})
        return {
            "total_market_cap": data.get("total_market_cap", {}).get("usd", 0),
            "total_volume": data.get("total_volume", {}).get("usd", 0),
            "btc_dominance": data.get("market_cap_percentage", {}).get("btc", 0),
            "eth_dominance": data.get("market_cap_percentage", {}).get("eth", 0),
            "market_cap_change_24h": data.get("market_cap_change_percentage_24h_usd", 0),
            "active_coins": data.get("active_cryptocurrencies", 0),
        }
    except Exception as e:
        print(f"CoinGecko global error: {e}")
    return None


async def get_trending() -> list[dict]:
    """کوین‌های ترند"""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{settings.COINGECKO_API}/search/trending")
            data = r.json()
        coins = []
        for item in data.get("coins", [])[:7]:
            c = item.get("item", {})
            coins.append({
                "name": c.get("name"),
                "symbol": c.get("symbol"),
                "rank": c.get("market_cap_rank", "?"),
            })
        return coins
    except Exception as e:
        print(f"CoinGecko trending error: {e}")
    return []


async def get_top_gainers_losers() -> dict:
    """برترین‌ها و بیشترین افت"""
    url = f"{settings.COINGECKO_API}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False,
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            data = r.json()

        sorted_data = sorted(data, key=lambda x: x.get("price_change_percentage_24h") or 0)
        losers = [{
            "name": c["name"], "symbol": c["symbol"].upper(),
            "change": c.get("price_change_percentage_24h", 0) or 0
        } for c in sorted_data[:5]]
        gainers = [{
            "name": c["name"], "symbol": c["symbol"].upper(),
            "change": c.get("price_change_percentage_24h", 0) or 0
        } for c in sorted_data[-5:][::-1]]
        return {"gainers": gainers, "losers": losers}
    except Exception as e:
        print(f"Gainers/Losers error: {e}")
    return {"gainers": [], "losers": []}


async def get_fear_greed() -> dict | None:
    """شاخص ترس و طمع"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.alternative.me/fng/")
            data = r.json()
        item = data.get("data", [{}])[0]
        return {
            "value": int(item.get("value", 0)),
            "label": item.get("value_classification", ""),
        }
    except Exception as e:
        print(f"Fear&Greed error: {e}")
    return None


def format_coin_message(coin: dict) -> str:
    """فرمت پیام قیمت کوین"""
    emoji = "₿" if coin["symbol"] == "BTC" else ("Ξ" if coin["symbol"] == "ETH" else "🪙")
    return f"""
{emoji} <b>{coin['name']} ({coin['symbol']})</b>
━━━━━━━━━━━━━━━━━━
💵 قیمت: <b>{format_price(coin['price'])}</b>
📈 ۱ ساعته: {format_change(coin['change_1h'])}
📊 ۲۴ ساعته: {format_change(coin['change_24h'])}
📅 ۷ روزه: {format_change(coin['change_7d'])}
━━━━━━━━━━━━━━━━━━
🔺 بالاترین ۲۴h: {format_price(coin['high_24h'])}
🔻 پایین‌ترین ۲۴h: {format_price(coin['low_24h'])}
💹 حجم بازار: {format_volume(coin['market_cap'])}
🔄 حجم معاملات: {format_volume(coin['volume'])}
🏆 رتبه: #{coin['rank']}
🚀 ATH: {format_price(coin['ath'])} ({coin['ath_change']:.1f}%)
━━━━━━━━━━━━━━━━━━
<i>📡 داده از CoinGecko — لحظه‌ای</i>
""".strip()
