import re

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
    '''
    with open("./wordcount.txt", "w", encoding="utf-8") as f:
        for word in sorted_dict:
            f.write(word[0] + ":" + str(word[1]) + "\n")
    f.close()
    '''
    return sorted_dict

if __name__ == '__main__':
    generate_word_count()