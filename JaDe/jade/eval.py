import fnmatch
import os
import re
import sys
import pathlib
import statistics
import spacy
from sklearn.metrics import classification_report
from preprocessor import preprocessor

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


def preprocess_annotated(model):
    """
        Run the preprocessor against test data
    """
    nlp = spacy.load(model)
    data_dir = pathlib.Path('JaDe/resources/annotated_poems')
    out_dir = pathlib.Path('JaDe/resources/detected')
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for file in data_dir.iterdir():
        filename = str(file)[31:]
        print(filename)
        out_file = str(out_dir) + '/' + filename

        with open(str(file), 'r', encoding='utf-8') as curfile: 
            preprocessor(curfile, True, out_file, nlp)
            

def get_manual_annotations(file): 
    """
        Retrieve manual annotation
    """
    with open(file, 'r', encoding='utf-8') as poem_file:
        poem = poem_file.read()
        poem_annotations = []

        all_annotations = re.findall(r'^(\d{2,} \d{2,})(.*)', poem, flags=re.MULTILINE)
        for annotated_line in all_annotations:
            line_annotation = annotated_line[1].split(' ')
            poem_annotations.append(line_annotation[1])
    
    return tuple(poem_annotations)


def get_detected_annotations(file):
    """
        Retrieve automatic annotation. 
        Since contrary to manual annotation, the [] are not added if the 
        line is end-stopped, append dummy brackets if line is end-stopped.
    """
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
    """
        Build global dictionnary so that skickit metrics can be used 
        and compute detection measures. 
    """

    model = input('Model to be used for evaluation: ')
    preprocess_annotated(model)

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
        # print(poem)
        manual_annotations = enjambments[0]
        automatic_annotations = enjambments[1]
        # print(manual_annotations)
        # print(automatic_annotations)
        # print(classification_report(manual_annotations, automatic_annotations, digits=3))
        # print()
        for i in range(len(manual_annotations)):
            # print(manual_annotations[i], automatic_annotations[i])
            if manual_annotations[i] != "[]" and automatic_annotations[i] != '[]':
                true_positive += 1
            elif manual_annotations[i] == automatic_annotations[i]:
                true_positive += 1
            elif automatic_annotations[i] == "[]" and manual_annotations[i] != "[]":
                false_negative += 1
            elif manual_annotations[i] == "[]" and automatic_annotations[i] != "[]":
                false_positive += 1
            else : 
                true_negative += 1

            # print(true_positive, true_negative, false_positive, false_negative)

        detection_precision = true_positive/(true_positive + false_positive)
        detection_recall = true_positive/(true_positive + false_negative)
        detection_fscore = 2 * ((detection_precision * detection_recall)/(detection_precision + detection_recall))
#             print(f"detection_precision\t\tdetection_recall\t\tdetection_fscore\n\
# {detection_precision}\t\t{detection_recall}\t\t{detection_fscore}")

        precision.append(detection_precision)
        recall.append(detection_recall)
        fscore.append(detection_fscore)

        true_positive = 0
        true_negative = 0 
        false_positive = 0 
        false_negative = 0 

    print(f"detection_precision\t\tdetection_recall\t\tdetection_fscore\n\
{statistics.mean(precision):.2f}\t\t\t\t{statistics.mean(recall):.2f}\t\t\t\t{statistics.mean(fscore):.2f}\n")


    manual_annotations = global_['true']
    automatic_annotations = global_['predicted']
    print(classification_report(manual_annotations, automatic_annotations, digits=3, zero_division=0))