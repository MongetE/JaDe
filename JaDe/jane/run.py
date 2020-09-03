"""
   JaDe is a command-line tool to automatically detect enjambment in English 
   poetry. This file aims to provie an example on how to use charmak, a simple
   bokeh wrapper. Building diagrams helps to get insight on enjambment 
   distribution according to various criteria. 

    Copyright (C) 2020  Eulalie Monget

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os 
import pathlib
import re
import sys
from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.palettes import cividis
from charmak.diagrams import classic_barplot

def get_annotation(directory): 
    """
        Retrieve JaDe's annotations in a given directory. 

        Parameters
        ----------
            directory: pathlib.Path
                path to the annotated file
    
        Returns
        -------
            directory_annotations: list
                list of every annotation found in the directory
    """
    directory_annotations = []
    for file in directory.iterdir():

        with open(str(file), 'r', encoding='utf-8') as curfile: 
            poem = curfile.read()
            annotations = re.findall(r'\[.*?\]', poem, flags=re.MULTILINE)
        
        for annotation in annotations:
            directory_annotations.append(annotation)

    return directory_annotations


def build_plot_dict_list(new_values, existing_list=None): 
    """
        Updates values of a given list. 

        When building the data required for multi bars plot from different 
        directory (eg authors from a given century if each author has their own 
        directory), the number of occurrences of a given type may need to be 
        updated (dictionary for multi_bar_plot() should look like: 
        {enjambment_types: [types], compared_value_1: [0,1,2.], 
        compared_value_2: [3,4,5]})

        Parameters
        ----------
            existing_list: list
                
    """
    if len(existing_list) > 0 or existing_list is None:
        tmp_list = []
        for i in range(len(new_values)):
            tmp_value = existing_list[i] + new_values[i]
            tmp_list.append(tmp_value)
        
        return tmp_list

    else: 
        existing_list = new_values

        return existing_list


def run(working_dir, title):
    """
        The goal is to provide a quick way to build classic diagrams and give 
        an example on how the data need to be built for other kinds of charts, 
        bearing in mind that it may vary slightly from one type to another. 

        The two arguments, working_dir and title, are to be given when running 
        the script, for ex: `python run.py /path/to/annotated/files chart_name`.

        More details on the arguments accepted by each type of diagram can 
        be found in charmak.diagrams' docstring or in the project documentation.

        Parameters
        ----------
            working_dir: str
                path to the annotated files

            title: str
                title of the chart to be built 
    """

    working_path = pathlib.Path(working_dir)
    annotations = get_annotation(working_path)

    chart_data = {}
    
    for annotation in annotations: 
        annotation = annotation.replace('[', '').replace(']', '')
        try: 
            chart_data[annotation] += 1 
        except KeyError: 
            chart_data[annotation] = 1


    x_axis = list(chart_data.keys())
    y_axis = list(chart_data.values())
    x_name = 'enjambment_types'
    y_name = 'number_of_occurrences'

    source = ColumnDataSource(data=dict(enjambment_types=x_axis, number_of_occurrences=y_axis))
    chart = classic_barplot(x_axis, x_name, y_axis, y_name, source=source, title=title, orientation='vertical', y_margin=5)
    grid = gridplot([[chart]])
    show(grid)


if __name__ == "__main__":
    working_dir, title = sys.argv[1:]
    run(working_dir, title)