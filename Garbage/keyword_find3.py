import json
from hazm import POSTagger, word_tokenize, stopwords_list, sent_tokenize
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def rec_dd():
    return defaultdict(rec_dd)

# print(re.search(stopwords, "آمدم"))
with open('../Data/cleaned_data.json', 'r', encoding='utf-8') as jfile:
    data = json.load(jfile)
data = {int(k): v for k, v in data.items()}

posTagger = POSTagger(model='../Data/pos_tagger.model', universal_tag=False)
tagset = list({'NUM,EZ', 'ADV', 'ADP', 'ADP,EZ', 'PUNCT', 'CCONJ', 'ADJ', 'VERB',
               'NUM', 'NOUN', 'ADV,EZ', 'DET,EZ', 'INTJ', 'ADJ,EZ', 'NOUN,EZ',
               'PRON,EZ', 'PRON', 'CCONJ,EZ', 'SCONJ', 'DET'})
categories = defaultdict(list)
punct_set = list(map(re.escape, [']', '»', '–', ':', '*', '?', '…', '#', 'نخواهید_،', '؟', ')',
                 '[', '.', '&', '"', 'نخواهند_،', '+', '/', '-', ',', '!', 'نخواهد_.'
                    , '(', "'", '«', '،', '{', ';', 'نخواهد_،', '؛', '$', '}']))
def pos_tag(text):
    global posTagger, normalizer, tagset, punct_set
    tokened_sentence = word_tokenize(text)
    tags = posTagger.tag(tokens=tokened_sentence)
    # for tag in tags:
    #     if tag[1] == 'PUNCT':
    #         punct_set.add(tag[0])
    tagged_sents = [tokened_sentence[i]+"``"+tags[i][1]for i in range(len(tokened_sentence))]
    return " ".join(tagged_sents)


for article_id, article in data.items():
    article["tagged_sents"] = pos_tag(article["body"])
    categories[article["category"]].append(article_id)
    if article_id % 1000 == 0:
        print(article_id, article)
    # print(article)
# print(tagset)
# print(punct_set)

stopwords = re.compile(rf'(^|\s)({"|".join(stopwords_list())})(``)({"|".join(tagset)})')
puncts = re.compile(rf'(^|\s)({"|".join(punct_set)})(``)(PUNCT)')
ngrams = defaultdict(set)
ngram_maxwords = 3
for category, article_list in categories.items():
    for id_counter, article_id in enumerate(article_list):
        article = data[article_id]
        sentences = article["tagged_sents"]
        tags = sentences.split(" ")
        bad_indices = []
        for i, tag in enumerate(tags):
            if re.search(stopwords, tag) or re.search(puncts, tag):
                bad_indices.append(i)
        for n in range(1, ngram_maxwords + 1):
            for ngram_index in range(len(tags) - n):
                if len([index for index in bad_indices if ngram_index <= index < ngram_index + n]) > 0:
                    continue
                ngram = " ".join(tags[ngram_index: ngram_index + n])
                ngrams[category].add(ngram)
        for percent in range(40):
            if id_counter == percent * len(article_list) // 40:
                print(f"{percent/40} through {category}, {id_counter}")

tf = rec_dd()
idf = {}
for category, ngram_set in ngrams.items():
    article_list = categories[category]
    categorized_data = {k:v for k, v in data.items() if k in article_list}
    idf[category] = defaultdict(int)
    for article_id, article in categorized_data.items():
        sentences = article["tagged_sents"]
        for ngram in ngram_set:
            occurrence_count = sentences.count(ngram)
            if  occurrence_count> 0:
                tf[category][article_id][ngram] = occurrence_count
                idf[category][ngram] += 1
    print(category, ":", len(list(categorized_data.keys())))

for category, article_id in categories.items():
    article_ngrams = tf[category][article_id]
    for ngram in article_ngrams.keys():
        tf[category][article_id][ngram] /= idf[category][ngram] # + 0.001

with open('../Results/tf.json', 'w') as fp:
    json.dump(tf, fp, sort_keys=True, indent=2, ensure_ascii=False)

