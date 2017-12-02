#!/usr/bin/env python
# coding=utf-8

import logging

"""
准备给GBDT输入的feature
输入： 可能为train_file,也可能为test_file

"""
import argparse, csv, sys

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
parser.add_argument('--dense_path', type=str,help="输出稠密型feature")
parser.add_argument('--sparse_path',type=str,help="输出稀疏型feature")

args = parser.parse_args()

"""
训练样本总共有7377418条
根据count.py统计，以下feature出现次数超过xxx次， 可以视为dense feature
"""

feature_str='msno,song_id,source_system_tab,source_screen_name,source_type,target,song_length,genre_ids,artist_name,composer,lyricist,language,city,bd,gender,registered_via,expiration_date,membership_days,registration_year,registration_month,registration_date,expiration_year,expiration_month,song_year,genre_ids_count,lyricists_count,composer_count,is_featured,artist_count,artist_composer,artist_composer_lyricist,song_lang_boolean,smaller_song,count_song_played,count_artist_played'

# target_cat_feats里面的内容需要通过上一步输出的结果来确定
target_cat_feats = []
numerical_feature=['song_length','membership_days','genre_ids_count','lyricists_count','composer_count','artist_count','count_song_played','count_artist_played']
categorical_feature=[feature for feature in feature_str.split(",") and feature not in numerical_feature]
with open(args['dense_path'], 'w') as f_d, open(args['sparse_path'], 'w') as f_s:
    for row in csv.DictReader(open(args['csv_path'])):
        feats = []
        cat_feats = set()
        for feature in numerical_feature:
            value = row[feature]
            feats.append(value)
        for feature in categorical_feature:
            key = feature + "-" + row[feature]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
        if feat in cat_feats:
            feats.append(str(j))
        f_s.write(label + ' ' + ' '.join(feats) + '\n')
