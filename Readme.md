# JaDe - enJambment Detection

JaDe is a tool to detect and classify enjambment in English poetry.
The aim is to help researchers in stylistics to gather more evidence to support their claims.

## Repository Structure

1. [JaDe](https://github.com/MongetE/JaDe/tree/master/JaDe): contains code and resources necessary to run the tool
    - [jade](https://github.com/MongetE/JaDe/tree/master/JaDe/jade): source code
    - [ressources](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/): txt files
        1. [annotated_poems](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/annotated_poems): poems used for tool evaluation
        2. [detected](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/detected): poem from the test corpus annotated by the tool
2. script_corpus: contains scripts used to gather the corpus [to be added]

## Requirements

- python3.7
- spacy
- fuzzywuzzy
- click
- tqdm

Required libraries can be installed using `pip install -r requirements.txt`.

*Note*  
Spacy requires a language model. The current version of JaDe was tested with the `en_core_web_sm`, so the results
prenseted below are valid with that given model. No test was done yet with spacy bigger models.  
To install a spacy model, run `python -m spacy download "modelname"`.

## Run JaDe

JaDe can be run using `python run.py [OPT]`. A list of all options available is available through `python run.py --help`.

Basic usage include a single file analysis or the analysis of a whole directory at once.  

### Single file analysis

`python run.py --file path/to/file --save False`  
This will analyse the given file and print the result in the prompt.  
By default, the `--save` option is set to `True`, thus saving the file if the `--outfile` option is passed.
If it is not specified but the `--save` argument is default, the analysis will be saved in the current directory.

### Directory analysis

`python run.py --dir path/to/dir`  
The `--save` option MUST be set to True: for readability's sake, the analysis won't be printed in the prompt.  
By default, if `--outdir` is not specified, the analysed files will be saved in a `analysis` directory, created in the current
working directory.

## Results

As of JaDe 1.0, 11 types of enjambment are supported for classification. Out of these 11 types, 7 yield relatively
satisfactory results, using only the part-of-speech tag.

The results (curated to only show those supported) for the classification task are presented below:

|              | precision | recall | F1-score | Occurrences |
|--------------|-----------|--------|----------|-------------|
| Cross_clause | 1.00      | 0.400  | 0.571    | 20          |
| Adj_adj      | 0.00      | 0.00   | 0.00     | 6           |
| Adj_adv      | 0.00      | 0.00   | 0.00     | 2           |
| Noun_adj     | 0.765     | 0.382  | 0.510    | 34          |
| Det_noun     | 1.00      | 0.550  | 0.710    | 20          |
| Noun_noun    | 0.100     | 0.500  | 0.167    | 2           |
| Noun_prep    | 0.511     | 0.575  | 0.541    | 40          |
| Verb_adv     | 0.333     | 0.667  | 0.444    | 6           |
| Verb_chain   | 0.800     | 0.800  | 0.800    | 5           |
| Adv_adv      | 0.00      | 0.00   | 0.00     | 1           |
| To_verb      | 0.00      | 0.00   | 0.00     | 2           |

Regarding the detection per se, the results are as follow:

| Precision | Recall | F-score |
|-----------|--------|---------|
| 0.76      | 0.98   | 0.86    |

These results can be obtained running `eval.py`.  
**Please note that to run `eval.py`, it is necessary to change
`from .utils import get_type` (line 7 in `preprocessor.py`)
to
`from utils import get_type`.
 To run `run.py` after running evaluation, it must then be changed to `from .utils import get_type` again.**
