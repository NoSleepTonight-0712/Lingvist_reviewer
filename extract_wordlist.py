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

data_file = './wl_data/data.txt'

def read_data_file(data_fp):
    with open(data_fp, encoding='utf-8') as f:
        data_string = f.read()

        
        def split_word_meta_data(word):
            return word.split(field_splitter)
        
        return [split_word_meta_data(i) for i in data_string.split(word_splitter)]
       
data = read_data_file(data_file)

df = pd.DataFrame(data, columns=['word', 'sentence', 'last_practice', 'practiced_time'])


def is_selected_for_listening_list(lp):
    # lp = last_practice
    # Rule: if there is "minute", 'hour', 'yesterday', 'one day', '1 day', '2 days', add them to review list.
    test_strings = ["minute", 'hour', 'yesterday', 'one day', '1 day', '2 days']
    for i in test_strings:
        if i in lp:
            return True
    
    return False

def get_practiced_time(pt):
    # pt = practiced_time
    pt = pt.replace('Practiced: ', '').replace(' times', '')
    if pt.endswith('time'):
        pt_int = 1
    else:
        pt_int = int(pt) 
        
    def get_weight(n):
        if n <= 3:
            return 1
        elif n <= 10:
            return 1
        else:
            return 1
        
    return get_weight(pt_int)

def correct_curl_in_word(w):
    return w.replace("' ", "'")

df['is_selected'] = df['last_practice'].apply(is_selected_for_listening_list)
df['weight'] = df['practiced_time'].apply(get_practiced_time)
df['word'] = df['word'].apply(correct_curl_in_word)

df_selected = df[df['is_selected']]

df.to_csv('wordlist.csv')
