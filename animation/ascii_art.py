from pet.mood import BORED, HUNGRY, PLAYFUL, SAD, normalize_mood

ASCII_FRAMES = {
    PLAYFUL: {
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
    SAD: {
        "open": r"""
 /\_/\
( ;.; )  Mood: Sad
 > ^ <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Sad
 > ^ <
""",
    },
    HUNGRY: {
        "open": r"""
 /\_/\
( o.o )  Mood: Hungry
 > ~ <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Hungry
 > ~ <
""",
    },
    BORED: {
        "open": r"""
 /\_/\
( -.- )  Mood: Bored
 > - <
""",
        "closed": r"""
 /\_/\
( -.- )  Mood: Bored
 > - <
""",
    },
}


def get_frame(mood: str, blink: bool = False) -> str:
    mood_frames = ASCII_FRAMES[normalize_mood(mood)]
    return mood_frames["closed"] if blink else mood_frames["open"]
