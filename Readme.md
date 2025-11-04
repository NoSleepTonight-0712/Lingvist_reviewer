## French learning - making audio from lingvist word list



### Usage:
1. Use `extract_word.js` to extract word from `https://learn.lingvist.com/#insights/wordlist`.
2. Copy the console output to `wl_data/data.txt`
3. Run `extract_wordlist.py`. You will se a generated `wordlist.csv`.
4. (Optional) Change the `weight` column in the csv file. If you don't want to review some words, set the corresponding `weight` to 0. 
> For now, setting the `weight` to 1 or above is the same.
5. Run `generate_audio.py`. Make sure the internet connection is good to connect google TTS service.
6. Find your audio and lrc subtitle files in `French_audios/`! The subtitle is also embedded into the mp3 file, so if your player supports the embedded lyric, you can just use the `.mp3` file itself without `.lyc` file.