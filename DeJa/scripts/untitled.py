import json
import pathlib
import spacy # can't install it for now, pip is broken


def load_file():
    dir = 'data/annotations'

    for filepath in pathlib.Path(dir).iterdir():
        with open(str(filepath), 'r', encoding='utf-8') as file:
            json_dict = json.load(file)

        return json_dict


def reconstruct_poem(json_dict):
    poem = ""
    for item in json_dict:
        if "&&" in item.get('text'):
            poem += item.get('text').split('&&')[0] + '\n'
        elif '%%' in item:
            poem += item.get('text').split('&&')[0] + '\n'

    return poem


if __name__ == '__main__':
    json_dict = load_file()
    reconstructed = reconstruct_poem(json_dict)