# JaDe - en**Ja**mbment **De**tection

JaDe is a tool to detect and classify enjambment in English poetry.
The aim is to help researchers in stylistics to gather more evidence to support
their claims. A web app to play around is available [there](https://enjambment-detection.herokuapp.com/).

Don't forget to visit the [wiki](https://github.com/MongetE/JaDe/wiki).

## Repository Structure

[JaDe](https://github.com/MongetE/JaDe/tree/master/JaDe): contains code and
resources necessary to run the tool

- [jade](https://github.com/MongetE/JaDe/tree/master/JaDe/jade): source code
- [ressources](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/): txt files
    1. [annotated_poems](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/annotated_poems):
    manually annotated poems used for tool evaluation
    2. [detected](https://github.com/MongetE/JaDe/tree/master/JaDe/resources/detected):
    poems from the test corpus annotated by the tool
    3. phrasal_verbs.txt: list of phrasal verbs supported by the classifier
- [jane](https://github.com/MongetE/JaDe/tree/master/JaDe/jane): examples for
    en**Ja**mbment a**N**alysis. Jane includes a `run.py` file, which is a basic example
    on how to use JaDe and [charmak](https://github.com/MongetE/JaDe/tree/master/JaDe/jane/charmak)
    for enjambment analysis. It also includes a ipynb file, also found [here](https://nbviewer.jupyter.org/github/MongetE/JaDe/blob/master/JaDe/jane/jane.ipynb?flush_cache=true),
    which explains how to build multibars plot (see [here](https://github.com/MongetE/JaDe/blob/master/JaDe/jane/img/no_provided.png) for an example) so as to carry
    out a ***comparative*** analysis.

## Getting started

### Requirements

- python3.7
- spacy
- fuzzywuzzy
- click
- tqdm
- matplotlib
- pandas
- seaborn
- bokeh
- scikit_learn
- numpy

Required libraries can be installed using `pip install -r requirements.txt`.

*Note*  
Spacy requires a language model. By default, the model used in this project is the
`en_core_web_sm` one.

To install a spacy model, run `python -m spacy download "modelname"`.

See [spaCy English models page](https://spacy.io/models/en) for further
information on the different models that can be used with JaDe.

### Quickstart

JaDe can be run using `python run.py [OPT]`. A list of all options available is
available through `python run.py --help`.

Basic usage include a single file analysis or the analysis of a whole directory
at once. See [Running JaDe](https://github.com/MongetE/JaDe/wiki/Running-JaDe)
for details on how to run JaDe on several directories or files at a time.

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
won't be printed in the prompt. If not passed, `--save` is set to True by default.
By default, if `--outdir` is not specified, the analysed files will be saved in
a `annotated_[original_directory_name]` directory, created in the working directory.

## Results

The evaluation was perfomed with all three spaCy models. However, they did not
significantly improved as the model got bigger. Thus, only the results obtained
with the smallest model are presented below:

| type              | precision | recall | f1-score | support |
|-------------------|-----------|--------|----------|---------|
| [pb_verb_adv]     | 0.571     | 0.667  | 0.615    | 6       |
| [pb_to_verb]      | 1.000     | 0.500  | 0.667    | 2       |
| [pb_phrasal_verb] | 1.000     | 0.167  | 0.286    | 6       |
| [pb_adj_adj]      | 1.000     | 0.500  | 0.667    | 6       |
| [pb_det_noun]     | 0.857     | 0.600  | 0.706    | 20      |
| [ex_subj_verb]    | 0.569     | 0.674  | 0.617    | 43      |
| [pb_adv_adv]      | 0.500     | 0.500  | 0.500    | 2       |
| [pb_verb_chain]   | 0.800     | 0.800  | 0.800    | 5       |
| [pb_noun_prep]    | 0.676     | 0.625  | 0.649    | 40      |
| [pb_noun_adj]     | 1.000     | 0.559  | 0.717    | 34      |
| [pb_verb_cprep]   | 0.500     | 0.250  | 0.333    | 8       |
| [ex_verb_adjunct] | 0.500     | 0.017  | 0.032    | 60      |
| [ex_dobj_verb]    | 0.846     | 0.541  | 0.660    | 61      |
| [pb_verb_prep]    | 0.061     | 1.000  | 0.114    | 2       |
| [pb_adj_adv]      | 1.000     | 0.500  | 0.667    | 2       |
| [pb_adj_prep]     | 1.000     | 0.167  | 0.286    | 6       |
| [pb_noun_noun]    | 0.125     | 0.500  | 0.200    | 2       |
| [pb_comp]         | 0.333     | 0.667  | 0.444    | 3       |
| [cc_cross_clause] | 1.000     | 0.600  | 0.750    | 20      |
| [pb_relword]      | 0.800     | 0.364  | 0.500    | 22      |
| [ex_dobj_pverb]   | 1.000     | 0.333  | 0.500    | 3       |
| **micro_avg**     | 0.634     | 0.462  | 0.534    | 353     |
| **macro_avg**     | 0.721     | 0.501  | 0.510    | 353     |
| **weighted_avg**  | 0.738     | 0.462  | 0.522    | 353     |

Regarding the detection per se, the results are as follow:

|           | precision | recall | f1-score | support |
|-----------|-----------|--------|----------|---------|
| accuracy  |           |        | 0.857    | 952     |
| macro_avg | 0.859     | 0.831  | 0.841    | 952     |
| micro_avg | 0.858     | 0.857  | 0.854    | 952     |

These results can be obtained by running `evaluation.py`.

### Running evaluation

Evaluation can be performed on the system as a whole or on a specific classifier.
However, a change in evaluation mode (overall vs specific), the `--annotate`
argument MUST be set to `True`. Otherwise, the evaluation will be performed
on the annotations obtained for the previous mode. For example, if the evaluation
was run with `--classifier all` and `--classifier dependencies` is run after
without `annotate True`, then the results would also includes the annotations
made by the regex classifier.

For instance, `cross-clause` results are :
|              | precision | recall | f1-score | support |
|--------------|-----------|--------|----------|---------|
| overall      | 1.000     | 0.600  | 0.750    | 20      |
| regex        | 1.000     | 0.450  | 0.621    | 20      |
| dependencies | 0.667     | 0.500  | 0.571    | 20      |

See [here](https://github.com/MongetE/JaDe/wiki/Evaluation)
for more information on the different options to evaluate JaDe
