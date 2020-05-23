# JaDe - enJambment Detection

JaDe is a tool to detect and classify enjambment in English poetry. 
The aim is to help researchers in stylistics to gather more evidence to support their claims. 

## Repository Structure

to be done

## Requirements

- python3.7
- spacy
- fuzzywuzzy
- python-levenshtein

Required libraries can be installed using `pip install -r requirements.txt`.

*Note*
Spacy requires a model. The current version of JaDe was tested with the `en_core_web_sm`, so the results
prenseted below are valid with that given model. No test was done yet with spacy bigger models.  
To install a spacy model, run `python -m spacy download "modelname"`.

## Run JaDe

to be done

## Results

As of JaDe 1.0, 11 types of enjambment are supported for classification. Out of these 11 types, 7 yield relatively
satisfactory results, using only the part-of-speech tag.

The results for the classification task are presented below:

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
