ASCII_FRAMES = {
    "happy": {
        "open": r"""
 /\_/\
( ^.^ )  Mood: Happy
 > ^ <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Happy
 > ^ <
""",
    },
    "playful": {
        "open": r"""
 /\_/\
( o.o )  Mood: Playful
 > ^ <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Playful
 > ^ <
""",
    },
    "grumpy": {
        "open": r"""
 /\_/\
( -.- )  Mood: Grumpy
 > ^ <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Grumpy
 > ^ <
""",
    },
}


def get_frame(mood: str, blink: bool = False) -> str:
    mood_frames = ASCII_FRAMES.get(mood, ASCII_FRAMES["playful"])
    return mood_frames["closed"] if blink else mood_frames["open"]
