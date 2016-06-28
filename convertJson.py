#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import re

def dealWithZhidao(filename):
    f = open(filename, 'r')
    oup = filename.replace('.json', '.txt')
    fw = open(oup, 'w')
    for line in f:
        s = json.loads(line)
        ques = s['question']
        ans = s['answer'].replace('##', '\t')
        if ques == None or ans == None:
            continue
        newLine=remove_punctuation(ques) + '\t' + remove_punctuation(ans) + '\n'
        fw.write(newLine)


def dealWithTieba(filename):
    f = open(filename, 'r')
    oup = filename.replace('.json', '.txt')
    fw = open(oup, 'w')
    for line in f:
        s = json.loads(line)
        title = s['title']
        text = s['text']
        if title == None or text == None:
            continue
        newLine = remove_punctuation(title) + '\t' + remove_punctuation(text) + '\n'
        fw.write(newLine)


def dealWithWangyi(filename):
    f = open(filename,'r')
    oup = filename.replace('.json', '.txt')
    fw = open(oup, 'w')
    for line in f:
        s = json.loads(line)
        title = s['title']
        text = s['text']
        if title == None or text == None:
            continue
        newline=remove_punctuation(title) + '\t' + remove_punctuation(text) + '\n'
        fw.write(newline)

def remove_punctuation(line):
    rule = re.compile(ur"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line


if __name__ == '__main__':
    filename = sys.argv[1]
    if filename.endswith('zhidao.json'):
        dealWithZhidao(filename)
    elif filename.endswith('tieba.json'):
        dealWithTieba(filename)
    elif filename.endswith('wangyi.json'):
        dealWithWangyi(filename)
    else:
        print 'illegal filename'
