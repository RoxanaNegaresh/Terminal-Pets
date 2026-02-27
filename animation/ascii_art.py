from pet.mood import BORED, HUNGRY, PLAYFUL, SAD, normalize_mood

ASCII_BASE = {
    PLAYFUL: {
        "open": [
            r"/\_/\ ",
            r"( o.o )",
            r" > ^ < ",
        ],
        "closed": [
            r"/\_/\ ",
            r"( -.- )",
            r" > ^ < ",
        ],
    },
    SAD: {
        "open": [
            r"/\_/\ ",
            r"( ;.; )",
            r" > ^ < ",
        ],
        "closed": [
            r"/\_/\ ",
            r"( -.- )",
            r" > ^ < ",
        ],
    },
    HUNGRY: {
        "open": [
            r"/\_/\ ",
            r"( o.o )",
            r" > ~ < ",
        ],
        "closed": [
            r"/\_/\ ",
            r"( -.- )",
            r" > ~ < ",
        ],
    },
    BORED: {
        "open": [
            r"/\_/\ ",
            r"( -.- )",
            r" > - < ",
        ],
        "closed": [
            r"/\_/\ ",
            r"( -.- )",
            r" > - < ",
        ],
    },
}


def _compose_frame(base_lines: list[str], mood: str) -> str:
    mood_text = f"Mood: {mood.capitalize()}"
    content_width = max(max(len(line) for line in base_lines), len(mood_text))
    centered_pet = [line.center(content_width) for line in base_lines]
    centered_mood = mood_text.center(content_width)
    return "\n" + "\n".join(centered_pet + [centered_mood]) + "\n"


def get_frame(mood: str, blink: bool = False) -> str:
    safe_mood = normalize_mood(mood)
    mode = "closed" if blink else "open"
    return _compose_frame(ASCII_BASE[safe_mood][mode], safe_mood)
