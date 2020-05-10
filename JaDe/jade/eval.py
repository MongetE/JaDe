import os
import re
import sys
import pathlib
import statistics
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
    global_ = {'true': [], 'predicted': []}
    tmp_true = []
    for filepath in pathlib.Path(ANNOT_DIR).iterdir():
        filename = str(filepath)
        poem_name = str(filepath)[31:]
        annotations[poem_name] = []
        annotations[poem_name].append(get_manual_annotations(filename))
        tmp_true.append(get_manual_annotations(filename))

    tmp_predicted = []
    for filepath in pathlib.Path(DETECTED_DIR).iterdir():
        filename = str(filepath)
        curr_poem_name = filename[24:]
        for poem in annotations.keys():
            if poem == curr_poem_name:
                annotations[poem].append(get_detected_annotations(filename))
        tmp_predicted.append(get_detected_annotations(filename))

    for i in range(len(tmp_predicted)):
        for tag in tmp_predicted[i]:
            global_['predicted'].append(tag)
        for tag in tmp_true[i]:
            global_['true'].append(tag)

    true_positive = 0
    true_negative = 0 
    false_positive = 0 
    false_negative = 0 
    precision = []
    recall = []
    fscore = []
    for poem, enjambments in annotations.items():
        #print(poem)
        manual_annotations = enjambments[0]
        automatic_annotations = enjambments[1]
        # print(classification_report(manual_annotations, automatic_annotations, digits=3))
        # print()
        for i in range(len(manual_annotations)):
            if manual_annotations[i] != "[]" and automatic_annotations[i] != '[]':
                true_positive += 1
            elif automatic_annotations[i] == "[]" and manual_annotations[i] != "[]":
                false_negative += 1
            elif manual_annotations[i] == "[]" and automatic_annotations[i] != "[]":
                false_positive += 1
            else : 
                true_negative += 1

            #print('detected: ', automatic_annotations[i], '\tmanual: ', manual_annotations[i])

            detection_precision = true_positive/(true_positive + false_positive)
            detection_recall = true_positive/(true_positive + false_negative)
            detection_fscore = 2 * ((detection_precision * detection_recall)/(detection_precision + detection_recall))
#             print(f"detection_precision\t\tdetection_recall\t\tdetection_fscore\n\
# {detection_precision}\t\t{detection_recall}\t\t{detection_fscore}")

            precision.append(detection_precision)
            recall.append(detection_recall)
            fscore.append(detection_fscore)

    print(f"detection_precision\t\tdetection_recall\t\tdetection_fscore\n\
{statistics.mean(precision)}\t\t{statistics.mean(recall)}\t\t{statistics.mean(fscore)}")


    manual_annotations = global_['true']
    automatic_annotations = global_['predicted']
    print(classification_report(manual_annotations, automatic_annotations, digits=3, zero_division=0))