import random
import time

from pet.mood import BORED, HUNGRY, PLAYFUL, SAD, normalize_mood


class Pet:
    BORED_TIMEOUT_SECONDS = 10 * 60
    HUNGRY_TIMEOUT_SECONDS = 15 * 60
    SAD_IF_NEGLECTED_FOR_SECONDS = 20 * 60
    RANDOM_SAD_MIN_INTERVAL_SECONDS = 60
    RANDOM_SAD_MAX_INTERVAL_SECONDS = 8 * 60

    def __init__(self) -> None:
        self.xp = 0
        self.hunger = 50

        now = self._now()
        self.last_play_at = now
        self.last_feed_at = now

        self.is_bored = False
        self.is_hungry = False
        self.both_since: float | None = None

        # Default mode starts as sad.
        self.sad_active = True
        self.sad_needs_play = self.sad_active
        self.sad_needs_feed = self.sad_active
        self.mood = SAD
        self.next_random_sad_at = now + self._next_random_sad_delay()

    @staticmethod
    def _now() -> float:
        return time.time()

    @classmethod
    def from_state(cls, state: dict | None) -> "Pet":
        pet = cls()
        if not state:
            pet.tick()
            return pet

        now = cls._now()
        pet.xp = int(state.get("xp", 0))
        pet.hunger = int(state.get("hunger", 50))
        pet.last_play_at = float(state.get("last_play_at", now))
        pet.last_feed_at = float(state.get("last_feed_at", now))
        pet.is_bored = bool(state.get("is_bored", False))
        pet.is_hungry = bool(state.get("is_hungry", False))

        both_since = state.get("both_since")
        pet.both_since = float(both_since) if both_since is not None else None

        pet.sad_active = bool(state.get("sad_active", False))
        pet.sad_needs_play = bool(state.get("sad_needs_play", False))
        pet.sad_needs_feed = bool(state.get("sad_needs_feed", False))
        pet.next_random_sad_at = float(state.get("next_random_sad_at", now + pet._next_random_sad_delay()))
        pet.mood = normalize_mood(str(state.get("mood", SAD)))

        pet.tick()
        return pet

    def to_state(self) -> dict:
        return {
            "mood": self.mood,
            "xp": self.xp,
            "hunger": self.hunger,
            "last_play_at": self.last_play_at,
            "last_feed_at": self.last_feed_at,
            "is_bored": self.is_bored,
            "is_hungry": self.is_hungry,
            "both_since": self.both_since,
            "sad_active": self.sad_active,
            "sad_needs_play": self.sad_needs_play,
            "sad_needs_feed": self.sad_needs_feed,
            "next_random_sad_at": self.next_random_sad_at,
        }

    def _next_random_sad_delay(self) -> float:
        return random.uniform(self.RANDOM_SAD_MIN_INTERVAL_SECONDS, self.RANDOM_SAD_MAX_INTERVAL_SECONDS)

    def _start_sad(self) -> None:
        self.sad_active = True
        self.sad_needs_play = True
        self.sad_needs_feed = True
        self.next_random_sad_at = self._now() + self._next_random_sad_delay()

    def _try_resolve_sad(self) -> None:
        if self.sad_active and not self.sad_needs_play and not self.sad_needs_feed:
            self.sad_active = False
            self.both_since = None

    def tick(self) -> None:
        now = self._now()

        self.is_bored = (now - self.last_play_at) >= self.BORED_TIMEOUT_SECONDS
        self.is_hungry = (now - self.last_feed_at) >= self.HUNGRY_TIMEOUT_SECONDS

        if self.is_bored and self.is_hungry:
            if self.both_since is None:
                self.both_since = now
            if (now - self.both_since) >= self.SAD_IF_NEGLECTED_FOR_SECONDS:
                self._start_sad()
        else:
            self.both_since = None

        if (not self.sad_active) and now >= self.next_random_sad_at:
            self._start_sad()

        if self.sad_active:
            self.mood = SAD
        elif self.is_hungry:
            self.mood = HUNGRY
        elif self.is_bored:
            self.mood = BORED
        else:
            self.mood = PLAYFUL

    def feed(self) -> None:
        self.tick()
        self.hunger = max(0, self.hunger - 10)
        self.xp += 5
        self.last_feed_at = self._now()
        self.is_hungry = False
        if self.sad_active:
            self.sad_needs_feed = False
        self._try_resolve_sad()
        self.tick()

    def play(self) -> None:
        self.tick()
        self.xp += 10
        self.last_play_at = self._now()
        if self.sad_active:
            self.sad_needs_play = False
        self._try_resolve_sad()
        self.tick()

    def seconds_until_bored(self) -> int:
        self.tick()
        remaining = self.BORED_TIMEOUT_SECONDS - (self._now() - self.last_play_at)
        return max(0, int(remaining))

    def seconds_until_hungry(self) -> int:
        self.tick()
        remaining = self.HUNGRY_TIMEOUT_SECONDS - (self._now() - self.last_feed_at)
        return max(0, int(remaining))

    def seconds_until_neglect_sad(self) -> int:
        self.tick()
        if self.sad_active:
            return 0
        if not (self.is_bored and self.is_hungry):
            return self.SAD_IF_NEGLECTED_FOR_SECONDS
        if self.both_since is None:
            return self.SAD_IF_NEGLECTED_FOR_SECONDS
        remaining = self.SAD_IF_NEGLECTED_FOR_SECONDS - (self._now() - self.both_since)
        return max(0, int(remaining))
