import json
import os
import pathlib
import re
import spacy


DIR = pathlib.Path('./data/annotated_poems')
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


def reconstruct_poem(marked_poem):
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
    poem += re.sub(r'(&&|%%|\n)', ' ', marked_poem[0])

    for line in marked_poem[1:]:
        line = line.lower()
        if '%%' in line:
            last_words_enj.append(re.search(r'\w*(?=%%)', line).group(0))
            poem += re.sub(r'(%%|\n)', ' ', line)
        elif '&&' in line:
            last_words_end.append(re.search(r'\w*(?=&&)', line).group(0))
            poem += re.sub(r'(&&|\n)', ' ', line)

    return poem, last_words_enj, last_words_end


def get_before_after(sentences, last_words_enj, tokens_in_sent, pos_in_sent, tags_in_sent):
    """
        Split the sentence between what's before the enjambment and what's after.

        Parameters
        ----------
        sentences: list
            A list of the poem sentences.
        last_words_enj: list
            A list of the last words before an enjambment
        tokens_in_sent: list
            A list of all the tokens in the poem
        pos_in_sent: list
            A list of all the tokens POS in the poem
        tags_in_sent: list
            A list of all the tokens tags in the poem

        Returns
        -------
            enjs: dict
                A dictionary. Keys include:
                * the tokens before the enjambment
                * the tokens after the enjambment
                * the POS before the enjambment
                * the POS after the enjambment
                * the tags before the enjambment
                * the tags after the enjambment
    """
    enjs = []
    for i in range(len(sentences)):
        for word in last_words_enj:
            enj = {}
            if word != '' and word in tokens_in_sent[i]:
                enj_position = tokens_in_sent[i].index(word)
                enj['tok_before'] = tokens_in_sent[i][:enj_position + 1]
                enj['pos_before'] = pos_in_sent[i][:enj_position + 1]
                enj['tok_after'] = tokens_in_sent[i][enj_position + 1:]
                enj['pos_after'] = pos_in_sent[i][enj_position + 1:]
                enj['tags_before'] = tags_in_sent[i][enj_position + 1:]
                enj['tags_after'] = tags_in_sent[i][enj_position + 1:]
            enjs.append(enj)

    return enjs


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

    """
    json_dict = []

    textsPairs = re.findall(r'(^\d{1,}\.)(.*)', content, flags=re.MULTILINE)
    pairs = [enj_marker(textsPairs[i][1].lstrip()) + textsPairs[i + 1][1] for i in range(len(textsPairs))
             if textsPairs[i] != textsPairs[-1]]

    poem = "\n".join([enj_marker(textsPairs[i][1].strip()) for i in range(len(textsPairs))])

    annotPairs = re.findall(r'(\d{2,} \d{2,})(.*)', content, flags=re.MULTILINE)
    tmp = [(match[0], match[1]) for match in annotPairs]

    json_dict = []
    for i in range(len(tmp)):
        tmp_dict = dict()

        tmp_dict['nbPair'], tmp_dict['annot'] = tmp[i][0], tmp[i][1]
        tmp_dict['text'], tmp_dict['marked_text'] = re.sub('(%%|&&)', '', pairs[i]), pairs[i]

        if '%%' in pairs[i]:
            tmp_dict['isEnj'] = True
        else:
            tmp_dict['isEnj'] = False

        json_dict.append(tmp_dict)

    raw, last_words_enj, last_words_end = reconstruct_poem(poem)
    sentences, tokens_in_sent, pos_in_sent, tags_in_sent = get_sentences(raw)
    enjs_dict = get_before_after(sentences, last_words_enj, tokens_in_sent, pos_in_sent, tags_in_sent)

    return json_dict, enjs_dict


def main():
    for file in DIR.iterdir():
        with open(str(file), 'r', encoding='utf-8') as curfile:
            filename = str(file)[21:-4].replace(',', '').replace('\'', '').replace('.', '').replace(' ', '_')\
                .replace(':', '').replace('?', '').lower()
            content = curfile.read()

            json_dict, enjs_dict = build_dict(content)

            with open(str(file).replace('txt', 'json').replace(str(DIR), './data/tokenized_enj_pairs'), 'w', encoding='utf-8') as file:
                json.dump(enjs_dict, file)

if __name__ == '__main__':
    main()