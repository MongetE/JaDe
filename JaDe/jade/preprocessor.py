import json
import os
import pathlib
import sys
import re
from fuzzywuzzy import fuzz
import spacy
from .utils import get_pos_type, get_dep_type, detect_phrasal_verb


def get_poem_lines(poem):
    return poem.split('\n')

def is_enjambment(line):
    """
        Take a line and return whether it is end-stopped or enjambed.
        
        Parameters
        ----------
        line: str
            A line from a given poem

        Returns
        -------
        bool
    """

    if re.search(r'[\.,\!\?;\-:]$', line):
        return False

    return True

def get_enjambment_sentence(enjambment_line, poem_sentences):
    """
        Try to match a line to the sentence where it occurs. 

        Parameters
        ----------
            enjambment_line: str
                An enjambed line according to is_enjambment
            sentences: list
                The list of the poem sentences
        Returns
        -------
            sentence: str
                The sentence in which occurs the enjambment
    """
    for sentence in poem_sentences:
        if '(' in enjambment_line or ')' in enjambment_line:
            enjambment_line = re.sub(r'[\(\)]', '', enjambment_line)
            sentence = re.sub(r'[\(\)]', '', enjambment_line)
        elif '*' in enjambment_line: 
            enjambment_line = re.sub(r'\*', '°', enjambment_line)
        if re.search(enjambment_line, sentence, flags=re.MULTILINE):
            return sentence


def fuzzy_enjambment_matching(enjambment_line, poem_sentences): 
    """
        If match by regex fails, try to establish whether or not
        a given line is present in the sentence. 

        Fuzzy matching is done using the set_token_ration method,
        so that the length of the string doest not really matter. 

        Parameters
        ----------
            enjambment_line: str
                An enjambed line according to is_enjambment
            sentences: list
                The list of the poem sentences
        Returns
        -------
            sentence: str
                The sentence in which occurs the enjambment
    """
    for sentence in poem_sentences:
        ratio = fuzz.token_set_ratio(enjambment_line, sentence)
        if ratio > 75:
            return sentence


def remove_annotations(poem):
    """
        Get poem from annotated poem.

        Parameters
        ----------
            poem: str
                An annotated poem 

        Returns
        -------
            text: str
                The text of the poem
    """
    lines = re.findall(r'(^\d{1,}\. )(.*)', poem, flags=re.MULTILINE)
    text = ""
    for line in lines:
        text += line[1] + '\n'

    return text

def preprocessor(file, save, outfile, nlp):
    """
        Execute the whole preprocessing module. 

        Split the poem into lines, then check whether a line end-stopped. 
        If not, checks if the line is contained into a given sentence, then the 
        sentence is tagged and regex are ran against  spacy POS and tags. 

        If there is a match (or several), an annotation is added to the end of the line. 
        If no match was found and the line is not end-stopped, [?] is added to the line. 

        Finally, the poem is reconstructed, unfortunately removing the blanks between stanzas 
        (at least for now).

        Parameters
        ----------
            file: TextIOWrapper
                poem file to process
            save: bool
                whether the file is to be printed to cmd or save to disk
            outfile: str
                path to where the result will be saved
            nlp: 
                spacy nlp pipeline
    """
    # filename = str(file)[31:]

    poem = file.read()

    if re.findall(r'(^\d{1,}\. )(.*)', poem, flags=re.MULTILINE):
        poem = remove_annotations(poem)
    
    preprocessed_poem = nlp(poem)
    poem_lines = get_poem_lines(poem)
    if not poem_lines[-1] == '\n':
        poem_lines.append('\n')
        
    # poem_sentences = [str(sent) for sent in preprocessed_poem.sents]
        transformed_lines = []

    for i in range(len(poem_lines)+1):
        if i < len(poem_lines)-1: 
            line = poem_lines[i].strip()
            if len(line) > 1:
                if is_enjambment(line):
                    if poem_lines[i+1] != '':
                        line_pair = poem_lines[i] + '\n' + poem_lines[i+1]
                    else:
                        line_pair = poem_lines[i] + '\n' + poem_lines[i+2]
                    
                    line_break = line_pair.index('\n')
                    last_word_before_enjambment = line_break - 1
                    line_pair = line_pair.replace('\n', '\t')
                    phrasal = detect_phrasal_verb(line_pair)


                    # better results were obtained with only the line-pair part of the sentence
                    # so it is used instead of the whole sentence
                    tagged_sentence = nlp(line_pair.lower())
                    sentence_part_of_speech = [(token, str(token.pos_), str(token.tag_)) for token in tagged_sentence]
                    dependency_dict = {token.text : (str(token.dep_), str(token.pos_), str(token.tag_), token.head.text,
                                                    token.head.pos_, [str(child) for child in token.children]) 
                                        for token in tagged_sentence}
                    pos_types = get_pos_type(sentence_part_of_speech)
                    dep_types = list(set(get_dep_type(dependency_dict)))

                    if len(dep_types) > 1:
                        if 'ex_dobj_verb' in dep_types and 'ex_subj_verb' in dep_types:
                            del dep_types[dep_types.index('ex_subj_verb')]
                            if len(dep_types) > 1:
                                del dep_types[dep_types.index('ex_dobj_verb')]
                        
                        elif 'ex_dobj_verb' in dep_types and 'ex_verb_adjunct' in dep_types \
                            or 'ex_subj_verb' in dep_types and 'ex_verb_adjunct' in dep_types:
                            del dep_types[dep_types.index('ex_verb_adjunct')]

                        if 'ex_dobj_verb' in dep_types: 
                            del dep_types[dep_types.index('ex_dobj_verb')]

                        if 'ex_subj_verb' in dep_types:
                            del dep_types[dep_types.index('ex_subj_verb')]

                        if 'ex_verb_adjunct' in dep_types:
                            del dep_types[dep_types.index('ex_verb_adjunct')]
                        
                        if 'pb_relword' in dep_types:
                            del dep_types[dep_types.index('pb_relword')]

                        else:
                            for i in range(len(dep_types)): 
                                if i < len(dep_types) - 1:
                                    if dep_types[i] == dep_types[i+1]: 
                                        del(dep_types[i])
                    
                        
                    # TODO: choose between pos and dep tag if both are > 0 ?
                    if len(phrasal) > 0:
                        line += ' [' + str(', '.join(phrasal)) + ']'
                    elif len(pos_types) > 0 and len(dep_types) == 0:
                        line += ' [' + str(','.join(pos_types)) + ']'
                    elif len(dep_types) > 0 and len(pos_types) == 0: 
                        line += ' [' + str(', '.join(dep_types)) + ']'
                    elif len(dep_types) > 0 and len(pos_types) > 0:
                        line += ' [' + str(', '.join(pos_types)) + ']'
                    
                    # else: 
                    #     line += ' [?]'
            
            transformed_lines.append(line)

            
    # # Merge lines together back so that we have something readable
    poem = '\n'.join(transformed_lines)

    if save:
        with open(outfile, 'w', encoding='utf-8') as file:
            file.write(poem)
        
    else: 
        print(poem)
