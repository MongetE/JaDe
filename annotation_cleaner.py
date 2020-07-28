import os
import pathlib
import re 


if __name__ == "__main__":
    annot_dir = "JaDe/resources/annotated_poems"

    adjunct = r'ex_(verb|a[dj]*unct)_\w*'
    noun_verb = 'pb_noun_adv'
    verb_adj = 'pb_verb_adj'

    for poem_file in pathlib.Path(annot_dir).iterdir(): 
        with open(str(poem_file), 'r+', encoding='utf-8') as file: 
            current = file.readlines()
            file.seek(0)

            for line in current: 
                

                if re.search(adjunct, line): 
                    new_line = re.sub(adjunct, 'ex_verb_adjunct', line)
                    file.write(new_line)

                elif re.search(noun_verb, line): 
                    new_line = re.sub(noun_verb, '', line)
                    file.write(new_line)

                elif re.search(verb_adj, line): 
                    new_line = re.sub(verb_adj, '', line)
                    file.write(new_line)

                else:
                    file.write(line)
                

            file.truncate()

