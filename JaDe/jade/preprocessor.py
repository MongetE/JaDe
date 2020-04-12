import json
import os
import pathlib
import re
import spacy


DIR = pathlib.Path('data/annotated_poems')
nlp = spacy.load('en_core_web_sm')


def enj_marker(line):
    """
        Take a line and return whether it is end-stopped or enjambed.
        
        Parameters
        ----------
        line: str
            A line from a given poem

        Returns
        -------
        str
            The same line marked with:
             * && if the line was end-stopped
             * %% if the line was enjambed

    """
    marked = ""
    if re.search(r'[\.,\!\?;\-:]$', line) or line == "\n":
        marked += line + '&&'
    else:
        marked += line + '%%'

    return marked


def build_dict(content):
    """
        Build a json object.

        Ideally, this dictionary should also contains the sentence(s) found
        within the line pair and only the section(s) of these sentence(s)
        corresponding to the line pair.

        Parameters
        ----------
            content: str
                An annotated poem

        Returns
        -------
            json_dict: dict
                A list of dictionaries in which the following keys are found:
                * nbPair is the id of the line pair
                * text is the marked version of the line pair
                * annot are the annotations given for the line pair
                * isEnj is a bool, False if there is no enjambment, True otherwise

            poem: str
                May be removed.
                The poem with a mark at the end of each line, indicating
                whether the line is end-stopped (&&) or enjambed (%%).
    """
    json_dict = []

    textsPairs = re.findall(r'(^\d{1,}\.)(.*)', content, flags=re.MULTILINE)
    pairs = [enj_marker(textsPairs[i][1].lstrip()) + textsPairs[i+1][1] for i in range(len(textsPairs))
             if textsPairs[i] != textsPairs[-1]]

    poem = [enj_marker(textsPairs[i][1].strip())+'\n' for i in range(len(textsPairs))]

    annotPairs = re.findall(r'(\d{2,} \d{2,})(.*)', content, flags=re.MULTILINE)
    tmp = [(match[0], match[1]) for match in annotPairs]

    for i in range(len(tmp)):
        tmp_dict = dict()

        tmp_dict['nbPair'], tmp_dict['annot'] = tmp[i][0], tmp[i][1]
        tmp_dict['text'], tmp_dict['marked_text'] = re.sub('(%%|&&)', '', pairs[i]), pairs[i]

        if '%%' in pairs[i]:
            tmp_dict['isEnj'] = True
        else:
            tmp_dict['isEnj'] = False

        json_dict.append(tmp_dict)

    return json_dict, poem


def get_sentences(poem):
    # TODO: change list comprehensions by for loop to avoid looping three times on the same list
    """
        Take a poem and destructure it into sentences.

        Paramaters
        ----------
            poem: str

        Returns
        -------
            list
             Three lists corresponding to the sentences, the tokens in
             the sentences and the POS in the sentences.
    """
    doc = nlp(poem)
    sp_sentences = [str(sent) for sent in doc.sents]
    tokens_in_sent = [[str(token) for token in nlp(sentence)] for sentence in sp_sentences]
    pos_in_sent = [[str(token.pos_) for token in nlp(sentence)] for sentence in sp_sentences]
    tags_in_sent = [[str(token.tag_) for token in nlp(sentence)] for sentence in sp_sentences]

    return sp_sentences, tokens_in_sent, pos_in_sent, tags_in_sent


def reconstruct_poem(json_dict):
    """
        Reconstruct the poem from the json representation of that poem.

        Parameters
        ----------
        json_dict: dict
            A json object representing a poem.

        Returns
        -------
            str
                The poem
            list
                Two lists: one containing the last word of enjambed lines
                and the other, the last word of end-stopped lines.
    """
    poem = ""
    last_words_enj = []
    last_words_end = []
    for item in json_dict:
        line_pair = item.get('marked_text')
        if item == json_dict[0]:
            poem += line_pair.lower().split('%%')[0] + line_pair.lower().split('%%')[1]
            last_words_enj.append(re.search(r'\w*(?=%%)', line_pair).group(0))
        elif '&&' in line_pair:
            poem += line_pair.lower().split('&&')[0] + line_pair.lower().split('&&')[1]
            last_words_end.append(re.search(r'\w*(?=\W&&)', line_pair).group(0))
        else:
            if "&&" in line_pair:
                poem += line_pair.lower().split('&&')[1]
                last_words_end.append(re.search(r'\w*(?=\W&&)', line_pair).group(0))
            else:
                poem += line_pair.lower().split('%%')[1]
                last_words_enj.append(re.search(r'\w*(?=%%)', line_pair).group(0))

        return poem, last_words_enj, last_words_end


def main():
    for file in DIR.iterdir():
        with open(str(file), 'r', encoding='utf-8') as curfile:
            filename = str(file)[21:-4].replace(',', '').replace('\'', '').replace('.', '').replace(' ', '_')\
                .replace(':', '').replace('?', '').lower()
            content = curfile.read()
            json_dict, poem = build_dict(content)
            print(json_dict)
            reconstructed, last_words_enj, last_words_end = reconstruct_poem(json_dict)
            sentences, tokens_in_sent, pos_in_sent, tags_in_sent = get_sentences(reconstructed)
            # writer(json_dict, filename, poem)


if __name__ == '__main__':
    main()