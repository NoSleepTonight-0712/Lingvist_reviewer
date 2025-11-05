def get_easy_word_list():
    with open('./wl_data/easy_words.txt') as f:
        ls = f.read().split('\n')
        
    return [i.strip() for i in ls if (i.strip() != '')]
    
    