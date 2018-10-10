from cryptography.fernet import Fernet
import numpy as np
from pathlib import Path
from getpass import getpass

class  cylog():

    def __init__(self,init=False,destination_folder='.cylog'):
        self.dest_path = Path.home().joinpath(destination_folder)
        p = self.dest_path.joinpath('.cylog.npz')
        if (init == False) and p.exists():
            return 
        else:
            self.setup(destination_folder=destination_folder)

    def setup(self,destination_folder='.cylog'):
        username = input("Enter your username: ")  
        password = getpass()
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_user = cipher_suite.encrypt((username.encode()))   #required to be bytes
        ciphered_pass = cipher_suite.encrypt((password.encode()))   #required to be bytes
        data = {'key':key, 'ciphered_user':ciphered_user,'ciphered_pass':ciphered_pass}
        self.dest_path = Path.home().joinpath(destination_folder)
        if not self.dest_path.exists():
            self.dest_path.mkdir()
        self.dest_path.chmod(0o700)
        p = self.dest_path.joinpath('.cylog.npz')
        np.savez(p,**data)
        p.chmod(0o600)

    def login(self):
        data = np.load(self.dest_path.joinpath('.cylog.npz'))
        return (Fernet(data['key']).decrypt(np.atleast_1d(data['ciphered_user'])[0]),\
                Fernet(data['key']).decrypt(np.atleast_1d(data['ciphered_pass'])[0]))


