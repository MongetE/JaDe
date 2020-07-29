import fnmatch
import os
import re
import sys
import pathlib
import statistics
import click
import spacy
from sklearn.metrics import classification_report
from JaDe.jade.preprocessor import preprocessor

ANNOT_DIR = r'JaDe/resources/annotated_poems'
DETECTED_DIR = r'JaDe/resources/detected'

regex_types = ['[cc_cross_clause]', '[pb_adj_adj]', '[pb_noun_adj]', '[pb_det_noun]', '[pb_noun_noun]', '[pb_noun_prep]',
                '[pb_verb_adv]', '[pb_verb_chain]', '[pb_verb_prep]', '[pb_adv_adv]', '[pb_to_verb]', '[pb_verb_cprep]', 
                '[pb_comp]']
dependency_rules = ['[pb_noun_noun]', '[pb_det_noun]', '[pb_noun_adj]', '[pb_verb_prep]', '[pb_verb_chain]', '[pb_adj_adv]', '[pb_verb_adv]', 
                '[ex_dobj_verb]', '[ex_subj_verb]', '[pb_phrasal_verb]', '[cc_cross_clause]', '[pb_adj_prep]', '[pb_relword]', 
                '[ex_verb_adjunct]']
pdict = ['[pb_phrasal_verb]', '[ex_dobj_pverb]']


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
        # print(filename)
        out_file = str(out_dir) + '/' + filename

        with open(str(file), 'r', encoding='utf-8') as curfile: 
            preprocessor(curfile, True, out_file, nlp)
            

def get_manual_annotations(file, classifier): 
    """
        Retrieve manual annotation
    """
    with open(file, 'r', encoding='utf-8') as poem_file:
        poem = poem_file.read()
        poem_annotations = []

        all_annotations = re.findall(r'^(\d{2,} \d{2,})(.*)', poem, flags=re.MULTILINE)
        for annotated_line in all_annotations:
            line_annotation = annotated_line[1].split(' ')
            wanted = line_annotation[1]

            if classifier == 'all':
                if not 'lex' in wanted:
                    poem_annotations.append(wanted)
                else: 
                    poem_annotations.append('[]')
            
            elif classifier == 'dependencies': 
                if wanted in dependency_rules: 
                    poem_annotations.append(wanted)
                elif len(wanted) > 2:
                        poem_annotations.append('[?]')
                else: 
                    poem_annotations.append('[]')

            elif classifier == 'regex': 
                if wanted in regex_types: 
                    poem_annotations.append(wanted)
                elif len(wanted) > 2:
                        poem_annotations.append('[?]')
                else: 
                    poem_annotations.append('[]')

            elif classifier == 'dictionary': 
                if wanted in pdict: 
                    poem_annotations.append(wanted)
                elif len(wanted) > 2:
                        poem_annotations.append('[?]')
                else: 
                    poem_annotations.append('[]')

    return tuple(poem_annotations)


def get_detected_annotations(file, classifier):
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

                if classifier == 'all':
                    poem_annotations.append(annotation)
                
                elif classifier == 'dependencies': 
                    if annotation in dependency_rules: 
                        poem_annotations.append(annotation)
                    elif len(annotation) > 2:
                        poem_annotations.append('[?]')
                
                elif classifier == 'regex': 
                    if annotation in regex_types: 
                        poem_annotations.append(annotation)
                    elif len(annotation) > 2:
                        poem_annotations.append('[?]')

                
                elif classifier == 'dictionary': 
                    if annotation in pdict: 
                        poem_annotations.append(annotation)
                    elif len(annotation) > 2:
                        poem_annotations.append('[?]')
                
            else: 
                poem_annotations.append('[]')
                
    return tuple(poem_annotations)


def build_classification_report(classifier):
    """
        Build global dictionnary so that skickit metrics can be used 
        and compute detection measures. Compute precision, recall and f1-score
        for detection task as well. 
    """
    annotations = {}
    global_ = {'true': [], 'predicted': []}

    tmp_true = []
    for filepath in pathlib.Path(ANNOT_DIR).iterdir():
        filename = str(filepath)
        poem_name = str(filepath)[31:]
        annotations[poem_name] = []
        annotations[poem_name].append(get_manual_annotations(filename, classifier))
        tmp_true.append(tuple(get_manual_annotations(filename, classifier)))


    tmp_predicted = []
    for filepath in pathlib.Path(DETECTED_DIR).iterdir():
        filename = str(filepath)
        curr_poem_name = filename[24:]
        for poem in annotations.keys():
            if poem == curr_poem_name:
                annotations[poem].append(get_detected_annotations(filename, classifier))
        tmp_predicted.append(get_detected_annotations(filename, classifier))

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
        manual_annotations = enjambments[0]
        automatic_annotations = enjambments[1]
        for i in range(len(manual_annotations)):
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



@click.command()
@click.option('--model', help="Language model to be used", default='en_core_web_sm')
@click.option('--classifier', help="Classifier to evaluate", default="all", 
            type=click.Choice(['all', 'dependencies', 'regex', 'dictionary', 'dep', 'dict'], 
                            case_sensitive=False))
@click.option('--annotate', help="If set to True, run JaDe to annotate test data", default=False)
def run(model, classifier, annotate): 
    """
        Evaluation command-line interface. 

        The evaluation can be run on each classifier separately or on all 3.
        The automatic annotation can be updated if necessary (set --annotate 
        to True). 

        Parameters
        ----------
            model: str
                language model to be used. Default to spaCy smaller model.
            classifier: str
                classifier on which evaluation is to be performed. Default to all.
                See run_eval.py --help for a list of accepted values.
            annotate: bool
                whether JaDe should be run to update automatic test data. 
                Default to False. 
    """
    if annotate:
        preprocess_annotated(model)
    build_classification_report(classifier)


if __name__ == "__main__":
    run()