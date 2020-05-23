import fnmatch
import os
import pathlib
import re
import sys
import click
from tqdm import tqdm
from JaDe.jade.preprocessor import main

@click.command()
@click.option('--dir', help="Path to the directory to analyze", default=None)
@click.option('--file', help="Path to the file to analyze", default=None)
@click.option('--save', help="Specify whether or not the analysis should be saved.\
            Only works at file level.", default=True)
@click.option('--outfile', help="Path to where the analyzed file should be saved",
            default=None)
@click.option('--outdir', help="Path to where the analyzed files in input\
            directory should be saved", default=None)

def run(dir, file, outdir, outfile, save): 
    """
        JaDe command-line interface manager. 

        The --.*dir options and the --.*file options are mutually exclusive. 
        By default, all of them are set to None, except save, set to True.

        Parameters
        ----------
            dir: str
                Path to the directory to be analysed. 
            outdir: str
                Path to where the files should be saved after analysis. Default
                to current working directory. 
            file: str
                Path to the file to be analysed
            outfile: str
                Path to where the file will be saved after analysis. Default to
                filename.txt in the current working directory
            save: bool
                Whether or not the save is to be enabled. Can be set to False for
                single file analysis only. 
    """
    if save != True:
        if save.capitalize() == "False": 
            save = False
        else: 
            print('--save only accepts True or False.')

    if dir is None and file is not None: 
        with open(file, 'r', encoding='utf-8') as poem_file:
            filename = re.search(r'(\w*[\/\\])+(?P<name>(\w*[ _\d]?)+)', str(file)).group('name')

            if outfile is None: 
                outfile = filename + '.txt'

            main(poem_file, save, outfile)

    elif dir is not None and file is None: 
        if not dir.endswith('/'):
            dir += '/'
            
        if outdir is None: 
            outdir = "analysis"

        if save:
            files = [dir+file for file in os.listdir(dir) if fnmatch.fnmatch(file, '*.txt')]

            for i in tqdm(range(len(files))):
                with open(files[i], 'r', encoding='utf-8') as poem_file:
                    filename = re.search(r'(\w*[\/\\])+(?P<name>(\w*[ _\d]?)+)', str(files[i])).group('name')
                    outfile = outdir + '/' + filename + '.txt'

                    if sys.platform.startswith('win'):
                        outfile = str(pathlib.PureWindowsPath(outfile))

                    if not os.path.exists(outdir): 
                        os.mkdir(outdir)

                    main(poem_file, save, outfile)
                
        else: 
            print('For readability, the -dir command can only be run when save is enabled')
            print('By default, the -save argument is set to True.')
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