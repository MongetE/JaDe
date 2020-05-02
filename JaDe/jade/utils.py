import json
import re


def load_dict(filepath):
    """
        Load json file. 

        Parameters:
        -----------
            filepath: str
                Path to the file to be read
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        dict_ = json.load(file)

    return dict_


def dump_dict(filepath, dictname):
    """
        Dump python dictionary into a json file.

        Parameters
        ----------
            filepath: str
                Path where the dictionary will be saved

            dictname: dict
                Dictionary to dump
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(dictname, file, ensure_ascii=False)


def get_tag(sentence):
    """
        Retrieve the type of enjambment present in a sentence. 

        The sentence is formatted according to its original form 
        in the poem, meaning that the newline character is 
        still present.  

        Parameters
        ----------
            sentence: list
                The tokenized sentence. Each object in the sentence is 
                a tuple (token, pos, tag)

        Returns
        -------
            tags: list
                A list of the enjambment found in the sentence. 

    """

    print(sentence)

    DET_NOUN = r'DET SPACE NOUN'
    NOUN_NOUN = r'NOUN SPACE NOUN'
    ADJ_NOUN = r'ADJ SPACE NOUN|NOUN SPACE ADJ'
    ADJ_ADJ = r'ADJ SPACE ADJ'
    NOUN_PREP = r'NOUN SPACE ADP'
    CROSS = r'NN SPACE WDT'
    V_CHAIN = r'VERB SPACE AUX|AUX SPACE VERB'
    ADV_ADV = r'ADV SPACE ADV'
    VERB_ADV = r'ADV SPACE VERB|VERB SPACE ADV'
    ADJ_ADV = r'ADV SPACE ADJ'

    tags = []

    if re.search(DET_NOUN, sentence[1]):
        tags.append('pb_det_noun')

    if re.search(ADJ_NOUN, sentence[1]):
        tags.append('pb_adj_noun')

    if re.search(ADJ_ADV, sentence[1]):
        tags.append('pb_adj_adv')

    if re.search(VERB_ADV, sentence[1]):
        tags.append('pb_verb_adv')

    if re.search(ADV_ADV, sentence[1]):
        tags.append('pb_adv_adv')

    if re.search(ADJ_ADJ, sentence[1]):
        tags.append('pb_adj_noun')

    if re.search(NOUN_PREP, sentence[1]):
        tags.append('pb_noun_prep')

    if re.search(NOUN_NOUN, sentence[1]):
        tags.append('pb_noun_noun')

    if re.search(CROSS, sentence[2]):
        tags.append('cc_cross_clause')

    if re.search(V_CHAIN, sentence[1]):
        tags.append('pb_v_chain')

    return tags