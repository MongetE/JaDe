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


def get_pos_type(sentence):
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
            types: list
                A list of the enjambment found in the sentence. 

    """

    DET_NOUN = r'DET SPACE NOUN'
    NOUN_NOUN = r'NOUN SPACE NOUN'
    ADJ_NOUN = r'ADJ SPACE NOUN|NOUN SPACE ADJ'
    ADJ_ADJ = r'ADJ SPACE ADJ'
    NOUN_PREP = r'NOUN SPACE ADP|ADP SPACE (ADJ|DET)? NOUN'
    CROSS = r'NN _SP WDT'
    V_CHAIN = r'VERB SPACE AUX|AUX SPACE VERB'
    ADV_ADV = r'ADV SPACE ADV'
    VERB_ADV = r'ADV SPACE VERB|VERB SPACE ADV'
    ADJ_ADV = r'ADV SPACE ADJ|ADJ SPACE ADV'
    VERB_TO = r'TO _SP VB'
    
    types = []
    tag = ""
    pos = ""
    text = ""

    for token in sentence: 
        pos += token[1] + " "
        tag += token[2] + " "
        text += str(token[0]) + " "

    if re.search(DET_NOUN, pos):
        types.append('pb_det_noun')

    if re.search(ADJ_NOUN, pos):
        types.append('pb_noun_adj')

    if re.search(ADJ_ADV, pos):
        types.append('pb_adj_adv')

    if re.search(VERB_ADV, pos):
        types.append('pb_verb_adv')

    if re.search(ADV_ADV, pos):
        types.append('pb_adv_adv')

    if re.search(ADJ_ADJ, pos):
        types.append('pb_adj_adj')

    if re.search(NOUN_PREP, pos):
        types.append('pb_noun_prep')

    if re.search(NOUN_NOUN, pos):
        types.append('pb_noun_noun')

    if re.search(CROSS, tag):
        types.append('cc_cross_clause')

    if re.search(VERB_TO, tag):
        types.append('pb_to_verb')

    if re.search(V_CHAIN, pos):
        types.append('pb_verb_chain')

    return types


def get_dep_type(tokendict):
    types = []
    dict_as_list = list(tokendict)

    if '\t' in tokendict:
        enjambment_index = dict_as_list.index('\t')
    
        for token, token_info in tokendict.items(): 
            token_index = dict_as_list.index(token)
            if len(token_info[4]) > 0:
                children = token_info[4]
                if '\t' in children: 
                    newline_index = children.index('\t')
                    del children[newline_index]
            
                for child in children: 
                    try:
                        child_infos = tokendict[child]
                        child_index = dict_as_list.index(child)

                        if child_index > enjambment_index and token_index < enjambment_index \
                            or child_index < enjambment_index and token_index > enjambment_index:

                            if child_infos[0] == 'nmod' and child_infos[1] == 'NOUN': 
                                types.append('pb_noun_noun')

                            elif child_infos[0] == 'nmod' and child[1] == 'ADJ': 
                                types.append('pb_noun_adj')

                            elif child_infos[0] == 'dobj': 
                                types.append('ex_dobj_verb')

                            elif child_infos[0] == 'nsubj': 
                                types.append('ex_subj_verb')

                            elif child_infos[0] == 'poss':
                                types.append('pb_det_noun')

                            elif child_infos[0] == 'acl' and child_infos[1] == 'VERB':
                                types.append('pb_noun_adj')

                            elif child_infos[0] == 'prt' and token_info[1] == 'VERB':
                                types.append('pb_phrasal_verb')

                            elif child_infos[0] == 'prep' and token_info[1] == 'VERB': 
                                types.append('pb_verb_prep')
                                
                            elif child_infos[0] == 'compound' and token_info[1] == 'NOUN': 
                                types.append('pb_noun_noun')
                            
                        elif child_index == enjambment_index - 1 and token_index < child_index:
                            if child_infos[0] == 'prep' and token_info[1] == 'NOUN': 
                                types.append('pb_relword')

                    except KeyError as err: 
                        continue

        
    return types