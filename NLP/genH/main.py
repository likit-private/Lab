# -*- coding: utf-8 -*-

import re
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
import numpy

start_token = 0
end_token = 1

def get_str():
    return open('sfbj.txt').read().decode('utf-8').replace("\n", "").replace(u'　', "").replace(u"「",u"“").replace(u"」",u"”").replace(u"＊","")
    
def to_sents_list(s):
    sents = re.findall(u'[^。？”]*。”|[^。？”]*？”|[^。？”]*。|[^。？”]*？|[^。？”]*”', s)
    return sents
    
def build_dict(s):
    word_to_num = {}
    num_to_word = {}
    word_to_num['START'] = 0
    word_to_num['END'] = 1
    word_cnt = {}
    for c in s:
        if c not in word_to_num:
            k = len(word_to_num)
            word_to_num[c] = k
            num_to_word[k] = c
            word_cnt[c] = 1
        else:
            word_cnt[c] = word_cnt[c] + 1
    return word_to_num, num_to_word, word_cnt
    
def code_sent(s, word_to_num):
    res = [word_to_num[c] for c in s]
    return res
    
def decode_sent(l, num_to_word):
    res = [num_to_word[c] for c in l]
    return res
    
def build_xy(s, word_to_num, num_to_word, word_cnt, data_size=200):    
    #sl = to_sents_list(s)
    sl = list(s)
    if data_size < 0:
        data_size = len(sl)
    sents = sl[:data_size]
    X = []
    y = []
    dim = len(word_to_num)
    for sent in sents:
        l = [start_token] + code_sent(sent, word_to_num) + [end_token]
        oh_l = [num_to_onehot(c, dim) for c in l]
        X.append(oh_l[:-1])
        y.append(oh_l[1:])
    return numpy.asarray(X), numpy.asarray(y)
    
def num_to_onehot(k, dim):
    res = numpy.zeros(dim)
    res[k] = 1
    return res
    
def onehot_to_num(k, dim):
    return k.find(1)
    
def run(s):
    word_to_num, num_to_word, word_cnt = build_dict(s)
    X, y = build_xy(s, word_to_num, num_to_word, word_cnt)
    
    print X.shape,y.shape
    dim = len(word_to_num)

    
    print("Number of words: %d" % dim)
    print("Number of sentences: %d" % len(X))
    
    model = Sequential()
    model.add(LSTM(output_dim=50, input_dim=dim, activation='sigmoid', inner_activation='hard_sigmoid'))
    # model.add(Dropout(0.5))
    model.add(Dense(200))
    model.add(Activation('sigmoid'))
    
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    #model.summary()
    
    model.fit(X, y, batch_size=200, nb_epoch=10)
    
    N = 200 # num of sents to be generated
    
    for i in range(N):
        model.reset_states()
        k = start_token
        res = [k]
        while k != end_token:
            k_oh = num_to_onehot(k, dim)
            kk_oh = model.predict(k_oh)
            kk = onehot_to_num(kk_oh, dim)
            k = kk
            res.append(k)
        s = ""
        for c in res:
            s = s + num_to_word(c)
        print s

    
if __name__=='__main__':
    txt = get_str()
    run(txt)
#    word_to_num, num_to_word, word_cnt = build_dict(txt)
#    items = word_cnt.items()
#    items.sort(key=lambda d: d[1], reverse=True)
#    print len(word_to_num), len(word_cnt)