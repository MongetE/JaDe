import os
import pathlib
import spacy

DIRPATH = '/home/rhodri/Documents/memoire/corpus/annotated_corpus'
MAIN_DIR = '/home/rhodri/Documents/memoire/corpus/raw_corpus/per_author'

def annotate(file, author_dir):
    nlp = spacy.load('en_core_web_sm')
    current_file = str(file)
    print(current_file)
    with open(file, 'r', encoding='utf-8') as file:
        poem = file.read()
        annotated_poem = nlp(poem)

    # with open(os.path.join(DIRPATH, author_dir, current_file + '.csv'), 'w', encoding='utf-8') as data:
    #     header = f'TOKEN,POS,DEP\n'
    #     data.write(header)
    #     for token in annotated_poem:
    #         line = f'{token.text},{token.pos_},{token.dep_}\n'
    #         data.write(line)
             

def open_files(cwd, author_dir):
    for file in os.listdir(cwd):
        annotate(file, author_dir)

if __name__ == "__main__":
    if not os.path.exists(DIRPATH):
        os.mkdir(DIRPATH)

    for author_dir in os.listdir(MAIN_DIR):
        if not os.path.exists(DIRPATH+'/'+author_dir):
            os.mkdir(DIRPATH+'/'+author_dir)
            
        to_open = str(MAIN_DIR)+'/'+author_dir
        os.chdir(to_open)
        cwd = os.getcwd()
        open_files(cwd, author_dir)
        os.chdir(MAIN_DIR)
        
    