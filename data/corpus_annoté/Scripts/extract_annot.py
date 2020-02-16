import sys
import pathlib
import os 
import re
import csv

DIR_R = pathlib.Path(sys.argv[1])
DIR_M = pathlib.Path(sys.argv[2])
DIR_TO_SAVE_R = pathlib.Path(sys.argv[3])
DIR_TO_SAVE_M = pathlib.Path(sys.argv[4])
REGEX = re.compile(r'\d{1,2}-\d{1,2} \[.*?\] \[.*?\] \[.*?\]')

def get_R_annots(filename):
    with open(os.path.join(DIR_R, filename), 'r', encoding='utf-8') as file:
        annotations_R = []
        for line in file:
            if '#' in line: 
                index = line.index('#')
                line = line[:index]

            line = line.replace(' ', '-', 1)

            if REGEX.match(line):
                annotations_R.append(line.split())
    return annotations_R

def get_M_annots(filename):
    with open(os.path.join(DIR_M, filename), 'r', encoding='utf-8') as file:
        annotations_M = []
        for line in file:
            if '#' in line: 
                index = line.index('#')
                line = line[:index]

            line = line.replace(' ', '-', 1)

            if REGEX.match(line):
                annotations_M.append(line.split())

    return annotations_M

def write_csv(current_file, dir_save, annotations):
    with open(os.path.join(dir_save,current_file+'.csv'), 'w', newline='') as csvfile:
        fieldnames = ['Lines', 'Syntactic_type', 'Style_type', 'Meaning_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(annotations)):
            writer.writerow({'Lines' : annotations[i][0], 'Syntactic_type' : annotations[i][1],
                                'Style_type' : annotations[i][2],
                                'Meaning_type' : annotations[i][3]})

if __name__ == "__main__":
    files_R = [filename for filename in DIR_R.glob('*.txt')]
    files_M = [filename for filename in DIR_M.glob('*.txt')]
    #filenames = [str(filename) for filename in os.listdir(DIR_M)]
   
    # annotations_R = [get_R_annots(filename) for filename in files_R]
    # annotations_M = [get_M_annots(filename) for filename in files_M]

    for filename in os.listdir(DIR_M):
        annotations_M = get_M_annots(filename)
        write_csv(str(filename), DIR_TO_SAVE_M, annotations_M)

    for filename in os.listdir(DIR_R):
        annotations_R = get_R_annots(filename)
        write_csv(str(filename), DIR_TO_SAVE_R, annotations_R)
    
    