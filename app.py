#-*- coding: utf-8 -*- 

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api, reqparse
from flask_restful.utils import cors
from gensim.models.word2vec import Word2Vec as w
# from gensim.models.keyedvectors import KeyedVectors as w
import argparse
import base64
import sys
import MeCab
from collections import defaultdict

class Category(Resource):
    def post(self):
        try:
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
            parser = reqparse.RequestParser()
            parser.add_argument('query', required=True, help="query cannot be blank!")
            args = parser.parse_args()
            mecab = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
            # mecab = MeCab.Tagger('-Owakati -d /opt/local/lib/mecab/dic/mecab-ipadic-neologd')
            query = args['query']
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
            return cat_val
        except(Exception, e):
            return e

    def get(self):
        try:
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
            parser = reqparse.RequestParser()
            parser.add_argument('query', required=True, help="query cannot be blank!")
            args = parser.parse_args()
            mecab = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
            query = args['query']
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
            return cat_val
        except(Exception, e):
            return e

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['POST','GET'])]

@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"

@app.errorhandler(500)
def raiseError(error):
    return error

if __name__ == '__main__':
    global model
    model_path = "./vec.bin"
    binary = True
    # host = "localhost"
    path = "/word2vec"
    # port = 5000
    model = w.load_word2vec_format(model_path, binary=binary, unicode_errors='ignore')
    api.add_resource(Category, path+'/category')
    print("starting server")
    app.run()

