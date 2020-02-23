import json
import pathlib
import spacy

# TODO: change how load_file is executed bc iter on only one file
# TODO: mark sentence with && and %% depending on how original line ends
# TODO: create preprocess pipeline or file → need POS and dependencies

def load_file():
    dir = 'data/annotations'

    for filepath in pathlib.Path(dir).iterdir():
        with open(str(filepath), 'r', encoding='utf-8') as file:
            json_dict = json.load(file)

        return json_dict


def reconstruct_poem(json_dict):
    poem = ""
    for item in json_dict:
        if item == json_dict[0]:
            if '%%' in item.get('text'):
                poem += item.get('text').lower().split('%%')[0] + item.get('text').lower().split('%%')[1]
            elif '&&' in item.get('text'):
                poem += item.get('text').lower().split('&&')[0] + item.get('text').lower().split('&&')[1]
        else:
            if "&&" in item.get('text'):
                poem += item.get('text').lower().split('&&')[1] + ' '
            else:
                poem += item.get('text').lower().split('%%')[1] + ' '

    return poem


def get_sentences(poem):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(poem)

    for sent in doc.sents:
        print(sent)


if __name__ == '__main__':
    json_dict = load_file()
    reconstructed = reconstruct_poem(json_dict)
    get_sentences(reconstructed)
