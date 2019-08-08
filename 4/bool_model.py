import re
import sys
import traceback
import io
import json
import cmath
import math
# from bitarray import bitarray

def get_stopwords():
    stopwords_list = []
    with open("./stopwords.txt", encoding='utf-8') as f:
        line = f.readline()
        while line:
            word = line.strip()
            stopwords_list.append(word)
            line = f.readline()
    return stopwords_list

def get_whole_dict():
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
                if re.match(r'([\S]*?)-([\S]*?)-([\S]*?)-([\S]*?)', word):
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

def get_all_possible_bool(size):
    bool_arr = []
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    if size == 2:
        return [[False], [True]]
    for i in range(size):
        bool_value = []
        bi_num = get_bin(i, (math.ceil(math.sqrt(size))))
        print(bi_num)
        for i in range(len(bi_num)):
            if bi_num[i] == '1':
                bool_value.append(True)
            else:
                bool_value.append(False)
        print(bool_value)
        bool_arr.append(bool_value)
    return bool_arr
        #bi_num = bitarray(bin(i)[2:].zfill((math.ceil(math.sqrt(size)))))
        # bool_arr.append(bi_num.tolist())
    #return bool_arr

def get_all_matched(string_to_match):
    matched_num = 0
    unmatched_num = 0

    char_arr_to_match, bool_values = parse_bool_str(string_to_match)
    print('可能的布尔取值：')
    print(bool_values)

    whole_dict = get_whole_dict()
    all_matched = list()
    for paragraph_dict in whole_dict.values():
        word_set = set()
        for char in paragraph_dict.keys():
            word_set.add(char)
        ok = False
        for bool_list in bool_values:
            _ok = True
            for i in range(len(bool_list)):
                if bool_list[i] == True and char_arr_to_match[i] not in word_set or bool_list[i] == False and char_arr_to_match[i] in word_set:
                    _ok = False
                    break
            if _ok:
                ok = True
                break
        if ok:
            matched_num = matched_num + 1
            all_matched.append(word_set)
        else:
            unmatched_num = unmatched_num + 1

    print_num = min(matched_num, 10)
    for i in range(print_num):
        print(all_matched[i])
    print('击中数：', str(matched_num), '未击中数：', str(unmatched_num))
    return True



def parse_bool_str(_string):
    parsed_set = _string.replace(')', '').replace('(', '').split(' ')
    bool_word = ['and', 'not', 'or']
    for word in bool_word:
        if word in parsed_set:
            parsed_set.remove(word)
    for word in parsed_set:
        if word == 'and' or word == 'or' or word == 'not' or word == '':
            parsed_set.remove(word)
    parsed_set.sort(key=len, reverse=True)
    all_bool = get_all_possible_bool(2 ** len(parsed_set))
    right_bool = []
    for i in range(len(all_bool)):
        string_to_parse = str(_string)
        for j in range(len(parsed_set)):
            string_to_parse = string_to_parse.replace(parsed_set[j], str(all_bool[i][j]))
        result = eval(string_to_parse)
        if result == True:
            right_bool.append(all_bool[i])
    return parsed_set, right_bool

def interface():
    line = input('请输入一个布尔语句：')
    proper = get_all_matched(line)
    while not proper:
        line = input('请输入一个布尔语句：')
        proper = get_all_matched(line)

if __name__ == '__main__':
    interface()