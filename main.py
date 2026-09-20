import cv2
import numpy as np
import pytesseract
import re
from pathlib import Path
import pyautogui
import pydirectinput
import random
import time
from src.area_selector import AreaSelector
from src.word_guesser import WordGuesser

VALID_WORDS: set[str] = set()
with open("valid_words.txt", "r") as f:
    valid = []
    for l in f:
        valid.append(l.strip().lower())
    VALID_WORDS = set(valid)


def is_real_word(word: str) -> bool:
    return (word.lower() in VALID_WORDS and len(word) > 3) # word shouldn't be less than 3 letters


def get_word_region() -> tuple | None:
    input("Press enter when you are ready to select the area to look for the words.")

    selector = AreaSelector()
    region = selector.get_selection()
    if not region:
        print("Could not get region from selection")
        return None

    return region


def get_words_in_region(screenshot) -> list[str]:
    img_resized = cv2.resize(screenshot, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
    _, s, v = cv2.split(hsv)
    
    # strip away panels with image wizardry idk man
    white_text_mask = (s < 60) & (v > 160)
    binary = np.where(white_text_mask, np.uint8(255), np.uint8(0))

    inverted = cv2.bitwise_not(binary)

    cv2.imwrite("logs/region_screenshot_processed.png", inverted)
    #cv2.imshow("debug", inverted)
    #cv2.waitKey()

    config = r'--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    raw_text = pytesseract.image_to_string(inverted, config=config).strip().lower()

    words = re.findall(r'\b[a-zA-Z]{2,}\b', raw_text)
    words = [word for word in words if is_real_word(word)]
    return words


def input_word(word: str) -> None:
    pydirectinput.typewrite(word, 0.05)
    time.sleep(0.1 + random.random() * 0.2)
    pydirectinput.press("enter")


def bot_loop() -> None:
    Path("logs/").mkdir(parents=True, exist_ok=True)

    guesser = WordGuesser(VALID_WORDS)

    word_region = get_word_region()
    if word_region == None:
        return

    already_guessed = []

    time.sleep(1)
    while True:
        screenshot = np.array(pyautogui.screenshot("logs/region_screenshot.png", region=word_region))
        words = get_words_in_region(screenshot)
        print(f"Words found: {words}")
        guess, confidence = guesser.guess_next_word(words, already_guessed)
        if guess:
            print(f"Guessed word: {guess} (confidence: {confidence:.2f})")
            input_word(guess)
            already_guessed.append(guess)
        time.sleep(1)


def main():
    bot_loop()


if __name__ == "__main__":
    main()
