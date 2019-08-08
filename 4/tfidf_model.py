import re
import sys
import traceback
import io
import json
import math
import time
from tqdm import tqdm
from pymongo import MongoClient

def get_tf_database():
    client = MongoClient()
    return client.dcs.tf

def get_idf_database():
    client = MongoClient()
    return client.dcs.idf

def get_tfidf_database():
    client = MongoClient()
    return client.dcs.tfidf

def get_word_dict():
    words_set = list()
    with open("./wordcount.txt", encoding="utf-8") as f:
        line = f.readline()
        while line:
            word = line.split(":")
            try:
                words_set.append(word[0])
            except:
                print(traceback)
            line = f.readline()
    f.close()
    return words_set

def get_stopwords():
    stopwords_list = []
    with open("./stopwords.txt", encoding='utf-8') as f:
        line = f.readline()
        while line:
            word = line.strip()
            stopwords_list.append(word)
            line = f.readline()
    return stopwords_list

def generate_word_count():
    whole_dict = dict()
    with open("./语料库.txt", encoding='utf-8') as f:
        line = f.readline()
        while line:
            line = f.readline()
            match = re.findall(r'([\S]*?)/([\S]*?)', line)
            for item in match:
                word = item[0]
                if not word in whole_dict.keys():
                    whole_dict[word] = 1
                else:
                    whole_dict[word] = whole_dict[word] + 1
    f.close()
    sorted_dict = sorted(whole_dict.items(), key=lambda d: d[1], reverse=True)

    return sorted_dict

def get_segment_right(text, word_list):
    if text in word_list:
        return text
    elif len(text) == 0:
        return ""
    elif len(text) == 1:
        return text
    else:
        length = len(text) - 1
        text = text[:length]
        return get_segment_right(text, word_list)

def fmm(str):
    fmm_list = list()
    word_set = get_word_dict()
    test_str = str.strip()
    result_str = ''
    max_length = 5
    result_length = 0
    while test_str:
        temp = test_str[:max_length]
        seg_str = get_segment_right(temp, word_set)
        seg_length = len(seg_str)

        result_length = result_length + seg_length
        if seg_str.strip():
            result_str = result_str + seg_str + '/'
            fmm_list.append(seg_str)
        test_str = test_str[seg_length:]
    return fmm_list

def get_whole_dict():
    stop_words = get_stopwords()
    whole_dict = dict()
    with open("./语料库.txt", encoding='utf-8') as f:
        paragraph_dict = dict()
        paragraph_num = 0
        line = f.readline()
        info_str = ''
        while line:
            line = f.readline()
            info = re.findall(r'([\S]*?)-([\S]*?)-([\S]*?)-([\S]*?)', line)
            if len(info) == 0:
                if len(paragraph_dict) != 0:
                    whole_dict[info_str] = paragraph_dict
                paragraph_dict = dict()
                continue

            info_str = info[0][0] + '-' + info[0][1] + '-' + info[0][2]
            match = re.findall(r'([\S]*?)/([\S]*?)', line)
            for item in match:
                word = item[0]
                if word in stop_words or re.match(r'([\S]*?)-([\S]*?)-([\S]*?)-([\S]*?)', word):
                    continue
                if not word in paragraph_dict.keys():
                    paragraph_dict[word] = 1
                else:
                    paragraph_dict[word] = paragraph_dict[word] + 1

        #whole_dict[]
    f.close()

    return whole_dict

def get_word_set():
    whole_dict = get_whole_dict()

    print('File closed.')
    words_set = set()
    for child_dict in whole_dict.values():
        for word in child_dict.keys():
            words_set.add(word)
    print('Words set constructed.')
    return words_set


def get_idf_dict():
    print('Calculating idf...')
    whole_dict = get_whole_dict()
    words_set = get_word_set()

    idf_collection = get_idf_database()

    word_num = len(words_set)
    processed = idf_collection.count()
    idf_dict = dict()
    # print(len(words_set))
    with tqdm(total = word_num - processed) as pbar:
        for word in words_set:
            count_document = len(whole_dict)
            exists_doc_count = 0
            for words in whole_dict.values():
                words_in_doc = [item for item in words.keys()]
                # print(words_in_doc)
                if word in words_in_doc:
                    exists_doc_count = exists_doc_count + 1
            idf_value = math.log(count_document / exists_doc_count)
            idf_dict[word] = idf_value

            if idf_collection.count({'word': word}) == 0:
                idf_collection.insert_one({
                    'word': word,
                    'idf': idf_value
                })

            pbar.update(1)

    return idf_dict

def get_tf_dict():
    print('Calculating tf...')
    whole_dict = get_whole_dict()
    tf_collection = get_tf_database()

    tf_dict = dict()
    total_num = len(whole_dict)
    processed = tf_collection.count()
    with tqdm(total = total_num - processed) as pbar:

        for str_info, paragraph_dict in whole_dict.items():
            child_tf_dict = dict()
            whole_count = sum(paragraph_dict.values())
            for word, count in paragraph_dict.items():
                word_tf = count / whole_count
                child_tf_dict[word] = word_tf
            tf_dict[str_info] = child_tf_dict

            tf_collection.insert_one({
                'info_str': str_info,
                'word_dict': paragraph_dict,
                'tf_dict': child_tf_dict,
                'word_set': [word for word in paragraph_dict.keys()]
                })
            pbar.update(1)

    return tf_dict

def get_word_set_from_str_info(str_info):
    tf_collection = get_tf_database()
    try:
        item = tf_collection.find_one({'info_str': str_info})
        return item['word_set']
    except:
        print('Word set not found.')
        return []

def get_line_value_sort(words):
    tf_idf_collection = get_tfidf_database()
    sum_values_dict = dict()
    for item in tf_idf_collection.find():
        tf_idf_sum_value = 0
        info_str = item['info_str']
        tf_idf_dict = item['tf_idf_dict']
        for word in words:
            if word in tf_idf_dict.keys():
                tf_idf_sum_value = tf_idf_sum_value + tf_idf_dict[word]
            else:
                continue
        sum_values_dict[info_str] = tf_idf_sum_value
    sorted_sum_dict = sorted(sum_values_dict.items(), key=lambda d: d[1], reverse=True)
    for i in range(10):
        print(sorted_sum_dict[i])

def analyze_input(line):
    stop_words = get_stopwords()
    fmm_result = fmm(line)
    for word in fmm_result:
        if word in stop_words:
            fmm_result.remove(word)
    print(fmm_result)
    tf_idf_dict = get_tf_idf_values_dict()

    calculated_sum_dict = list()

    for info_str, values_dict in tf_idf_dict.items():
        sum = 0
        for word in fmm_result:
            try:
                sum = sum + values_dict[word]
            except:
                continue
        calculated_sum_dict.append((info_str, sum))
    sorted_dict = sorted(calculated_sum_dict, key=lambda d: d[1], reverse=True)

    for i in range(10):
        print(sorted_dict[i][0], get_word_set_from_str_info(sorted_dict[i][0]))


def get_idf_values_dict():
    idf_dict = dict()
    idf_collection = get_idf_database()
    for item in idf_collection.find():
        idf_dict[item['word']] = item['idf']
    return idf_dict

def get_tf_idf_values_dict():
    tf_idf_dict = dict()
    tf_idf_collection = get_tfidf_database()
    for item in tf_idf_collection.find():
        tf_idf_dict[item['info_str']] = item['tf_idf_dict']
    return tf_idf_dict

def get_idf_value(word):
    idf_collection = get_idf_database()
    try:
        item = idf_collection.find_one({'word': word})
        return item['idf']
    except:
        #print('Cannot find idf value of', word)
        return 0


def generate_tfidf_dict():
    print('Calculating tfidf_values..')
    tf_collection = get_tf_database()
    tf_idf_collection = get_tfidf_database()

    idf_dict = get_idf_values_dict()

    tf_idf_dict = dict()
    total_num = tf_collection.count()
    processed = tf_idf_collection.count()
    with tqdm(total=total_num - processed) as pbar:
        for item in tf_collection.find():
            info_str = item['info_str']
            tf_dict = item['tf_dict']
            tf_idf_dict = dict()

            for word, tf in tf_dict.items():
                try:
                    idf = idf_dict[word]
                    tf_idf = idf * tf
                    tf_idf_dict[word] = tf_idf
                except:
                    continue

            #print(tf_idf_dict)

            if tf_idf_collection.count({'info_str': info_str}) == 0:
                tf_idf_collection.insert_one({
                    'info_str': info_str,
                    'tf_idf_dict': tf_idf_dict,
                    'tf_dict': tf_dict
                })
            pbar.update(1)

    #print(whole_num)

    return tf_idf_dict

def read_and_analyze():
    line = input('请输入不超过八个字的短语：')
    if line != None:
        print(analyze_input(line))



if __name__ == '__main__':
    #get_tf_dict()
    #get_idf_dict()
	#generate_tfidf_dict()
	read_and_analyze()