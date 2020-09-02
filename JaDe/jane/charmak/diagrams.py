import numpy
import pandas as pd
from math import pi
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, dodge, cumsum
from .utils import random_colors


# worked at first but seems there is a problem with bokeh since even example 
# from gallery did not work afterwards
#TODO: verify that it still works correctly
def stacked_plot(x, y, data, title, x_name, orientation='horizontal', plot_width=750, height=750, colors=None, y_start=0, 
                location='top_left', bar_width=0.5, save=False, save_name=None):
    """
        Build stacked diagrams in a jiffy. 
        `Example of stacked diagram <https://docs.bokeh.org/en/latest/docs/gallery/bar_stacked.html>`_

        Parameters
        ----------
            x: list
                Data to be shown on the x axis
            y: list 
                Data to be shown on the y axis
            title: str
                Title of the diagram
            orientation: str
                Orientation of the labels on the x axis. Default to horizontal.
            plot_width: int
                Plot width, default to 750px.
            height: int
                Plot height, default to 750px.
            colors: list
                List of colors to be used. Default to None (random colors are
                generated according to the number of x items). 
            y_start: int
                Y axis' starting value
            location: str
                Legend location, default to top left.
            bar_witdh: float or int
                Bar width, default to 0.5
            save: bool
                Whether the diagram should be saved in html file. Default to False
            save_name: str
                Name of the html file. If one is provided but save is still set 
                to False, save anyway. Default to None.
        
        Returns
        -------
            stacked_figure: figure
                A Bokeh stacked figure.
    """
    if colors is None:
        colors = random_colors(len(data)) 

    tooltips = f'$name @{x_name}: @$name'

    stacked_figure = figure(x_range=x, plot_height=height, plot_width=plot_width, title=title,
            toolbar_location=None, tools="hover", tooltips=tooltips)

    stacked_figure.vbar_stack(y, x=x_name, width=bar_width, colors=colors, source=data,
                legend_label=y)

    stacked_figure.y_range.start = 0
    stacked_figure.x_range.range_padding = 0.1
    stacked_figure.legend.location = location
    stacked_figure.legend.orientation = orientation
    stacked_figure.xaxis.major_label_orientation = orientation

    if save or save_name is not None:
        output_file(save_name)

    return stacked_figure


def classic_barplot(x, x_name, y, y_name, source, title, height=750, plot_width=750, colors=None, orientation='horizontal', 
                    location='top_left', save=False, save_name=None, y_max=None, y_margin=0, shown_legend=False, 
                    y_start=0): 
    """
        Build classic bar diagrams in a jiffy. 
        `Example of classic diagram <https://docs.bokeh.org/en/latest/docs/gallery/bar_colormapped.html>`_

        Parameters
        ----------
            x: list
                Data to be shown on the x axis
            y: list 
                Data to be shown on the y axis
            x_name: str
                name of the x axis data (same than in source)
            y_name: str
                name of the y axis (same than in source)
            y_max: int
                Maximum value for y axis. If None is passed, then see y_margin.
            y_margin: int
                Used to compute maximum value for y axis. If default (0), y_max 
                is equal to max(y), else to max(y) + y_margin. Default to 0.
            source: ColumnDataSource
                Mapping between the axis data and the axis label. 
            title: str
                Title of the diagram
            orientation: str
                Orientation of the labels on the x axis. Default to horizontal.
            plot_width: int
                Plot width, default to 750px.
            height: int
                Plot height, default to 750px.
            colors: list
                List of colors to be used. Default to None (random colors are
                generated according to the number of x items). 
            y_start: int
                Y axis' starting value
            location: str
                Legend location, default to top left.
            bar_witdh: float or int
                Bar width, default to 0.5
            save: bool
                Whether the diagram should be saved in html file. Default to False
            save_name: str
                Name of the html file. If one is provided but save is still set 
                to False, save anyway. Default to None.
            shown_legend: bool
                Whether legend should be visible or not. Default to False 
                (legend is NOT shown)

        Returns
        -------
            bar_figure: figure
                A Bokeh bar figure.
    """
    if colors is None:
        colors = random_colors(len(x)) 

    bar_figure = figure(x_range=x, plot_height=height, plot_width=plot_width, toolbar_location=None, 
    title=title)
    bar_figure.vbar(x=x_name, top=y_name, width=0.5, source=source, legend_field="x",
        line_color='white', fill_color=factor_cmap(x_name, palette=colors, factors=x))

    bar_figure.xgrid.grid_line_color = None
    bar_figure.xaxis.major_label_orientation = orientation
    bar_figure.yaxis.axis_label_text_font_style = "italic"
    bar_figure.y_range.start = y_start  

    if y_max is None:
        bar_figure.y_range.end = max(y) + y_margin
    else:
        bar_figure.y_range.end = y_max
        
    bar_figure.legend.visible = shown_legend

    if save or save_name is not None:
        output_file(save_name)

    return bar_figure


def multibars_plot(data, title, orientation, width=1000, colors=None, y_margin=0, legend_location='top_right'):
    """
        Build multibars plot in a jiffy. 
        `Example of multibar plot <https://docs.bokeh.org/en/latest/docs/gallery/bar_nested_colormapped.html>`_

        Parameters
        ----------
            data: dict
                data from which the chart will be build. Should look like: 
                {enjambment_types: [types], compared_value_1: [0,1,2.], 
                compared_value_2: [3,4,5]}
            title: str
                title of the chart
            orientation: str
                orientation of the x axis labels (horizontal or vertical). See
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html?highlight=x_axis%20major_label_orientation
                for more information on valid inputs.
            width: int
                width of the plot
            colors: list
                colors to be used for the bars
            y_margin: int
                Used to compute maximum value for y axis. If default (0), y_max 
                is equal to max(y), else to max(y) + y_margin. Default to 0.
            legend_location: str
                where the legend should be displayed. Default to top_right. See
                https://docs.bokeh.org/en/latest/docs/reference/core/enums.html#bokeh.core.enums.LegendLocation
                for a list of valid values.

        Returns
        -------
            A Bokeh mutlibars figure.
    """
    potential_max = []
    for item, value in data.items():
        if 'types' not in item:
            potential_max.append(max(value))
        else:
            labels = value

    rounded_max = round(max(potential_max), -1)
    if rounded_max > max(potential_max): 
        y_range = rounded_max
    else: 
        y_range = max(potential_max) + y_margin
        
    source = ColumnDataSource(data=data)
    bar_figure = figure(x_range=labels, y_range=(0,y_range), plot_height=500, plot_width=width, 
                        toolbar_location=None, title=title)

    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        position_range = (len(data) * 0.25)/2
        positions = [i for i in numpy.arange(-position_range, position_range, 0.25)]
        number_of_colors = len(data.keys())
        
        if colors is None:
            colors = random_colors(number_of_colors)

        if 'types' in key:
            x_dodge = key
        else:
            bar_figure.vbar(x=dodge(x_dodge, positions[i], range=bar_figure.x_range), 
                            top=key, width=0.2, source=source, color=colors[i], legend_label=key)

    bar_figure.x_range.range_padding = 0
    bar_figure.xgrid.grid_line_color = None
    bar_figure.xaxis.major_label_orientation = orientation
    bar_figure.legend.location = legend_location
    bar_figure.legend.orientation = "horizontal"

    return bar_figure

