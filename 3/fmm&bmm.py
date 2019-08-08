import traceback

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

def get_segment_left(text, word_list):
    if text in word_list:
        return text
    elif len(text) == 0:
        return ""
    elif len(text) == 1:
        return text
    else:
        length = len(text) - 1
        text = text[-length:]
        return get_segment_left(text, word_list)

def fmm(str):
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
        test_str = test_str[seg_length:]
    print(result_str[:-1])

def bmm(str):
    word_set = get_word_dict()
    test_str = str.strip()
    result_str = ''
    max_length = 5
    result_length = 0
    while test_str:
        temp = test_str[-max_length:]
        seg_str = get_segment_left(temp, word_set)
        seg_length = len(seg_str)

        result_length = result_length + seg_length
        if seg_str.strip():
            result_str = '/' + seg_str + result_str
        test_str = test_str[:-seg_length]
    print(result_str[1:])

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

if __name__ == '__main__':
    test_str1 = '祝愿祖国明天更加繁荣昌盛 香港大学生在京度佳节'
    test_str2 = '新华社北京１月１日电'
    test_str3 = '昨晚，第一次来到首都北京的５０多名香港大学生，和北京航空航天大学的同学们在《歌唱祖国 》的歌声中一起迎接１９９８年的到来。'
    test_str4 = '此次到京的香港大学生来自香港科技大学和浸会大学，他们于１２月３０日抵京后  参观了北大、清华和抗日战争纪念馆。在中国青年政治学院，两地大学生就学习、生活等共同关心的话题展开了交流'

    for str in [test_str1, test_str2, test_str3, test_str4]:
        fmm(str)
        bmm(str)
        print()

    fmm('江泽民')