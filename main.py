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
    gray = cv2.cvtColor(np.array(img_resized), cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    cv2.imshow("debug", thresh)
    cv2.waitKey()

    config = r'--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    raw_text = pytesseract.image_to_string(thresh, config=config)

    words = re.findall(r'\b[a-zA-Z]{2,}\b', raw_text)
    return words


def input_word(word: str) -> None:
    pydirectinput.typewrite(word, 0.05)
    time.sleep(0.1 + random.random() * 0.2)
    pydirectinput.press("enter")


def bot_loop() -> None:
    Path("logs/").mkdir(parents=True, exist_ok=True)

    guesser = WordGuesser()

    word_region = get_word_region()
    if word_region == None:
        return

    time.sleep(1)
    while True:
        screenshot = pyautogui.screenshot("logs/region_screenshot.png", region=word_region)
        words = get_words_in_region(screenshot)
        print(f"Words found: {words}")
        guess, confidence = guesser.guess_next_word(words)
        if guess:
            print(f"Guessed word: {guess} (confidence: {confidence:.2f})")
            input_word(guess)


def main():
    bot_loop()


if __name__ == "__main__":
    main()
