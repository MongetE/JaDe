import os
import pathlib

DIRPATH = '/home/rhodri/Documents/memoire/corpus/preprocess_corpus'
MAIN_DIR = '/home/rhodri/Documents/memoire/corpus/raw_corpus/per_author'


def number_lines(file, author_dir):
    current_file = str(file)
    
    with open(file, 'r', encoding='utf-8') as file:
        poem = file.readlines()

        numbered_poem = []
        line_nb = 1
        for i in range(len(poem)):
            if poem[i].isspace():
                new_line = '\n'
            else:
                new_line = str(line_nb)+'. '+poem[i]
                line_nb += 1
            numbered_poem.append(new_line)


  
    with open(os.path.join(DIRPATH, author_dir, current_file), 'w', encoding='utf-8') as new_file:
        for line in numbered_poem:
            new_file.write(line)
             
def open_files(cwd, author_dir):
    for file in os.listdir(cwd):
        number_lines(file, author_dir)

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