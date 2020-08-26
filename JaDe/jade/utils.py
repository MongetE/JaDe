import json
import re


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
    ADJ_NOUN = r'ADJ SPACE NOUN'
    VBN_NOUN = r'VBN _SP NOUN'
    ADJ_ADJ = r'ADJ SPACE ADJ'
    NOUN_PREP = r'NOUN SPACE ADP'
    CROSS = r'NN _SP (WDT|VBG)'
    V_CHAIN = r'VERB SPACE AUX|AUX SPACE VERB'
    ADV_ADV = r'ADV SPACE ADV'
    VERB_ADV = r'ADV SPACE VERB|VERB SPACE ADV'
    VBN_ADV = r'RB.? _SP (JJ.?|VBN)'
    VERB_TO = r'TO _SP VB.?'
    CPREP = r'VB.? _SP TO'
    VERB_PREP = r'VB.? _SP IN'
    COMP = r'(RB|JJ)[RS]( \w*){0,3} _SP( \w*){0,4}((JJ|RB)[RS]|IN)?'
    SUB_VERB_tag  = r'NN(.+)? _SP VB[^NG].?'
    DOB_VERB = r'VB.? _SP (\w+ ){0,2}NN(.+)?'


    # ADJ_PREP = r'ADJ SPACE ADP'
    # JJ_PREP = r'JJ _SP IN'
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

    elif re.search(ADJ_NOUN, pos) or re.search(VBN_NOUN, tag):
        types.append('pb_noun_adj')

    elif re.search(VBN_ADV, tag):
        types.append('pb_adj_adv')

    elif re.search(VERB_ADV, pos):
        types.append('pb_verb_adv')

    elif re.search(ADV_ADV, pos):
        types.append('pb_adv_adv')

    elif re.search(ADJ_ADJ, pos):
        types.append('pb_adj_adj')

    elif re.search(NOUN_PREP, pos):
        types.append('pb_noun_prep')

    elif re.search(NOUN_NOUN, pos):
        types.append('pb_noun_noun')

    elif re.search(CROSS, tag):
        types.append('cc_cross_clause')

    elif re.search(VERB_TO, tag):
        types.append('pb_to_verb')

    elif re.search(CPREP, tag): 
        types.append('pb_verb_cprep')

    elif re.search(V_CHAIN, pos):
        types.append('pb_verb_chain')

    elif re.search(VERB_PREP, tag):
        types.append('pb_verb_prep')

    elif re.search(COMP, tag): 
        types.append('pb_comp')

    elif re.search(SUB_VERB_tag, tag): 
        types.append('ex_subj_verb')

    elif re.search(DOB_VERB, tag): 
        types.append('ex_dobj_verb')

    # elif re.search(ADJ_PREP, pos) or re.search(JJ_PREP, tag): 
    #     types.append('pb_adj_prep')

    return types


def get_dep_type(tokendict):
    types = []
    dict_as_list = list(tokendict)

    if '\t' in tokendict:
        enjambment_index = dict_as_list.index('\t')
    
        for token, token_info in tokendict.items(): 
            token_index = dict_as_list.index(token)
            if len(token_info[5]) > 0:
                children = token_info[5]
                if '\t' in children: 
                    newline_index = children.index('\t')
                    del children[newline_index]
            
                for child in children: 
                    try:
                        child_infos = tokendict[child]
                        child_index = dict_as_list.index(child)

                        if child_index == (enjambment_index - 1) and token_index == (enjambment_index + 1) \
                            or child_index == (enjambment_index + 1) and token_index == (enjambment_index - 1) :

                            if child_infos[0] == 'compound' and child_infos[1] == 'NOUN': 
                                types.append('pb_noun_noun')

                            elif child_infos[0] in ['poss', 'det']:
                                types.append('pb_det_noun')
                            
                            elif child_infos[0] in ['acl', 'amod', 'nummod']:
                                types.append('pb_noun_adj')
                                
                            elif child_infos[0] == 'prep' and token_info[1] == 'VERB': 
                                types.append('pb_verb_prep')     
                            
                            elif 'aux' in child_infos[0]: 
                                types.append('pb_verb_chain')

                            elif child_infos[0] == 'nmod' or child_infos[0] == 'prep' and token_info[1] == 'NOUN': 
                                types.append('pb_noun_prep')

                            elif 'adv' in child_infos[0]:
                                if token_info[2] == 'VBN' or 'JJ' in token_info[2]: 
                                    types.append('pb_adj_adv')
                                
                                elif token_info[1] == 'VERB': 
                                    types.append('pb_verb_adv')

                        if child_index > enjambment_index  and token_index < enjambment_index  \
                            or child_index < enjambment_index and token_index > enjambment_index:

                            if child_infos[0] in ['dobj', 'agent']: 
                                types.append('ex_dobj_verb')
                            
                            elif 'nsubj' in child_infos[0]: 
                                types.append('ex_subj_verb')

                            elif child_infos[0] == 'prt':
                                types.append('pb_phrasal_verb')

                            elif child_infos[0] == 'relcl' and 'NN' in token_info[2]:
                                types.append('cc_cross_clause')

                            elif child_infos[0] in ['xcomp'] and token_info[2] in ['JJ', 'VBN', 'JJR', 'JJS']: 
                                types.append('pb_adj_prep')
                                    
                        elif child_index == enjambment_index - 1 and token_index < child_index:
                            if child_infos[0] == 'prep' and token_info[0] == 'pobj' \
                                or child_infos[0] == 'prep' and token_info[1] in  ['NOUN', 'PRON'] \
                                or child_infos[0] == 'cc': 
                                types.append('pb_relword')

                        if token_index > enjambment_index:
                            if child_index > token_index and token_index - child_index <= 3: 
                                if child_infos[0] in ['conj', 'prep', 'mark'] and child_infos[2] == 'IN':
                                    if child.lower() in ['although', 'while', 'from', 'though', 'after', 'before','because'] :
                                        types.append('ex_verb_adjunct')
 
                    except KeyError as err: 
                        continue

        
    return types


def detect_phrasal_verb(line_pair): 
    types =  []
    with open('JaDe/resources/phrasal_verbs.txt', 'r', encoding='utf-8') as file: 
        phrasal_verbs = file.readlines()


    for phrasal in phrasal_verbs: 
        phrasal = phrasal.strip()
        object_pattern = r'some\w*'

        split_phrasal = phrasal.split(' ')
        ing_verb = split_phrasal[0] + '(.?ing|d)? '
        phrasal = ing_verb + ' '.join(split_phrasal[1:])
        
        if re.search(object_pattern, phrasal): 
            ex_verb_pattern_1 = split_phrasal[0] + r'(.?ing|d|t)( \\w*){0,3}' + re.sub(object_pattern, r'\\t( ?\\w*){0,3}', 
                                                                                    ' '.join(split_phrasal[1:]))
            ex_verb_pattern_2 = split_phrasal[0] + r'(.?ing|d|t)' + ' ' + re.sub(object_pattern, r'\\t( ?\\w*){0,3}', 
                                                                        ' '.join((split_phrasal[1:]))) 
            ex_verb_pattern_2 = ex_verb_pattern_2.replace(' \\t', '\\t')
            ex_verb_pattern_1 = ex_verb_pattern_1.replace( ' \\t', '\\t')

            if re.search(ex_verb_pattern_1, line_pair, flags=re.MULTILINE) or re.search(ex_verb_pattern_2, line_pair, 
                                                                                        flags=re.MULTILINE):
                types.append('ex_dobj_pverb')
            
        else: 
            pb_phrasal = ing_verb + '\\t' + ' '.join(split_phrasal[1:])
            pb_phrasal = pb_phrasal.replace(' \\t', '\\t')

            if re.search(pb_phrasal, line_pair, flags=re.MULTILINE): 
                types.append('pb_phrasal_verb')

    return types