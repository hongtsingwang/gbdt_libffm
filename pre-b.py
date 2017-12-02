#!/usr/bin/env python
# coding=utf-8

import logging

import argparse, csv, sys


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nr_bins', type=int, default=int(1e+6))
parser.add_argument('-t', '--threshold', type=int, default=int(10))
parser.add_argument('csv_path', type=str)
parser.add_argument('gbdt_path', type=str)
 parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

target_cat_feats = []
numerical_feature=['song_length','membership_days','genre_ids_count','lyricists_count','composer_count','artist_count','count_song_played','count_artist_played']
categorical_feature=[feature for feature in feature_str.split(",") and feature not in numerical_feature]
with open(args['dense_path'], 'w') as f_d, open(args['sparse_path'], 'w') as f_s:

def gen_feats(row):
    feats = []
    for field in numerical_feature:
        value = row[field]
        if value != '':
            value = int(value)
            if value > 2:
                value = int(math.log(float(value))**2)
            else:
                value = 'SP'+str(value)
        key = field + '-' + str(value)
        feats.append(key)
    for j in categorical_feature:
        field = j
        value = row[field]
        key = field + '-' + value
        feats.append(key)
    return feats


def read_freqent_feats(threshold=10):
    frequent_feats = set()
    for row in csv.DictReader(open('fc.trva.t10.txt')):
        if int(row['Total']) < threshold:
            continue
        frequent_feats.add(row['Field']+'-'+row['Value'])
    return frequent_feats

def gen_hashed_fm_feats(feats, nr_bins):
    feats = ['{0}:{1}:1'.format(field-1, hashstr(feat, nr_bins)) for (field, feat) in feats]
    return feats

with open(args['out_path'], 'w') as f:
    for row, line_gbdt in zip(csv.DictReader(open(args['csv_path'])), open(args['gbdt_path'])):
        feats = []
        for feat in gen_feats(row):
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            feats.append((field, feat))
        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i)+":"+feat))
        feats = gen_hashed_fm_feats(feats, args['nr_bins'])
