import re
import pathlib
import os

MAIN_DIR = pathlib.Path("/home/rhodri/Documents/memoire/corpus/raw_corpus/per_author")
SCRIPTS = pathlib.Path("/home/rhodri/Documents/memoire/corpus/Scripts")

def clean_poem(file):
    # Remove line numbers at the end of a line and unwanted chracters 
    current_file = str(file)
    
    with open(file, 'r+', encoding='utf-8') as file:
        poem = file.readlines()
        file.seek(0)

        for line in poem:

            if re.search(r' *\d{2,3}$', line):
                new_line = re.sub(r' *\d{2,3}$', '', line)
                file.write(new_line)

            elif re.search(r'&amp;', line):
                new_line = re.sub(r'&amp;', '&', line)
                file.write(new_line)

            elif re.search(r'&amp;c', line):
                new_line = re.sub(r'&amp;c', '&c', line)
                file.write(new_line)

            elif re.search(r'(&lt;).*?&gt;|&[gl]t;', line):
                new_line = re.sub(r'(&lt;).*?&gt;|&[lg]t;', '', line)
                file.write(new_line)
                
            elif re.search(r'&.*;.', line):
                new_line = re.sub(r'&.*;', '', line)
                file.write(new_line)

            elif re.search(r'&qu.*;', line):
                new_line = re.sub(r'&qu.*;', '"', line)
                file.write(new_line)

            elif re.search(r'&md.*;', line):
                new_line = re.sub(r'&md.*;', '―', line)
                file.write(new_line)

            elif re.search(r'Submitted.*', line):
                new_line = re.sub(r'Submitted.*', '', line)
                file.write(new_line)

            else:
                file.write(line)

            # get an overview of encoding problems 
            if re.search(r'[ÑÃ]|(&.*;)', line):
                with open(os.path.join(SCRIPTS, 'special_char.txt'), 'a', encoding='utf-8') as data:
                    to_write = f'{line.strip()}\t{current_file}\t{cwd[55:]}\n'
                    data.write(to_write)

        file.truncate()

                
def open_files(cwd):
    for file in os.listdir(cwd):
        clean_poem(file)


if __name__ == "__main__":
    for author_dir in os.listdir(MAIN_DIR):
        to_open = str(MAIN_DIR)+'/'+author_dir
        os.chdir(to_open)
        cwd = os.getcwd()
        open_files(cwd)
        os.chdir(MAIN_DIR)
    