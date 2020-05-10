import os
import re
import sys
import pathlib
from sklearn.metrics import classification_report

ANNOT_DIR = r'JaDe/resources/annotated_poems'
DETECTED_DIR = r'JaDe/resources/detected'
DETECTED_TYPES = [
                    'pb_noun_prep', 'pb_noun_noun', 'cc_cross_clause', 'pb_verb_adv',
                    'pb_det_noun', 'pb_v_chain', 'pb_noun_adj', 'pb_adj_adj', 
                    'pb_adv_adv', 'pb_adj_adv'
                ]

DET_NOUN = 'pb_det_noun'
NOUN_NOUN = 'pb_noun_noun'
ADJ_NOUN = 'pb_noun_adj'
ADJ_ADJ = 'pb_adj_adj'
NOUN_PREP = 'pb_noun_prep'
CROSS = 'cc_cross_clause'
V_CHAIN = 'pb_v_chain'
ADV_ADV = 'pb_adv_adv'
VERB_ADV = 'pb_verb_adv'
ADJ_ADV = 'pb_adj_adv'
END_STOPPED = ''


def get_manual_annotations(file): 

    with open(file, 'r', encoding='utf-8') as file:
        poem = file.read()
        poem_annotations = []

        all_annotations = re.findall(r'^(\d{2,} \d{2,})(.*)', poem, flags=re.MULTILINE)
        for annotated_line in all_annotations:
            line_annotation = annotated_line[1].split(' ')
            poem_annotations.append(line_annotation[1])
    
    return tuple(poem_annotations)


def get_detected_annotations(file):
    
    with open(file, 'r', encoding='utf-8') as file:
        poem = file.readlines()
        poem_annotations = []
        i = 1
        for i in range(len(poem) - 1): 
            if re.search(r'\[.*?\]', poem[i]):
                annotation = re.search(r'\[.*?\]', poem[i]).group(0)
                poem_annotations.append(annotation)
            else:
                poem_annotations.append('[]')
            
    return tuple(poem_annotations)
                

if __name__ == "__main__":
    annotations = {}
    for filepath in pathlib.Path(ANNOT_DIR).iterdir():
        filename = str(filepath)
        poem_name = str(filepath)[31:]
        annotations[poem_name] = []
        annotations[poem_name].append(get_manual_annotations(filename))

    for filepath in pathlib.Path(DETECTED_DIR).iterdir():
        filename = str(filepath)
        curr_poem_name = filename[24:]
        for poem in annotations.keys():
            if poem == curr_poem_name:
                annotations[poem].append(get_detected_annotations(filename))

    
    for poem, enjambments in annotations.items():
        print(poem)
        manual_annotations = enjambments[0]
        automatic_annotations = enjambments[1]
        print(classification_report(manual_annotations, automatic_annotations, digits=3))
        print()
        # for i in range(len(manual_annotations)):
        #     if len(automatic_annotations[i]) == len(manual_annotations[i]):
        #         print('detected: ', automatic_annotations[i], '\tmanual: ', manual_annotations[i])
