"""
   JaDe is a command-line tool to automatically detect enjambment in English 
   poetry. This file is JaDe's runner. See `python run.py --help` for further
   information on how to run it. 

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

import fnmatch
import os
import pathlib
import re
import sys
import click
import spacy
from tqdm import tqdm
from JaDe.jade.processing import processor


def get_filename(file): 
    filename = re.search(r'(\w*[\/\\])+(?P<name>(\w*[ _\d]?)+)', str(file)).group('name')
    filename = re.sub(r'[\?:;,\'! \.]', '_', filename)

    if filename.endswith('_'):
        filename = filename[:-1]
    
    return filename


@click.command()
@click.option('--model', help="Language model to be used", default='en_core_web_sm')
@click.option('--dir', help="Path to the directory to analyze", default=None, multiple=True)
@click.option('--file', help="Path to the file to analyze", default=None, multiple=True)
@click.option('--save', help="Specify whether or not the analysis should be saved.\
            Only works at file level.", default=True)
@click.option('--outfile', help="Path to where the analyzed file should be saved",
            default=None, multiple=True)
@click.option('--outdir', help="Path to where the analyzed files in input\
            directory should be saved", default=None, multiple=True)
def run(model, dir, file, outdir, outfile, save): 
    """
        JaDe command-line interface manager. 

        The --.*dir options and the --.*file options are mutually exclusive. 
        By default, all of them are set to None, except save, set to True.

        Parameters
        ----------
            model: str
                language model to be used. Default to spacy smaller one.
            dir: str
                Path to the directories to be analysed. To analyse a batch of 
                directories, use a comma to separate each path. Eg
                `--dir ../sylvia_plath,../oscar_wilde`. Please note that if
                there is a space in your path, you need to wrap it around double
                quotes `--dir "../oscar wilde".
            outdir: str
                Path to where the files should be saved after analysis. Default
                to current working directory. Please note that if
                there is a space in your path, you need to wrap it around double
                quotes `--dir "../oscar wilde". It can accept several outdirs, 
                as long as they are separated by commas, eg 
                `--outdir ../annotated_oscar_wilde,../annotated_sylvia_plath`.
            file: str
                Path to the files to be analysed. Several files can be analysed
                at the same time if their path is comma-separated, eg 
                `--file sylvia_plath/Admonition.txt,sylvia_plath/Amnesiac.txt`.
                Please note that if there is a space in your path, you need to 
                wrap it around double quotes `--file "../sylvia plath/Admonition.txt"
            outfile: str
                Path to where the file will be saved after analysis. Default to
                *filename*.txt in the current working directory. Several outfiles
                can be provided (if several files are provided as well), eg
                `--outfile annotated_Admonition.txt,annotated_Amnesiac.txt`.
                Please note that if there is a space in your path, you need to 
                wrap it around double quotes 
                `--outfile "../sylvia plath/annotated Admonition.txt"
            save: bool
                Whether or not the save is to be enabled. Can be set to False for
                single file analysis only. 
    """
    nlp = spacy.load(model)

    if len(file) == 0:
        file = None

    if len(dir) == 0: 
        dir = None

    if str(save).capitalize() == "False": 
        save = False
    elif str(save).capitalize() == "True": 
        save = True
    else: 
        print('save options only accepts True or False.')

    if dir is None and file is not None: 
        
        if len(file) > 1:
            print('For ease of reading, output will be saved in your working directory. It will be preceded by `annotated`.')
            save = True
                
        for i in range(len(file)):
            curr_file = file[i]
            with open(curr_file, 'r', encoding='utf-8') as poem_file:
                file_name = get_filename(str(curr_file))

                try: 
                    curr_outfile = outfile[i]
                except (IndexError, AttributeError, TypeError):
                    curr_outfile = 'annotated_' + file_name + '.txt'

                processor(poem_file, save, curr_outfile, nlp)
                print("File has been saved to disk at", curr_outfile)

    elif dir is not None and file is None: 
        for j in range(len(dir)): 
            curr_dir = dir[j].replace(' ', '_')
            print(curr_dir)
            
            if not curr_dir.endswith('\\') and sys.platform.startswith('win') and '\\' in curr_dir: 
                    curr_dir = curr_dir + r'\\'
                    curr_dir = curr_dir[:-1]
            elif not curr_dir.endswith('/'):
                curr_dir = curr_dir + '/'

            try: 
                curr_outdir = outdir[j]
            except (IndexError, AttributeError, TypeError):
                curr_outdir = 'annotated_' + re.search(r'.*[\\\/](?P<name>(\w*[ _]?)+)(?=[\\\/]$)',  curr_dir).group('name')
                print(curr_dir)

            if save:
                files = [curr_dir+file for file in os.listdir(curr_dir) if fnmatch.fnmatch(file, '*.txt')]

                for i in tqdm(range(len(files))):
                    with open(files[i], 'r', encoding='utf-8') as poem_file:
                        file_name = get_filename(str(files[i]))

                        outfile = curr_outdir + '/' + file_name + '.txt'

                        if sys.platform.startswith('win'):
                            outfile = str(pathlib.PureWindowsPath(outfile))

                        if not os.path.exists(curr_outdir): 
                            os.mkdir(curr_outdir)

                        processor(poem_file, save, outfile, nlp)
                print('Files have been saved to disk at', curr_outdir)
                
            else: 
                print('For readability, the --dir command can only be run when save is enabled')
                print('By default, the --save argument is set to True.')
                sys.exit(0)

    elif dir is not None and file is not None: 
        print('JaDe cannot simultaneously analyze a single file and a whole directory.')
        print('Please specify either --dir or --file, not both.')
        sys.exit(0)

    else:
        print("None of the options were recognized or passed.")
        print("Accepted options are --file, --outfile, --dir, --outdir and --save")
        print("Run run.py --help for further information.")
        sys.exit(0)

if __name__ == "__main__":
    run()