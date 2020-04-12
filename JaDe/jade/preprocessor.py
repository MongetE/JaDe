import json
import os
import pathlib
import re


DIR = pathlib.Path('data/annotated_poems')


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

    poem = [enj_marker(textsPairs[i][1].strip())+'\n' for i in range(len(textsPairs))]

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

    return json_dict, poem
