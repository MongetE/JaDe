import json
import os
import pathlib
import re
from fuzzywuzzy import fuzz
import spacy
from utils import get_type


DATA_DIR = pathlib.Path('JaDe/resources/annotated_poems')
OUT_DIR = pathlib.Path('JaDe/resources/detected')
nlp = spacy.load('en_core_web_sm')

def get_poem_lines(poem):
    return poem.split('\n')

def is_enjambement(line):
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

def get_enjambement_sentence(enjambement_line, poem_sentences):
    for sentence in poem_sentences:
        if '(' in enjambement_line or ')' in enjambement_line:
            enjambement_line = re.sub(r'[\(\)]', '', enjambement_line)
            sentence = re.sub(r'[\(\)]', '', enjambement_line)
        if re.search(enjambement_line, sentence):
            return sentence


def fuzzy_enjambment_matching(enjambement_line, poem_sentences): 
    for sentence in poem_sentences:
        ratio = fuzz.token_set_ratio(enjambement_line, sentence)
        if ratio > 75:
            return sentence


def remove_annotations(poem):
    lines = re.findall(r'(^\d{1,}\. )(.*)', poem, flags=re.MULTILINE)
    text = ""
    for line in lines:
        text += line[1] + '\n'

    return text

def main():
    if not os.path.exists(OUT_DIR): 
        os.makedirs(OUT_DIR)

    for file in DATA_DIR.iterdir():
        with open(str(file), 'r', encoding='utf-8') as curfile:
            filename = str(file)[31:].replace(',', '').replace('\'', '').replace(' ', '_')\
                .replace(':', '').replace('?', '').lower()
            print(filename)

            poem = curfile.read()
            poem = remove_annotations(poem)
            
            preprocessed_poem = nlp(poem)
            poem_lines = get_poem_lines(poem)
            poem_sentences = [str(sent) for sent in preprocessed_poem.sents]
            transformed_lines = []

            for line in poem_lines:
                if is_enjambement(line):
                    sentence = get_enjambement_sentence(line, poem_sentences)
                    if sentence is None: 
                        sentence = fuzzy_enjambment_matching(line, poem_sentences)
                    
                    if sentence is not None:
                        tagged_sentence = nlp(sentence)
                        sentence_part_of_speech = [(token, str(token.pos_), str(token.tag_)) 
                                                    for token in tagged_sentence]

                        # print([(token, str(token.pos_)) for token in tagged_sentence])
                        types = get_type(sentence_part_of_speech)

                        line += ' [' + str(' ,'.join(types)) + ']'

                transformed_lines.append(line)
                
            # Merge lines together back so that we have something readable
            poem = '\n'.join(transformed_lines)
            out_file = str(OUT_DIR) + '/' + filename

            with open(out_file, 'w', encoding='utf-8') as file:
                file.write(poem)

if __name__ == '__main__':
    main()