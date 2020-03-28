import json
import pathlib
import re


# TODO: move load_file function to a utils.py file
# TODO: move all reconstruct_* to a utils.py as well
def load_file(filepath):
    with open(str(filepath), 'r', encoding='utf-8') as file:
        json_dict = json.load(file)

    return json_dict


def reconstruct_pos_sent(json_dict):
    sents = {}
    for item in json_dict:
        tok_sent = " ".join(item.get('tok_before')) + "%%" + " ".join(item.get('tok_after'))
        pos_sent = " ".join(item.get('pos_before')) + "%%" + " ".join(item.get('pos_after'))

        sents[tok_sent] = pos_sent

    return sents


def tagger(sents):
    DET_NOUN = r'DET ((ADJ)?){1,2}%%(1)?NOUN'
    ADJ_NOUN = r'ADJ%%((ADJ)?){1,2}NOUN|NOUN(1)?%%ADJ'
    NOUN_PREP = r'NOUN%%ADP'
    CROSS = r'NOUN%%SCONJ'
    V_CHAIN = r'VERB%%AUX|AUX%%VERB'

    for tok_sent, pos_sent in sents.items():
        if re.search(DET_NOUN, pos_sent):
            det_noun = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_det_noun'
            print(det_noun)

        if re.search(ADJ_NOUN, pos_sent):
            adj_noun = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_adj_noun'
            print(adj_noun)

        if re.search(NOUN_PREP, pos_sent):
            noun_prep = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_noun_prep'
            print(noun_prep)

        if re.search(CROSS, pos_sent):
            cross = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' cc_cross_clause'
            print(cross)

        if re.search(V_CHAIN, pos_sent):
            v_chain = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_v_chain'
            print(v_chain)

if __name__ == '__main__':
    dir = 'data/tokenized_enj_pairs'

    for filepath in pathlib.Path(dir).iterdir():
        print(str(filepath))
        json_dict = load_file(str(filepath))
        sents = reconstruct_pos_sent(json_dict)
        if sents is not None:
            test = tagger(sents)