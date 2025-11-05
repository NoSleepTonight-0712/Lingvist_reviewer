import pandas as pd
import math
import random
from gtts import gTTS
from pydub import AudioSegment
from mutagen.id3 import ID3, USLT
import datetime

# Parameters
WORD_PAUSE = 1000
SENTENCE_PAUSE = 2500
SPEECH_SPEED = 1.0

timestamp = datetime.datetime.now().strftime(r"%Y%m%d_%H%M")
OUTPUT_FILE = f"French_audios/French_{timestamp}"

field_splitter = r"=*#&^!="
word_splitter = r"$%d82@$="

df_selected = pd.read_excel('wordlist.xlsx')

# append new easy word list
with open('./wl_data/easy_words.txt', 'a+') as f:
    f.write('\n')
    f.write('\n'.join(df_selected[df_selected['weight'] == 0]['word']))
    f.write('\n')

df_selected = df_selected[df_selected['weight'] > 0]

def Silence(duration=1000):
    return AudioSegment.silent(duration)

def ms_to_timestamp(milliseconds):
    seconds, millis = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)  
    hours, minutes = divmod(minutes, 60)
    # return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, math.floor(millis))
    return '{:02d}:{:02d}.{:03d}'.format(minutes, seconds, math.floor(millis))

import hashlib
import os

CACHE_DIR = "tts_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

lyric_seperate = []

def text_hash(text):
    """Stable unique ID for caching."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def tts_to_audio(text, lang="fr"):
    """TTS with disk caching."""
    h = text_hash(text)
    cache_path = os.path.join(CACHE_DIR, f"{h}.mp3")

    # Try cache
    if os.path.exists(cache_path):
        audio = AudioSegment.from_mp3(cache_path)
    else:
        print(f"Generating audio: {text}")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(cache_path)
        audio = AudioSegment.from_mp3(cache_path)

    # Apply playback speed modification
    if SPEECH_SPEED != 1.0:
        audio = audio.speedup(playback_speed=SPEECH_SPEED)

    return audio


def build_item_audio(word, sentence, start_offset):
    """Create audio + collect lyric timestamps."""
    audio = AudioSegment.empty()
    lyrics = []

    def add_tts(entry_text):
        nonlocal audio, start_offset, lyrics
        ts = ms_to_timestamp(start_offset)      
        lyrics.append(f"[{ts}] {entry_text}")
        lyric_seperate.append(f"[{ts}] {entry_text}")
        segment = tts_to_audio(entry_text)
        audio += segment
        start_offset += len(segment)
        return start_offset

    # Word
    start_offset = add_tts(word)
    audio += Silence(duration=WORD_PAUSE)
    start_offset += WORD_PAUSE
    start_offset = add_tts(word)
    audio += Silence(duration=WORD_PAUSE)
    start_offset += WORD_PAUSE

    # Sentence
    start_offset = add_tts(sentence)
    audio += Silence(duration=SENTENCE_PAUSE)
    start_offset += SENTENCE_PAUSE
    start_offset = add_tts(sentence)
    audio += Silence(duration=SENTENCE_PAUSE)
    start_offset += SENTENCE_PAUSE

    return audio, lyrics, start_offset

def evenly_spread_list(lst, total_length):
    result = [None] * total_length
    step = total_length / len(lst)
    for i, item in enumerate(lst):
        index = int(i * step)
        while result[index] is not None:
            index = (index + 1) % total_length
        result[index] = item
    return result

def generate_audio(df, export_name):
    expanded_list = []
    for _, row in df.iterrows():
        expanded_list.extend([(row["word"], row["sentence"])] * int(row["weight"]))

    total_items = len(expanded_list)
    ordered_list = evenly_spread_list(expanded_list, total_items)

    final_audio = AudioSegment.empty()
    all_lyrics = []
    offset = 0

    for idx, (word, sentence) in enumerate(ordered_list, start=1):
        print(f"Adding {idx}/{total_items}: {word}")
        entry_audio, entry_lyrics, offset = build_item_audio(word, sentence, offset)
        final_audio += entry_audio
        all_lyrics.extend(entry_lyrics)

    final_audio.export(export_name, format="mp3")

    # Add lyrics metadata
    audio = ID3(export_name)
    lyrics_text = "\n".join(all_lyrics)
    audio.add(USLT(encoding=3, lang="fra", desc="lyrics", text=lyrics_text))
    audio.save()


generate_audio(df_selected, OUTPUT_FILE+'.mp3')

with open(OUTPUT_FILE+'_bck.lrc', 'w', encoding='UTF-8') as f:
    f.write('\n'.join(lyric_seperate))
