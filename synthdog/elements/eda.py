# @Author : zhany
# @Time : 2019/03/20 

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from random import shuffle

# random.seed(2019)


#考虑到与英文的不同，暂时搁置
#文本清理
'''
import re
def get_only_chars(line):
    #1.清除所有的数字
'''


# ########################################################################
# # 同义词替换
# # 替换一个语句中的n个单词为其同义词
# ########################################################################
# def synonym_replacement(words, n):
#     new_words = words.copy()
#     random_word_list = list(set([word for word in words if word not in stop_words]))     
#     random.shuffle(random_word_list)
#     num_replaced = 0  
#     for random_word in random_word_list:          
#         synonyms = get_synonyms(random_word)
#         if len(synonyms) >= 1:
#             synonym = random.choice(synonyms)   
#             new_words = [synonym if word == random_word else word for word in new_words]   
#             num_replaced += 1
#         if num_replaced >= n: 
#             break

#     sentence = ' '.join(new_words)
#     new_words = sentence.split(' ')

#     return new_words

def get_synonyms(word):
    return synonyms.nearby(word)[0]


########################################################################
# 随机插入
# 随机在语句中插入n个词
########################################################################
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words

def random_gbk2312_chinese():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str

def add_word(new_words):
    synonyms = []
    counter = 0    
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        # synonyms = get_synonyms(random_word)
        synonyms = random_gbk2312_chinese()
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)


########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################

def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words

def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
    return new_words

########################################################################
# 随机删除
# 以概率p删除语句中的词
########################################################################
def random_deletion(words, p):

    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]

    return new_words

########################################################################
# 随机增加数字
# 随机增加数字
########################################################################
def random_insertion_number(words, n, max_length=11):
    new_words = words.copy()
    for _ in range(n):
        add_number(new_words, n=n, max_length=max_length)
    return new_words

def add_number(new_words, n, max_length):
    for i in range(n):
        random_synonym = ''
        for _ in range(random.randint(1, max_length)):
            random_synonym = random_synonym + str(random.randint(0, 9))
        random_idx = random.randint(0, len(new_words)-1)
        new_words.insert(random_idx, random_synonym)


########################################################################
#EDA函数
def eda(sentence, alpha_ri=0.2, alpha_rs=0.2, alpha_rd=0.2, alpha_rin=0.015, p_ri=0.33, p_rs=0.33, p_rd=0.33, p_rin=0.01, num_aug=1):
    # seg_list = jieba.cut(sentence)
    seg_list = list(sentence)
    seg_list = " ".join(seg_list)
    words = list(seg_list.split())
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug / 4) + 1
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    weight = [p_ri, p_rs, p_rd, p_rin]
    aug_list = ['ri', 'rs', 'rd', 'rin']
    aug_type = random.choices(aug_list, weight)[0]

    if aug_type == 'ri':
        #随机插入ri
        for _ in range(num_new_per_technique):
            a_words = random_insertion(words, n_ri)
            augmented_sentences.append(''.join(a_words))
    elif aug_type == 'rs':
        #随机交换rs
        for _ in range(num_new_per_technique):
            a_words = random_swap(words, n_rs)
            augmented_sentences.append(''.join(a_words))
    elif aug_type == 'rd':
        #随机删除rd
        for _ in range(num_new_per_technique):
            a_words = random_deletion(words, alpha_rd)
            augmented_sentences.append(''.join(a_words))
    elif aug_type == 'rin':
        #增加数字rin
        if (alpha_rin > 0):
            n_rin = max(1, int(alpha_rin*num_words))
            for _ in range(num_new_per_technique):
                a_words = random_insertion_number(words, n_rin)
                augmented_sentences.append(''.join(a_words))
    
    # return [augmented_sentences[-1]]
    #print(augmented_sentences)
    
    # shuffle(augmented_sentences)

    # if num_aug >= 1:
    #     augmented_sentences = augmented_sentences[:num_aug]
    # else:
    #     keep_prob = num_aug / len(augmented_sentences)
    #     augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    # augmented_sentences.append(seg_list)

    return augmented_sentences
