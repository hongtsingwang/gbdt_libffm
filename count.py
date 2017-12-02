#!/usr/bin/env python
# coding=utf-8

import logging
import argparse
import sys

"""
统计每个feature的数量。 确定哪些feature是稠密型feature， 哪些是稀疏型feature
外部调用命令example: python count.py --train_file='../input/train.txt' --output_file='./feature_count.txt'
"""

from collections import defaultdict
from csv import DictReader

parser = argparse.ArgumentParser()
parser.add_argument("--train_file", help="输入文件路径", type=file)
parser.add_argument("--output_category_count_file", help="输出feature统计路径",type=str)
args = parser.parse_args()


counts = collections.defaultdict(lambda : [0, 0, 0])
train_path = args.train_file
output_file = open(args.output_category_count_file, "w")

numerical_feature=['song_length','membership_days','genre_ids_count','lyricists_count','composer_count','artist_count','count_song_played','count_artist_played']
for i, row in enumerate(DictReader(open(train_path, "r"), start=1):
    label = row['target']
    for key,value in row.items():
        if key == 'target':
            continue
        if key in numerical_feature:
            continue
        else:
            field = key
            if label=='0':
                counts[field+','+value][0] += 1
            else:
                counts[field+','+value][1] += 1
            counts[field+','+value][2] += 1


output_file.write('Field,Value,Neg,Pos,Total,Ratio\n')
for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
    if total < 10:
        # 出现数量过少， feature准确性太低， 不可靠， 直接过滤
        continue
     ratio = round(float(pos)/total, 5)
     output_file.write(key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio))
     output_file.write("\n")

output_file.close()
