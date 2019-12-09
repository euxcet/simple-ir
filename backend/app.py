from flask import Flask, request, jsonify
from flask_cors import CORS
from elastic import Elastic
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)
elastic = Elastic()

def remove_class(doc):
    return "".join(map(lambda x: x.split('/')[0], doc))

def get_class(word):
    return word.split('/')[1]

option_dict = dict()
class_name = ['名词', '人名', '地名', '机构名', '其它专名', '数词', '量词', '数量词', '时间词', '方位词', '处所词', '动词', '形容词', '副词', '前接成分', '后接成分', '习语', '简称', '代词', '连词', '介词', '助词', '语气助词', '叹词', '拟声词', '语素', '标点', '其它']
class_type = ['n', 'np', 'ns', 'ni', 'nz', 'm', 'q', 'mq', 't', 'f', 's', 'v', 'a', 'd', 'h', 'k', 'i', 'j', 'r', 'c', 'p', 'u', 'y', 'e', 'o', 'g', 'w', 'x']
for i in range(len(class_name)):
    option_dict[class_name[i]] = class_type[i]

def gen_word_pattern(word, options):
    pattern = r'' + word + '/('
    first_option = True
    for option in options:
        if first_option:
            pattern = pattern + option_dict[option]
            first_option = False
        else:
            pattern = pattern + "|" + option_dict[option]
    pattern = pattern + ')'
    return pattern

def gen_pattern(words, options):
    return map(lambda word: gen_word_pattern(word, options), words)


def search_doc(words, phrase_word, options, window_len):
    search_pattern = gen_pattern(words, options)
    word_pattern = gen_word_pattern(phrase_word, options)
    result = elastic.search_doc_multi(search_pattern).json()
    phrase_set = set()
    docs = []
    for hit in result["hits"]["hits"]:
        doc = hit["_source"]['content'].split(' ')
        doc_without_class = remove_class(doc)
        for i in range(len(doc)):
            if re.match(word_pattern, doc[i]):
                for start in range(-window_len, 1):
                    valid = True
                    for j in range(window_len + 1):
                        if i + start + j < 0 or i + start + j >= len(doc) or get_class(doc[i + start + j]) == 'w' or get_class(doc[i + start + j]) == 'x':
                            valid = False
                            break

                    if valid:
                        phrase = remove_class(doc[i + start : i + start + window_len + 1])
                        if phrase not in phrase_set:
                            phrase_set.add(phrase)
                            docs.append({
                                'phrase': phrase,
                                'doc': doc_without_class
                            })
    return docs


@app.route('/search', methods = ['POST'])
def search():
    word = request.json['word']
    option = request.json['option']
    window = request.json['window']
    if len(word) == 0:
        return jsonify({
            'pair': []
        })
    else:
        word_s = word.split(' ')
        docs = search_doc(word_s, word_s[0], option, window)
        return jsonify({
            'pair': docs
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0')