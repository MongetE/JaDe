import json


def load_dict(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        dict_ = json.load(file)

    return dict


def dump_dict(filepath, dictname):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(dictname, ensure_ascii=False)