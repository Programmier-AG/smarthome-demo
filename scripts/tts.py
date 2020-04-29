from gtts import gTTS
import os
import time


def run(attr):
    attr = attr.replace("+", " ")

    tts = gTTS(text=attr, lang='de')
    try:
        os.remove("sounds/tts.mp3")
    except FileNotFoundError:
        pass
    tts.save("sounds/tts.mp3")
    os.system("mplayer file > /dev/null 2>&1 sounds/tts.mp3")
