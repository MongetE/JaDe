from math import pi

import pandas as pd

from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category20b_18

output_file("disagreement.html")

def create_diagrams(values, legend, title, colors=Category20b_18):
    """ 
        Values must be a dictionary where the key
        is the the element to be represented and the
        values its proportion
    """

    data = pd.Series(values).reset_index(name='value').rename(columns={'index':legend})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = colors[:len(values)]

    pie = figure(plot_width = 675, plot_height=500, title=title,
            toolbar_location=None, tools="hover", tooltips=f"@{legend}: @value", x_range=(-0.5, 1.0))

    pie.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend=legend, source=data)

    pie.axis.axis_label=None
    pie.axis.visible=False
    pie.grid.grid_line_color = None
    pie.title.align = "center"
    pie.title.text_font_size = "18px"

    return pie

if __name__ == "__main__":
    disagreement_null = { 
        "_|pb_adj_adv" : 1,
        "_|cc_cross_clause" : 6,
        "_|ex_dobj_verb" : 10, 
        "_|pb_adj_prep": 3, 
        "_|pb_verb_cprep" : 3,
        "_|pb_noun_adj" : 8,
        "_|pb_noun_noun" : 1,
        "_|pb_verb_adv" : 1,
        "_|ex_subj_verb" : 4,
        "_|pb_relword" : 19,
        "_|pb_noun_prep" : 6,
        "_|pb_adv_verb" : 1, 
        "_|pb_verb_adj" : 1, 
        "_|adv_noun" : 2,
        "_|pb_phrasal_verb" : 1, 
        "_|ex_dobj_pverb" : 1
    }

    disagreements =  {
        "ex_subj_verb|ex_dobj_verb" : 3,
        "pb_verb_cprep|pb_phrasal_verb" : 3,
        "ex_dobj_verb|pb_phrasal_verb" : 1,
        "cc_cross_clause|pb_noun_prep" : 1,
        "pb_noun_noun|pb_adj_noun" : 1,
        "pb_relword|ex_dojb_verb" : 2,
        "pb_relword|pb_adj_adj" : 1, 
        "pb_verb_adv|pb_phrasal_verb" : 1,
        "pb_lexical|pb_noun_noun" : 1, 
        "pb_relword|pb_noun_adj" : 2,
        "ex_subj_verb|pb_adj_prep": 1,
        "pb_adv_adv|pb_adv_prep" : 1,
        "pb_verb_chain|pb_verb_cprep" : 2,
        "pb_noun_adj|pb_adj_adj" : 1,
        "pb_relword|pb_noun_prep" : 2,
        "ex_subj_verb|pb_noun_adj" : 1, 
        "pb_noun_adj|pb_noun_prep" : 9
    }

    pie__ = create_diagrams(disagreement_null, 'disagreement', 'Disagreement pairs')
    pie_disagreement = create_diagrams(disagreements, 'disagreement', 'Disagreement pairs')
    grid = gridplot([[pie__, pie_disagreement]])

    # show the results
    show(grid)

