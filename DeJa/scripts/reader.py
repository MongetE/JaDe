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
            content = curfile.read()
            json_dict = cleaner(content)
            writer(json_dict, filename)


def enj_marker(content):
    marked = ""
    if re.search(r'[\.,\!\?;\-:]$', content) or content == "\n":
        marked += content + ''
    else:
        marked += content + '%%'

    return marked


def cleaner(content):
    """
    :param content: str, numbered + annotated poem
    :return: a dict organized according to line pairs. Keys include the lines, the annotations and whether it is an
            an enjambment or not
    """
    json_dict = []

    textsPairs = re.findall(r'(^\d{1,}\.)(.*)', content, flags=re.MULTILINE)
    pairs = [enj_marker(textsPairs[i][1].lstrip()) + textsPairs[i+1][1] for i in range(len(textsPairs))
             if textsPairs[i] != textsPairs[-1]]

    # poem = [textsPairs[i][1].strip() for i in range(len(textsPairs))]

    annotPairs = re.findall(r'(\d{2,} \d{2,})(.*)', content, flags=re.MULTILINE)
    tmp = [(match[0], match[1]) for match in annotPairs]

    for i in range(len(tmp)):
        tmp_dict = dict()

        tmp_dict['nbPair'], tmp_dict['text'], tmp_dict['annot'] = tmp[i][0], pairs[i], tmp[i][1]

        if '%%' in pairs[i]:
            tmp_dict['isEnj'] = True
        else:
            tmp_dict['isEnj'] = False

        json_dict.append(tmp_dict)

    return json_dict


def writer(json_dict, filename):
    annot_dir = 'data/annotations'
    if not pathlib.Path(annot_dir).exists():
        os.makedirs('data/annotations')

    json_path = annot_dir + '/' + filename + '.json'
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_dict, jsonfile)


if __name__ == '__main__':
    reader()
