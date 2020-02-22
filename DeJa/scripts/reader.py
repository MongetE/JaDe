import json
import os
import pathlib
import re

DIR = pathlib.Path('data/annotated_poems')


def reader():
    for file in DIR.iterdir():
        with open(str(file), 'r', encoding='utf-8') as curfile:
            filename = str(file)[21:-4].replace(',', '').replace('\'', '').replace('.', '').replace(' ', '_')\
                .replace(':', '').replace('?', '').lower()
            content = curfile.readlines()
            cleaned = cleaner(content, filename)
            enj_checker(cleaned)


def enj_checker(content):
    checked = ""
    for line in content:
        if len(line) > 0:
            if re.search(r'[\.,\!\?;-]$', line) or line == "\n":
                checked += line + ''
            else:
                checked += line + '%%'
    print(checked)


def cleaner(content, filename):
    poem = []
    annotations = []

    for line in content:
        line_pair = {}
        if re.search(r'(?<=\n)\n\d{2,}|\n\d{2,}', line):
            continue
        elif re.search(r'^\d{1,}\. ', line):
            line = re.sub(r'\d{1,}\. ', '', line)
            poem.append(line.strip())
        elif line == "\n":
            poem.append(line)
        elif re.search(r'(\d{,3} ){2}', line):
            line_pair['linePair'] = re.search(r'(\d{,3} ){2}', line).group(0)
            line_pair['texte'] = re.search(r'(?<!(\d{2}){2})\[.*', line).group(0)
            annotations.append(line_pair)

    annot_dir = 'data/annotations'
    if not pathlib.Path(annot_dir).exists():
        os.makedirs('data/annotations')

    json_path = annot_dir + '/' + filename + '.json'
    if not pathlib.Path(json_path).exists():
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(annotations, jsonfile)

    while poem[-1] == "\n":
        del poem[-1]

    return poem


if __name__ == '__main__':
    reader()
