import json
import os
import pathlib
import re
import spacy

# TODO: create preprocess pipeline or file → need POS and dependencies


def load_file(filepath):
    with open(str(filepath), 'r', encoding='utf-8') as file:
        json_dict = json.load(file)

    return json_dict


def reconstruct_poem(json_dict):
    poem = ""
    last_words_enj = []
    last_words_end = []
    for item in json_dict:
        line_pair = item.get('text')
        if item == json_dict[0]:
            if '%%' in line_pair:
                poem += line_pair.lower().split('%%')[0] + line_pair.lower().split('%%')[1]
                last_words_enj.append(re.search(r'\w*(?=%%)', line_pair).group(0))
            elif '&&' in line_pair:
                poem += line_pair.lower().split('&&')[0] + line_pair.lower().split('&&')[1]
                last_words_end.append(re.search(r'\w*(?=\W&&)', line_pair).group(0))
        else:
            if "&&" in line_pair:
                poem += line_pair.lower().split('&&')[1]
                last_words_end.append(re.search(r'\w*(?=\W&&)', line_pair).group(0))
            else:
                poem += line_pair.lower().split('%%')[1]
                last_words_enj.append(re.search(r'\w*(?=%%)', line_pair).group(0))

    return poem, last_words_enj, last_words_end


def get_sentences(poem):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(poem)
    sentences = [str(sent) for sent in doc.sents]
    tokens_in_sent = [[str(token) for token in nlp(sentence)] for sentence in sentences]
    return sentences, tokens_in_sent


if __name__ == '__main__':
    dir = 'data/annotations'

    if not pathlib.Path(r'data/tokenized_enj_pairs').exists():
        os.mkdir(r'data/tokenized_enj_pairs')

    for filepath in pathlib.Path(dir).iterdir():
        print(str(filepath))
        json_dict = load_file(str(filepath))
        reconstructed, last_words_enj, last_words_end = reconstruct_poem(json_dict)
        sentences, tokens_in_sents = get_sentences(reconstructed)

        enjs = []
        for i in range(len(sentences)):
            for word in last_words_enj:
                if word != '' and word in tokens_in_sents[i]:
                    enj = {}
                    enj_position = tokens_in_sents[i].index(word)
                    enj['before'] = tokens_in_sents[i][:enj_position+1]
                    enj['after'] = tokens_in_sents[i][enj_position+1:]
                    enjs.append(enj)

        with open(str(filepath).replace(dir, 'data/tokenized_enj_pairs'), 'w', encoding='utf-8') as file:
            json.dump(enjs, file)