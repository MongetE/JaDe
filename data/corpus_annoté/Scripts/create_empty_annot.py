import glob
import os
import pathlib

def create_annotation(input_file):
    with open(input_file, "r+", encoding="utf-8") as file:
        poem = file.readlines()
        file.write('\n\n')
        i = 0
        for line in poem[:-1]:    
            if line != '\n':
                i +=1

            if line == '\n':
                to_write = '\n'
            elif i == 9:
                to_write = f"0{i} {i+1} [] [] []\n"
            elif i < 10:
                to_write = f"0{i} 0{i+1} [] [] []\n"
            else:
                to_write = f"{i} {i+1} [] [] []\n"
            file.write(to_write)
        
if __name__ == "__main__":
    dirpath = pathlib.Path(os.getcwd())
    for file in dirpath.glob("*.txt"):
        create_annotation(file)