"""
   JaDe is a command-line tool to automatically detect enjambment in English 
   poetry. This file should be used to evaluate JaDe. Further information on 
   how to run it can be found using `python evaluation.py --help"

    Copyright (C) 2020  Eulalie Monget

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import fnmatch
import os
import re
import sys
import pathlib
import statistics
import click
import spacy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm
from JaDe.jade.processing import processor

ANNOT_DIR = r'JaDe/resources/annotated_poems'
DETECTED_DIR = r'JaDe/resources/detected'

regex_types = ['[cc_cross_clause]', '[pb_adj_adj]', '[pb_noun_adj]', '[pb_det_noun]', '[pb_noun_noun]', '[pb_noun_prep]',
                '[pb_verb_adv]', '[pb_verb_chain]', '[pb_verb_prep]', '[pb_adv_adv]', '[pb_to_verb]', '[pb_verb_cprep]', 
                '[pb_comp]', '[pb_adj_adv]', '[ex_subj_verb]', '[ex_dobj_verb]']
dependency_rules = ['[pb_noun_noun]', '[pb_det_noun]', '[pb_noun_adj]', '[pb_verb_prep]', '[pb_verb_chain]', '[pb_adj_adv]',
                     '[pb_verb_adv]', '[ex_dobj_verb]', '[ex_subj_verb]', '[pb_phrasal_verb]', '[cc_cross_clause]', 
                     '[pb_adj_prep]', '[pb_relword]', '[ex_verb_adjunct]', '[pb_noun_prep]']
pdict = ['[pb_phrasal_verb]', '[ex_dobj_pverb]']


def get_filename(file): 
    filename = re.search(r'(\w*[\/\\])+(?P<name>(\w*[ _\-\d]?)+)', str(file)).group('name')
    filename = re.sub(r'[\?:;,\'! \.]', '_', filename)
    filename = filename + '.txt'

    if filename.endswith('_'):
        filename = filename[:-1]
    
    return filename


def process_annotated(model, classifier):
    """
        Run the processor against test data
    """
    nlp = spacy.load(model)
    data_dir = pathlib.Path('JaDe/resources/annotated_poems')
    out_dir = pathlib.Path('JaDe/resources/detected')
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    files = [str(data_dir)+'/'+file for file in os.listdir(data_dir) if fnmatch.fnmatch(file, '*.txt')]

    for i in tqdm(range(len(files))):
        with open(files[i], 'r', encoding='utf-8') as curfile:
            file_name = get_filename(str(files[i]))
            out_file = str(out_dir) + '/' + file_name
            processor(curfile, True, out_file, nlp, classifier=classifier, is_eval=True)
            

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
                if not 'lex' in wanted and len(wanted) > 2:
                    poem_annotations.append(wanted)
                else: 
                    poem_annotations.append('[]')
            
            elif classifier == 'dependencies': 
                if wanted in dependency_rules: 
                    poem_annotations.append(wanted)
                else: 
                    poem_annotations.append('[]')

            elif classifier == 'regex': 
                if wanted in regex_types: 
                    poem_annotations.append(wanted)
                else: 
                    poem_annotations.append('[]')

            elif classifier == 'dictionary': 
                if wanted in pdict: 
                    poem_annotations.append(wanted)
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
            if len(poem[i]) > 1:
                if re.search(r'\[.*?\]', poem[i]):
                    annotation = re.search(r'\[.*?\]', poem[i]).group(0)

                    if classifier == 'all':
                        poem_annotations.append(annotation)
                    
                    elif classifier == 'dependencies':  
                        if annotation in dependency_rules: 
                            poem_annotations.append(annotation)
                        else:
                            poem_annotations.append('[]')

                    
                    elif classifier == 'regex': 
                        if annotation in regex_types: 
                            poem_annotations.append(annotation)
                        else:
                            poem_annotations.append('[]')
                    
                    elif classifier == 'dictionary': 
                        if annotation in pdict: 
                            poem_annotations.append(annotation)
                        else:
                            poem_annotations.append('[]')
                else: 
                    poem_annotations.append('[]')
                    
    return tuple(poem_annotations)


def build_classification_report(classifier, confusion):
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
        poem_name = filename[31:]
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


    manual_annotations = global_['true']
    automatic_annotations = global_['predicted']
    labels = (list(set(dependency_rules + regex_types + pdict)))

    # evaluating detection with scikit
    print("\t####### DETECTION #######")
    automatic_annotations_detection = [0  if x == '[]' else 1 for x in automatic_annotations]
    manual_annotations_detection = [0 if x == '[]' else 1 for x in manual_annotations]
    print(classification_report(manual_annotations_detection, automatic_annotations_detection, digits=3, zero_division=0))

    both = list(zip(manual_annotations, automatic_annotations))
    # ignore empty labels
    both_filtered = []
    for x in both: 
        x = list(x)
        if x[0] != '[]': 
            if x[1] == '[]':
                x[1] = 'None'
            both_filtered.append(x)
    
    manual_annotations_filt = [x[0] for x in both_filtered]
    automatic_annotations_filt = [x[1] for x in both_filtered]
   
    print("\n\t###### CLASSIFICATION ######")
    automatic_annotations = automatic_annotations_filt
    manual_annotations = manual_annotations_filt
    labels = list(set(manual_annotations))
    print(classification_report(manual_annotations, automatic_annotations, labels=labels, digits=3, zero_division=0))
    
    
    manual_annotations_filt = [x[0] for x in both_filtered]
    automatic_annotations_filt = [x[1] for x in both_filtered]
    data = {'true': manual_annotations_filt, 'predicted': automatic_annotations_filt} 
    
    if confusion: 
        df = pd.DataFrame(data, columns=['true', 'predicted'])
        confusion_matrix = pd.crosstab(df['true'], df['predicted'], rownames=['actual'], colnames=['predicted'])
        sn.heatmap(confusion_matrix, annot=False, robust=True)
        plt.show()


@click.command()
@click.option('--model', help="Language model to be used", default='en_core_web_sm')
@click.option('--classifier', help="Classifier to evaluate", default="all", 
            type=click.Choice(['all', 'dependencies', 'regex', 'dictionary'], 
                            case_sensitive=False))
@click.option('--confusion', help="Display confusion matrix in new window", default=False)
@click.option('--annotate', help="If set to True, run JaDe to annotate test data", default=False)
def run(model, classifier, annotate, confusion): 
    """
        Evaluation command-line interface. 
        The evaluation can be run on each classifier separately or on all 3.
        The automatic annotation can be updated if necessary, for example when 
        evaluating another classifier (set --annotate to True). 

        Parameters
        ----------
            model: str
                language model to be used. Default to spaCy smaller model.
            classifier: str
                classifier on which evaluation is to be performed. Default to all.
                See evaluation.py --help for a list of accepted values.
            annotate: bool
                whether JaDe should be run to update automatic test data. 
                Default to False. 
            confusion: bool
                whether the confusion matrix should be displayed (in a new window). 
                Default to False
    """
    bool_true = ['true', 'True']
    if annotate in bool_true:
        annotate = True
    else:
        annotate = False

    if confusion in bool_true:
        confusion = True
    else:
        confusion = False
    
    if annotate:
        process_annotated(model, classifier)
    build_classification_report(classifier, confusion)


if __name__ == "__main__":
    run()


