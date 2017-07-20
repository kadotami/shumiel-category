# coding: utf-8
from flask import Flask, request, jsonify, url_for, abort, Response
from functools import wraps
from gensim.models.word2vec import Word2Vec as w
import argparse
import base64
import sys
import MeCab
from collections import defaultdict
from flask_cors import CORS, cross_origin



app = Flask("test")

@app.route("/")
def hello():
    return "Hello, Flask!"

@app.route('/category', methods=['POST'])
@cross_origin()
def create():
    if not request.json or not 'query' in request.json:
        abort(400)
    query = request.json['query']
    categories = [
        u"読書",
        u"スポーツ",
        u"ゲーム",
        u"音楽",
        u"グルメ",
        u"旅行",
        u"アニメ",
        u"アウトドア",
        u"健康",
    ]
    words = []
    not_in_model = 0
    cat_val = defaultdict(lambda: 0)
    # mecab = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    mecab = MeCab.Tagger('-Owakati -d /opt/local/lib/mecab/dic/mecab-ipadic-neologd')
    mecab.parse('')
    node = mecab.parseToNode(query)
    while node:
        if node.feature.split(",")[0] == u'名詞':
            words.append(node.surface)
        node = node.next
    for cat in categories:
        for word in words:
            try:
                cat_val[cat] += model.similarity(word, cat)
            except:
                not_in_model += 1
        if ((len(words) - not_in_model) != 0):
            cat_val[cat] = cat_val[cat]/(len(words) - not_in_model)
        else:
            cat_val[cat] = 0

    return jsonify(cat_val), 201

if __name__ == "__main__":
    global model
    model_path = "./vec.bin"
    model = w.load_word2vec_format(model_path, binary=True, unicode_errors='ignore')
    app.run()