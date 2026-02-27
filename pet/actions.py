from persistence.storage import save_pet_state
from pet.pet import Pet


def _format_duration(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def apply_action(pet: Pet, command: str) -> bool:
    pet.tick()

    if command == "feed":
        pet.feed()
    elif command == "play":
        pet.play()
    elif command == "status":
        until_bored = _format_duration(pet.seconds_until_bored())
        until_hungry = _format_duration(pet.seconds_until_hungry())
        until_neglect_sad = _format_duration(pet.seconds_until_neglect_sad())
        hunger_state = "Hungry" if pet.is_hungry else "Not Hungry"
        bored_state = "Bored" if pet.is_bored else "Not Bored"
        if pet.sad_active:
            sad_requirements = []
            if pet.sad_needs_play:
                sad_requirements.append("play")
            if pet.sad_needs_feed:
                sad_requirements.append("feed")
            sad_need_text = "+".join(sad_requirements) if sad_requirements else "none"
        else:
            sad_need_text = "none"
        print(
            f"Mood: {pet.mood} | XP: {pet.xp} | Hunger: {pet.hunger} | "
            f"{hunger_state} | {bored_state} | Bored in: {until_bored} | "
            f"Hungry in: {until_hungry} | Sad(in neglect): {until_neglect_sad} | Sad needs: {sad_need_text}"
        )
    elif command == "exit":
        return False
    elif command:
        print("Unknown command")

    save_pet_state(pet.to_state())
    return True
