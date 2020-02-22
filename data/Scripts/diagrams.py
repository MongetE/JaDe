from math import pi

import pandas as pd

from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

output_file("data_corpus.html")

def create_diagrams(values, legend, title, colors=Category20c):
    """ 
        Values must be a dictionary where the key
        is the the element to be represented and the
        values its proportion
    """

    data = pd.Series(values).reset_index(name='value').rename(columns={'index':legend})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = colors[len(values)]

    pie = figure(plot_height=350, title=title,
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
    nationalities = {
        'American': 24,
        'British': 26, 
        'Indian': 1, 
        'Irish': 5, 
        'St Lucian': 1, 
        'Scottish': 3,
        'Jamaican': 1,
        'Welsh': 1 
    }

    poems = {
        '14th': 73, 
        '16-17th': 423, 
        '17-18th': 504,
        '17th': 350,
        '18-19th': 646,
        '18th': 356,
        '19-20th': 2301,
        '19th': 3022,
        '20th': 1917,
        '20-21th': 156
    }


    poets = {
        '14th': 1, 
        '16-17th': 2, 
        '17-18th': 3,
        '17th': 3,
        '18-19th': 4,
        '18th': 1,
        '19-20th': 12,
        '19th': 19,
        '20th': 14,
        '20-21th': 3
    }

    gender = {
        'men': 45, 
        'women': 17,
        '': 0
    }

    pie_nation = create_diagrams(nationalities, 'country', 'Number of poets per nationality')
    pie_poems = create_diagrams(poems, 'century', 'Number of poems per century')
    pie_poets = create_diagrams(poets, 'century', 'Number of poets per century')
    pie_gender = create_diagrams(gender, 'gender', 'Number of poets per gender')

    grid = gridplot([[pie_nation, pie_gender], [pie_poets, pie_poems]])

    # show the results
    show(grid)