import random
import pandas as pd

NUM_CHOICES = 10
NUM_CHALLENGES = 5

words = pd.read_csv("word-order.csv")
assert list(words.columns) == ["word", "metaphone", "translation"]

def play_sound(word):
    print(f"Mock playing audio/{word}.mp3")

def pick_challenge():
    start_index = random.randint(0, len(words) - NUM_CHOICES)
    stop_index = start_index + NUM_CHOICES
    true_index = random.randint(start_index, stop_index)

    word, _, translation = words.iloc[true_index]
    word_choices = list(words.iloc[start_index:stop_index]["word"])
    translation_choices = [translation]
    while len(translation_choices) < NUM_CHOICES:
        _, _, tmp = words.iloc[random.randint(0, len(words))]
        if tmp not in translation_choices:
            translation_choices.append(tmp)

    random.shuffle(word_choices)
    random.shuffle(translation_choices)

    return word, translation, word_choices, translation_choices

challenges = [pick_challenge() for _ in range(NUM_CHALLENGES)]

attempt = 1
while len(challenges) > 0:
    for index in range(len(challenges) - 1, -1, -1):
        word, translation, word_choices, translation_choices = challenges[index]

        print("\nWhich word do you hear?")
        play_sound(word)
        for i, word_choice in enumerate(word_choices):
            print(f"{i}. {word_choice}")
        choice = int(input(f"[0-{NUM_CHOICES}] "))
        if word_choices[choice] != word:
            if attempt < 3:
                print("Wrong.")
            else:
                print(f"Wrong. The correct word is \"{word}\".")
            continue

        print("Correct! What does it mean in English?")
        for i, translation_choice in enumerate(translation_choices):
            print(f"{i}. {translation_choice}")
        choice = int(input(f"[0-{NUM_CHOICES}] "))
        if translation_choices[choice] != translation:
            if attempt < 3:
                print("Wrong.")
            else:
                print(f"Wrong. The correct translation is \"{translation}\".")
            continue

        # both correct: remove it
        print("Correct!")
        del challenges[index]

    attempt += 1
