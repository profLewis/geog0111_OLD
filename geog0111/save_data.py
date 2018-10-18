from pathlib import Path

__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

'''
save_data(data,filename,destination_folder)` that takes the binary dataset `data` and writes it to the file `filename` in directory `destination_folder`. It should return the n umber of bytes written, and should check to see if files / directories exist and act accordingly.
'''

def save_data(data,filename,destination_folder,overwrite=False):
    '''
    Save data in data to destination_folder/filename

    Arguments:
    ---------

    data   : binary array
    filename : string: name of output file
    destination_folder: name of output directory (created if not existing)

    Keyword Arguments:
    -----------------

    overwrite : overwrite file if it already exists
    '''
    dest_path = Path(destination_folder)
    if not dest_path.exists():
        dest_path.mkdir()

    output_fname = dest_path.joinpath(filename)

    d = 0
    if overwrite or (not output_fname.exists()):  
        with open(output_fname, 'wb') as fp:
            d = fp.write(data)

    return(d)
  
