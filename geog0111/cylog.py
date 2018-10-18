from cryptography.fernet import Fernet
import numpy as np
from pathlib import Path
from getpass import getpass

__author__ = "P Lewis"
__copyright__ = "Copyright 2018 P Lewis"
__license__ = "GPLv3"
__email__ = "p.lewis@ucl.ac.uk"

class  cylog():
    '''
    cylog provides a mechanism to partially hide username and
    password information that is required in plain text.

    It does this by storing a key and the encrypted version in
    a file accessible only to the user.
    
    Of course, when called (by the user) the (username, password)
    are exposed in plain text, so only use this when you 
    have to enter plain text username/password information.

    It is written as a utility to allow UCL MSc students to 
    show access to NASA Earthdata dataset download, without 
    the need to expose (username, password) in a submitted report.

    Stores (in a dictionary in ~/{dest_path}/.cylog.npz) an
    encrypted form of username and password (and key)
   
    Uses cryptography.fernet.Fernet() for encryption
 
    cylog().login() : returns plain text tuple
                      (username, password) 
    '''
    def __init__(self,init=False,destination_folder='.cylog'):
        '''

        Keyword arguments 
        ----------
        init: bool
            to re-initialise the passord/username
            set to True. This will overwrite any existing password file.
 
        destination_folder: str
            The destination sub-folder, relative to ${HOME}.
            If this doesnt exist, it is created.



        when prompted, please supply:

        username: str
            The NASA EarthData username
        password: str
            The NASA EarthData password
        ''' 
        self.dest_path = Path.home().joinpath(destination_folder)
        p = self.dest_path.joinpath('.cylog.npz')
        if (init == False) and p.exists():
            return 
        else:
            self._setup(destination_folder=destination_folder)

    def _setup(self,destination_folder='.cylog'):
        username = input("Enter your username: ")  
        password = getpass()
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_user = cipher_suite.encrypt((username.encode()))
        ciphered_pass = cipher_suite.encrypt((password.encode()))
        data = {'key':key, 'ciphered_user':ciphered_user,\
                                   'ciphered_pass':ciphered_pass}
        self.dest_path = Path.home().joinpath(destination_folder)
        if not self.dest_path.exists():
            self.dest_path.mkdir()
        self.dest_path.chmod(0o700)
        p = self.dest_path.joinpath('.cylog.npz')
        np.savez(p,**data)
        p.chmod(0o600)

    def login(self):
        '''
        Reads encrypted information from ~/{dest_path}/.cylog.npz

        Returns
        --------
        A tuple containing plain text (username,password)

        '''
        data = np.load(self.dest_path.joinpath('.cylog.npz'))
        return (Fernet(data['key']).decrypt(np.atleast_1d(data['ciphered_user'])[0]),\
                Fernet(data['key']).decrypt(np.atleast_1d(data['ciphered_pass'])[0]))


