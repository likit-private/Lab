# -*- coding: utf-8 -*-

import jieba
import nltk

s = open('sfbj1.txt').read().decode('utf-8')

word_list = list(jieba.cut(s))
fd = nltk.FreqDist(word_list)
items = sorted(fd.items(), key=lambda d:d[1])

for w, cnt in items[:500]:
    print w, cnt

#words = set(word_list)
#
#word_to_ind = dict([(w,i) for (i,w) in enumerate(words)])
#ind_to_word = dict([(i,w) for (i,w) in enumerate(words)])

