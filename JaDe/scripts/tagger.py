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
    for enj_pair in json_dict:
        tok_sent = " ".join(enj_pair.get('tok_before')) + "%%" + " ".join(enj_pair.get('tok_after'))
        pos_sent = " ".join(enj_pair.get('pos_before')) + "%%" + " ".join(enj_pair.get('pos_after'))
        tag_sent = " ".join(enj_pair.get('tags_before')) + "%%" + " ".join(enj_pair.get('tags_after'))

        sents[tok_sent] = {'pos': pos_sent, 'tags': tag_sent}
    return sents


def tagger(sents):
    DET_NOUN = r'DET ((ADJ)?){1,2}%%(1)?NOUN'
    ADJ_NOUN = r'ADJ%%((ADJ)?){1,2}NOUN|NOUN(1)?%%ADJ'
    NOUN_PREP = r'NOUN%%ADP'
    CROSS = r'NN%%WDT|NN%%IN'
    V_CHAIN = r'VERB%%AUX|AUX%%VERB'

    pb_det_noun = 0
    pb_adj_noun = 0
    pb_noun_prep = 0
    cc_cross_clause = 0
    pb_v_chain = 0

    for tok_sent, tagged_sent in sents.items():
        pos_sent = tagged_sent['pos']
        tag_sent = tagged_sent['tags']

        if re.search(DET_NOUN, pos_sent):
            det_noun = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_det_noun'
            print(det_noun)
            pb_det_noun += 1

        if re.search(ADJ_NOUN, pos_sent):
            adj_noun = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_adj_noun'
            print(adj_noun)
            pb_adj_noun += 1

        if re.search(NOUN_PREP, pos_sent):
            noun_prep = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_noun_prep'
            print(noun_prep)
            pb_noun_prep += 1

        if re.search(CROSS, tag_sent):
            cross = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' cc_cross_clause'
            print(cross)
            cc_cross_clause += 1

        if re.search(V_CHAIN, pos_sent):
            v_chain = tok_sent.split('%%')[0] + '\n' + tok_sent.split('%%')[1] + ' pb_v_chain'
            print(v_chain)
            pb_v_chain += 1

    return pb_det_noun, pb_adj_noun, pb_noun_prep, cc_cross_clause, pb_v_chain

if __name__ == '__main__':
    dir = 'data/tokenized_enj_pairs'
    pb_det_noun = 0
    pb_adj_noun = 0
    pb_noun_prep = 0
    cc_cross_clause = 0
    pb_v_chain = 0

    for filepath in pathlib.Path(dir).iterdir():
        print(str(filepath))
        json_dict = load_file(str(filepath))
        sents = reconstruct_pos_sent(json_dict)
        if sents is not None:
            tagger(sents)
            dn, an, np, cc, vc = tagger(sents)

        pb_det_noun += dn
        pb_adj_noun += an
        pb_noun_prep += np
        cc_cross_clause += cc
        pb_v_chain += vc

    print(f"""\n
det_noun: {pb_det_noun}, 
adj_noun: {pb_adj_noun}, 
noun_prep: {pb_noun_prep}, 
cross_clause: {cc_cross_clause}, 
v_chain: {pb_v_chain}""")
    
