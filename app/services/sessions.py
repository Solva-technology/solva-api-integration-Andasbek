import json
import os
import time
import asyncio
from typing import Dict, List

SESSIONS_FILE = os.path.join(os.getcwd(), "sessions.json")
WINDOW_SEC = 120
LIMIT = 3

def _ensure_file():
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def _read_sessions() -> Dict[str, List[float]]:
    _ensure_file()
    try:
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _write_sessions(data: Dict[str, List[float]]) -> None:
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def record(user_id: int) -> None:
    now = time.time()
    data = _read_sessions()
    arr = data.get(str(user_id), [])
    arr.append(now)

    arr = [t for t in arr if now - t <= WINDOW_SEC]
    data[str(user_id)] = arr

    _write_sessions(data)

def is_blocked(user_id: int) -> bool:
    now = time.time()
    data = _read_sessions()
    arr = [t for t in data.get(str(user_id), []) if now - t <= WINDOW_SEC]
    return len(arr) >= LIMIT

async def periodic_cleanup_sessions(interval_sec: int = 120) -> None:
    while True:
        await asyncio.sleep(interval_sec)
        _write_sessions({})