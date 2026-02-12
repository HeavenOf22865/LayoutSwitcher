import configparser
import os
import sys
import threading
from pathlib import Path
from time import sleep

import pyautogui
import pyperclip
import pystray
from PIL import Image
from pynput import keyboard

LOCAL_APPDATA_PATH = os.environ["LOCALAPPDATA"]
CONFIG_DIR = Path(LOCAL_APPDATA_PATH) / "LayoutSwitcher"
CONFIG_FILE = CONFIG_DIR / "config.ini"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def get_config():
    config = configparser.ConfigParser()

    if not CONFIG_FILE.exists():
        config["General"] = {
            "Dictionary 1": "qwertyuiop[]asdfghjkl;'zxcvbnm,.",
            "Dictionary 2": "йцукенгшщзхъфывапролджэячсмитьбю",
            "Hotkey": "<alt>+c",
        }

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    else:
        config.read(CONFIG_FILE, encoding="utf-8")

    return config


def convert(d1_to_d2, d2_to_d1):
    saved_text = pyperclip.paste()

    pyperclip.copy("")

    sleep(0.1)

    pyautogui.hotkey("ctrl", "c")

    text = pyperclip.paste()

    result = ""

    for char in text:
        low_char = char.lower()

        if low_char in d1_to_d2:
            new_char = d1_to_d2[low_char]
        elif low_char in d2_to_d1:
            new_char = d2_to_d1[low_char]
        else:
            new_char = char

        result += new_char.upper() if char.isupper() else new_char

    pyperclip.copy(result)

    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(saved_text)


def quit(icon, item):
    icon.stop()

    os._exit(0)


def open_config_folder():
    os.startfile(CONFIG_DIR)


def setup_tray():
    icon_path = get_resource_path("Assets/tray_icon.png")

    img = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("Open Config Folder", open_config_folder),
        pystray.MenuItem("Exit", quit),
    )
    icon = pystray.Icon("layout_switcher", img, "LayoutSwitcher", menu)
    icon.run()


def main():
    cfg = get_config()

    DICTIONARY_1 = str(cfg["General"].get("Dictionary 1"))
    DICTIONARY_2 = str(cfg["General"].get("Dictionary 2"))
    HOTKEY = str(cfg["General"].get("Hotkey"))

    d1_to_d2 = dict(zip(DICTIONARY_1, DICTIONARY_2))
    d2_to_d1 = dict(zip(DICTIONARY_2, DICTIONARY_1))

    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    with keyboard.GlobalHotKeys({HOTKEY: lambda: convert(d1_to_d2, d2_to_d1)}) as h:
        h.join()


if __name__ == "__main__":
    main()
