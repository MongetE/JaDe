"""
   JaDe is a command-line tool to automatically detect enjambment in English 
   poetry. This file contains the rules used to classify enjambment. Details on
   the annotations' meaning can be found : <https://zenodo.org/record/3992703>.  

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

import re


def get_pos_type(sentence):
    """
        Retrieve the type of enjambment present in a sentence based on regex 
        patterns. 

        In general, these patterns only look at the last word before the break 
        and the first word after the break. This behavior is based on the 
        assumption that most of enjambment occurrences can be captured with such
        a configuration and that these occurrences tend to be stronger that way.
        This can be easily changed by adding {0,x} after the desired POS, where
        x is the number of POS that can be inserted between the two explicitly
        expressed in the regular exession. 
        Furthermore, when allowing for broader range in regular expression search, 
        you might want to change if/elif to if/if. Doing so will allow 
        multi-classification, which is bound to happen at some point when making
        the patterns more flexible. 

        Parameters
        ----------
            sentence: list
                list of tokens, spacy's pos and spacy's tags

        Returns
        ------- 
            types: list
                list of detected types

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

    return types


def get_dep_type(tokendict):
    """
        Retrieve the type of enjambment present in a sentence based on a 
        combination of dependency relationships and POS.

        Most rules are concerned only with the last word before the break 
        and the first one afterward, based on the assumption that most of
        enjambment occurrences can be captured with such a configuration. This
        can be changed by adjusting the first if in the try clause: instead of 
        enjambment +/- 1, change 1 to the desired scale. Be aware that doing so
        will cause multiclassification. 

        Parameters
        ----------
            tokendict: dict
                {token: [dep, pos, tag, token_head_text, token_head_pos, 
                token_children]}
        Returns
        -------
            types: list
                list of detected types
    """
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
                            if child_index > token_index and token_index - child_index < 3: 
                                if child_infos[0] in ['conj', 'prep', 'mark'] and child_infos[2] == 'IN':
                                    if child.lower() in ['although', 'while', 'from', 'though', 'after', 'before','because', 'as', 'to'] :
                                        types.append('ex_verb_adjunct')
 
                    except KeyError as err: 
                        continue

        
    return types


def detect_phrasal_verb(line_pair): 
    """
        Retrieve the type of enjambment present in a sentence based on a list
        of phrasal verbs. 

        Parameters
        ----------
            line_pair: str
                line pair as found in the poem 
        Returns
        -------
            types: list
                detected types
    """
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
            ex_verb_pattern_1 = split_phrasal[0] + r'(.?ing|e?d|t)( \\w*){1,3}' + re.sub(object_pattern, r'\\t( ?\\w*){1,3}', 
                                                                                    ' '.join(split_phrasal[1:]))
            ex_verb_pattern_2 = split_phrasal[0] + r'(.?ing|e?d|t)' + ' ' + re.sub(object_pattern, r'\\t( ?\\w*){1,3}', 
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