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
            # enj_checker(content)


def enj_checker(content):
    for line in content:
        if len(line) > 0:
            if re.search(r'[\.,\!\?;-]$', line):
                continue
            else:
                line += '%%'
                print(line)


def cleaner(content, filename):
    poem = []
    annotations = []

    for line in content:
        line_pair = {}
        if re.search(r'^\d{1,}\. ', line) or line == '\n':
            line = re.sub(r'\d{1,}\. ', '', line)
            poem.append(line)
        elif re.search(r'(\d{,3} ){2}', line):
            line_pair['linePair'] = re.search(r'(\d{,3} ){2}', line).group(0)
            line_pair['texte'] = re.search(r'(?<!(\d{2}){2})\[.*', line).group(0)
            annotations.append(line_pair)

    annot_dir = 'data/annotations'
    if not pathlib.Path(annot_dir).exists():
        os.makedirs('data/annotations')

    json_path = annot_dir + '/' + filename + '.json'
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        # jsonfile.writelines(annotations)
        json.dump(annotations, jsonfile)


if __name__ == '__main__':
    reader()
