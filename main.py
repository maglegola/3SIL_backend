import os
API_KEY = os.getenv("API_KEY", "replace-this-with-your-secret")
from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

app = FastAPI(
    title="3SIL Intraday Trading Backend",
    version="1.0.0",
    description="Backend API for 3SIL GPT Actions"
)

API_KEY = "replace-this-with-your-secret"

def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

class NewsItem(BaseModel):
    headline: str
    source: str
    published_at: str
    topic_tags: List[str]
    severity: str
    short_summary: str

class MacroEvent(BaseModel):
    event_name: str
    country: str
    scheduled_time_cet: str
    importance: str
    category: str
    minutes_until_event: int

@app.get("/")
def root():
    return {"message": "3SIL backend is running"}

@app.get("/market/snapshot")
def get_market_snapshot(
    isin: str = Query(...),
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    # TODO: replace with real provider calls
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "venue_name": "Tradegate",
        "venue_symbol": "SIL3",
        "isin": isin,
        "session_open_time": "07:30:00 CET",
        "last_price": 12.34,
        "bid": 12.31,
        "ask": 12.37,
        "spread_pct": 0.49,
        "session_open_price": 13.20,
        "intraday_high": 13.25,
        "intraday_low": 12.10,
        "vwap": 12.55,
        "volume": 105432,
        "pct_from_open": -6.52,
        "pct_from_low": 1.98,
        "trend_1m": "flat",
        "trend_5m": "down",
        "trend_15m": "down",
        "realized_volatility_short": 2.1,
        "trading_status": "open"
    }

@app.get("/market/related-assets")
def get_related_assets(
    isin: str = Query(...),
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    # TODO: replace with real provider calls
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "silver_futures_last": 31.42,
        "silver_futures_trend_1m": "flat",
        "silver_futures_trend_5m": "down",
        "silver_futures_trend_15m": "down",
        "spot_silver_last": 31.38,
        "eurusd_last": 1.0821,
        "eurusd_trend_1m": "up",
        "oil_last": 82.75,
        "oil_trend_1m": "up",
        "oil_trend_5m": "up",
        "dxy_last": 104.21,
        "dxy_trend_1m": "up",
        "gold_last": 3088.4,
        "us10y_yield_last": 4.18
    }

@app.get("/news/recent")
def get_recent_news(
    topics: str = Query(...),
    lookback_minutes: int = Query(...),
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    items = [
        NewsItem(
            headline="Oil rises after renewed Middle East supply concerns",
            source="Example News Feed",
            published_at=datetime.now(timezone.utc).isoformat(),
            topic_tags=["oil", "middle east"],
            severity="high",
            short_summary="Oil moved sharply higher on geopolitical tension."
        )
    ]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "items": [item.model_dump() for item in items]
    }

@app.get("/calendar/today")
def get_macro_calendar(
    timezone: str = Query("Europe/Amsterdam"),
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    events = [
        MacroEvent(
            event_name="US CPI",
            country="US",
            scheduled_time_cet="14:30",
            importance="high",
            category="inflation",
            minutes_until_event=180
        )
    ]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "events": [event.model_dump() for event in events]
    }