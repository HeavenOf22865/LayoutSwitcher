from time import sleep

import pyautogui
import pyperclip
from pynput import keyboard

DICTIONARY_RU = "йцукенгшщзхъфывапролджэячсмитьбю"
DICTIONARY_ENG = "qwertyuiop[]asdfghjkl;'zxcvbnm,."

ru_to_eng = dict(zip(DICTIONARY_RU, DICTIONARY_ENG))
eng_to_ru = dict(zip(DICTIONARY_ENG, DICTIONARY_RU))


def convert():
    pyperclip.copy("")

    sleep(0.1)

    pyautogui.hotkey("ctrl", "c")

    text = pyperclip.paste()

    result = ""

    for char in text:
        low_char = char.lower()

        if low_char in ru_to_eng:
            new_char = ru_to_eng[low_char]
        elif low_char in eng_to_ru:
            new_char = eng_to_ru[low_char]
        else:
            new_char = char

        result += new_char.upper() if char.isupper() else new_char

    pyperclip.copy(result)

    pyautogui.hotkey("ctrl", "v")


def main():
    with keyboard.GlobalHotKeys({"<alt>+c": convert}) as h:
        h.join()


if __name__ == "__main__":
    main()
