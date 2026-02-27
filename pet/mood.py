PLAYFUL = "playful"
SAD = "sad"
HUNGRY = "hungry"
BORED = "bored"

DEFAULT_MOOD = SAD
ALL_MOODS = {PLAYFUL, SAD, HUNGRY, BORED}


def normalize_mood(value: str) -> str:
    value = (value or "").strip().lower()
    return value if value in ALL_MOODS else DEFAULT_MOOD
