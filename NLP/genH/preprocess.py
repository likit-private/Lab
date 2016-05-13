# -*- coding: utf-8 -*-

s = open('sfbj1.txt').read().decode('utf-8').replace(u'\ufeff', "")

with open('sfbj1.txt', 'w') as f:
    f.write(s.encode('utf-8'))