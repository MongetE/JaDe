# JaDe - enJambment Detection

JaDe is a tool to detect and classify enjambment in English poetry.
The aim is to help researchers in stylistics to gather more evidence to support
their claims.

## Repository Structure

1. [JaDe](https://github.com/MongetE/JaDe/tree/master/JaDe): contains code and
resources necessary to run the tool
    - [jade](https://github.com/MongetE/JaDe/tree/master/JaDe/jade): source code
    - [ressources](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/): txt files
        1. [annotated_poems](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/annotated_poems):
        poems used for tool evaluation
        2. [detected](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/detected):
        poem from the test corpus annotated by the tool
        3. phrasal_verbs.txt: list of phrasal verbs supported by the classifier
2. script_corpus: contains scripts used to gather the corpus [to be added]

## Requirements

- python3.7
- spacy
- fuzzywuzzy
- click
- tqdm

Required libraries can be installed using `pip install -r requirements.txt`.

*Note*  
Spacy requires a language model. By default, the model used is  the
`en_core_web_sm` one.

To install a spacy model, run `python -m spacy download "modelname"`.

## Run JaDe

JaDe can be run using `python run.py [OPT]`. A list of all options available is
available through `python run.py --help`.

Basic usage include a single file analysis or the analysis of a whole directory
at once.  

### Single file analysis

`python run.py --file path/to/file --save False`  
This will analyse the given file and print the result in the prompt.  
By default, the `--save` option is set to `True`, thus saving the file if the
`--outfile` option is passed.
If it is not specified but the `--save` argument is default, the analysis will
be saved in the current directory.

### Directory analysis

`python run.py --dir path/to/dir`  
The `--save` option MUST be set to True: for readability's sake, the analysis
won't be printed in the prompt.  
By default, if `--outdir` is not specified, the analysed files will be saved in
a `analysis` directory, created in the current working directory.

## Results

The evaluation was perfomed with all three spaCy models. However, they did not
significantly improved as the model got bigger. Thus, only the results obtained
with the smallest model are presented below:

|                   | precision | recall | f1-score | support |
|-------------------|-----------|--------|----------|---------|
| []                | 0.836     | 0.936  | 0.883    | 598     |
| [cc_cross_clause] | 0.833     | 0.500  | 0.625    | 20      |
| [ex_dobj_pverb]   | 1.000     | 0.333  | 0.500    | 3       |
| [ex_dobj_verb]    | 0.718     | 0.459  | 0.560    | 61      |
| [ex_subj_verb]    | 0.388     | 0.442  | 0.413    | 43      |
| [ex_verb_adjunct] | 0.400     | 0.035  | 0.065    | 57      |
| [pb_adj_adj]      | 1.000     | 0.500  | 0.667    | 6       |
| [pb_adj_adv]      | 0.200     | 0.500  | 0.286    | 2       |
| [pb_adj_prep]     | 1.000     | 0.167  | 0.286    | 6       |
| [pb_adv_adv]      | 0.000     | 0.000  | 0.000    | 1       |
| [pb_comp]         | 0.286     | 0.667  | 0.400    | 3       |
| [pb_det_noun]     | 0.923     | 0.600  | 0.727    | 20      |
| [pb_noun_adj]     | 0.958     | 0.676  | 0.793    | 34      |
| [pb_noun_noun]    | 0.091     | 0.500  | 0.154    | 2       |
| [pb_noun_prep]    | 0.556     | 0.625  | 0.588    | 40      |
| [pb_phrasal_verb] | 1.000     | 0.167  | 0.286    | 6       |
| [pb_relword]      | 0.778     | 0.318  | 0.452    | 22      |
| [pb_to_verb]      | 1.000     | 0.500  | 0.667    | 2       |
| [pb_verb_adv]     | 0.400     | 0.667  | 0.500    | 6       |
| [pb_verb_chain]   | 0.800     | 0.800  | 0.800    | 5       |
| [pb_verb_cprep]   | 0.500     | 0.125  | 0.200    | 8       |
| [pb_verb_prep]    | 0.081     | 0.429  | 0.136    | 7       |
| **accuracy**      |           |        | 0.745    | 952     |
| **macro_avg**     | 0.625     | 0.452  | 0.454    | 952     |
| **weighted_avg**  | 0.762     | 0.745  | 0.728    | 952     |

**NB**:

- the evaluation of the classification work is done using scikit. When
running the evaluation module, the classification report gives the measures for
a ‘[]’ class. This ‘[]’ is normally used to indicated that there is an
end-stopped line. However, for evaluation purposes, some types (such as the
lexical one) are replaced by this class. As a consequence, these measures cannot
account for the precision, recall and f1-score for the detection task. So far,
any attempt to remove this class from the classification report resulted in the
report failure. What's more, the accuracy, macro_avg and weighted_avg are
slightly biased because of this class.
- When evaluating each classifier separately, a [?] class appears. This class
stands for enjambment context that are not supported by the evaluated classifier.


Regarding the detection per se, the results are as follow:

| Precision | Recall | F-score |
|-----------|--------|---------|
| 0.96      | 0.90   | 0.93    |

These results can be obtained by running `run_eval.py`.

**Please note that to run `run_eval.py` with `--annotate True`, it is necessary
to change `from .utils import get_type` (line 7 in `JaDe/jade/preprocessor.py`)
to `from utils import get_type`.
To run `run.py` after running evaluation, it must then be changed to
`from .utils import get_type` again.**
