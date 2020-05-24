import json
import os
import pathlib
import re
from fuzzywuzzy import fuzz
import spacy
from utils import get_type

nlp = spacy.load('en_core_web_lg')

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

def preprocessor(file, save, outfile):
    """
        Execute the whole preprocessing module. 

        Split the poem into lines, then check whether a line end-stopped. 
        If not, checks if the line is contained into a given sentence, then the 
        sentence is tagged and regex are ran against  spacy POS and tags. 

        If there is a match (or several), an annotation is added to the end of the line. 
        If no match was found and the line is not end-stopped, [?] is added to the line. 

        Finally, the poem is reconstructed, unfortunately removing the blanks between stanzas 
        (at least for now).
    """
    # filename = str(file)[31:]

    poem = file.read()

    if re.findall(r'(^\d{1,}\. )(.*)', poem, flags=re.MULTILINE):
        poem = remove_annotations(poem)
    
    preprocessed_poem = nlp(poem)
    poem_lines = get_poem_lines(poem)
    if not poem_lines[-1] == '\n':
        poem_lines.append('\n')
        
    poem_sentences = [str(sent) for sent in preprocessed_poem.sents]
    transformed_lines = []

    for i in range(len(poem_lines)+1):
        if i < len(poem_lines)-1: 
            line = poem_lines[i].strip()
            if len(line) > 1:
                if is_enjambment(line):
                    line_pair = poem_lines[i] + '\n' + poem_lines[i+1]
                    sentence = get_enjambment_sentence(line_pair, poem_sentences)
                    if sentence is None: 
                        sentence = fuzzy_enjambment_matching(line_pair, poem_sentences)

                    if sentence is not None:
                        tagged_sentence = nlp(line_pair)
                        sentence_part_of_speech = [(token, str(token.pos_), str(token.tag_)) 
                                                    for token in tagged_sentence]
                        # print([(token, str(token.pos_)) for token in tagged_sentence])
                        types = get_type(sentence_part_of_speech)
                        if len(types) > 0:
                            line += ' [' + str(' ,'.join(types)) + ']'
                        else: 
                            line += ' [?]'
            
            transformed_lines.append(line)

            
    # # Merge lines together back so that we have something readable
    poem = '\n'.join(transformed_lines)

    if save:
        with open(outfile, 'w', encoding='utf-8') as file:
            file.write(poem)
        
    else: 
        print(poem)