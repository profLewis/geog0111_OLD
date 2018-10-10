#!/usr/bin/env python
"""Procuring datasets for geog0111
The functions in this file deal with obtaining datasets for the Geog0111 course
at UCL Geography. The datasets are available over the internet, and are also
stored locally in the server. In case you're local to UCL Geography, symbolic
links will be created in your local folder, to avoid copying files across. If
you are outside, the files will be downloaded.

In either case, a directory called `data` will be created and things will end up
there.

From the user's provided perspective, each dataset will be a folder within somewhere
in the system. I recommend using symbolic links to make it accessible to the outside
work through e.g. `~/public_html`. Each folder should just contain a bunch of files,
so if you want to provide data in folders, provide a dataset for each of the folders.
"""

import urllib.request
from pathlib import Path
from socket import getfqdn

from bs4 import BeautifulSoup

__author__ = "J Gomez-Dans"
__copyright__ = "Copyright 2018 J Gomez-Dans"
__license__ = "GPLv3"
__email__ = "j.gomez-dans@ucl.ac.uk"

def procure_dataset(dataset_name, destination_folder="data",
                    location="/data/selene/ucfajlg/geog011_data/",
                    url="http://www2.geog.ucl.ac.uk/~ucfajlg/geog0111_data/"):

    """Procure a Geog0111 dataset. This function will look for the dataset called
    `dataset_name`, and either provide symbolic links or download the relevant
    files to a local folder called by default `data`, or with a user-provided name.
    The other two options are to do with the location of the dataset witin the UCL
    filesystem (`location`), and the external URL (`url`). It is assumed that in
    either case, `datasest_name` is a valid folder under both `location` and `url`.
    """
    fully_qualified_hostname = getfqdn()
    if fully_qualified_hostname.find("geog.ucl.ac.uk") >= 0:
        print("Running on UCL's Geography computers")
        generate_symlinks(dataset_name, location, destination_folder=destination_folder)
    else:
        print("Running outside UCL Geography. Will need to download data. This might take a while!")
        try:
            print("trying geog server ...")
            download_data(dataset_name, url, destination_folder=destination_folder)
        except:
            print("trying NASA server ...")
            save_data(dataset_name)

def generate_symlinks(dataset_name, location, destination_folder, verbose=True):
    """Generates symbolic links for a given dataset."""
    dest_path = Path(destination_folder)
    if not dest_path.exists():
        dest_path.mkdir()
    the_path = Path(location)/Path(dataset_name)
    if the_path.exists():
        files = [f for f in the_path.rglob("**/*")]
        for fich in files:
            try:
                (dest_path/Path(fich.name)).symlink_to(fich)
            except FileExistsError:
                (dest_path/Path(fich.name)).unlink()
                (dest_path/Path(fich.name)).symlink_to(fich)
            if verbose:
                print(f"Linking {fich} to {dest_path/Path(fich.name)}")


def download_data(dataset_name, url, destination_folder, verbose=True):
    """Downloads a dataset from UCL servers."""
    dest_path = Path(destination_folder)
    if not dest_path.exists():
        if verbose:
            print("Creating destination directory")
        dest_path.mkdir()
    resp = urllib.request.urlopen(f"{url:s}/{dataset_name:s}")
    if resp.code != 200:
        return None
    soup = BeautifulSoup(resp, "lxml",
                         from_encoding=resp.info().get_param('charset'))

    for pos, link in enumerate(soup.find_all('a', href=True)):
        if pos > 4:
            # Skip first crufty links...
            file_to_download = f"{url:s}/{dataset_name:s}/{link['href']:s}"
            dest_file = dest_path/Path(link['href'])
            if dest_file.exists():
                dest_file.unlink()
            with open(dest_file, 'wb') as filep:
                req = urllib.request.urlopen(file_to_download)
                filep.write(req.read())
            hdrs = req.getheaders()
            for hdr in hdrs:
                if hdr[0] == "Content-Length":
                    remote_size = int(hdr[1])
            local_size = dest_file.stat().st_size
            if local_size != remote_size:
                raise IOError("Remote and local file sizes differ!")
            if verbose:
                print(f"Remote file: {link['href']:s} ({remote_size:d} bytes) " +
                      f"-> {dest_file.absolute()} ({local_size:d} bytes) -> " + u'\u2713')


'''
Further codes by Lewis
'''
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from cylog import cylog
import datetime 

def save_data(filename,url='https://e4ftl01.cr.usgs.gov/MOTA',destination_folder='data'):
    """Downloads hdf data from a NASA URL for the specified tiles
       and saves the files in destination_folder.
       
       Checks to see if destination_folder exists, if not,
       creates it.
       
       Could do with further error checking
       
    Parameters
    ----------
    filename: string
        MODIS product filename
    destination_folder: str
        The destination folder
    url: str
        The required URL
    
    Returns
    --------
    A string with the location of the downloaded file.
    """

    

    # make sure destination_folder exists
    dest_path = Path(destination_folder)
    if not dest_path.exists():
        dest_path.mkdir()

    # sort rest of url
    product,adate,tile,version,code,hdf = filename.split('.')
    year = int(adate[1:5])
    doy = int(adate[5:])
    d = datetime.datetime(year,1,1) + datetime.timedelta(doy-1)
    fdate = f'{d.year}.{d.month}.{d.day}'
    url = f'{url}/{product}.{version}/fdate/'
 
    # make a compound file name from folder and filename
    output_fname = dest_path.joinpath(filename)
    
    # does the file already exist?
    if not output_fname.exists():
        # put download and save code here
        with requests.Session() as session:
            # get password-authorised url
            session.auth = cylog().login()
            r1 = session.request('get',url+filename)
            r2 = session.get(r1.url)
            with open(output_fname, 'wb') as fp:
                r = fp.write(r2.content)
    else:
        print(f'file {output_fname} exists')            
    return str(output_fname)
