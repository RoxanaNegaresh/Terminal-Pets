import json
import os
import tempfile
import uuid
from typing import Any

STATE_FILE = os.path.join(tempfile.gettempdir(), "terminal_pet_state.json")


def load_pet_state() -> dict[str, Any] | None:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            return data
    except FileNotFoundError:
        return None
    except Exception:
        return None
    return None


def save_pet_state(state: dict[str, Any]) -> None:
    directory = os.path.dirname(STATE_FILE) or "."
    os.makedirs(directory, exist_ok=True)
    temp_path = f"{STATE_FILE}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=True)
    os.replace(temp_path, STATE_FILE)


def reset_pet_state() -> bool:
    try:
        os.remove(STATE_FILE)
        return True
    except FileNotFoundError:
        return False
