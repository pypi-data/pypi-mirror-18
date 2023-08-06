import sys
import logging
import logging.config
import os
import yaml
import socket

from pymongo import MongoClient
import requests
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from biomaj_user.user import BmajUser


class BiomajAuthorizer(DummyAuthorizer):

    def set_config(self, cfg):
        self.cfg = cfg
        self.mongo = MongoClient(self.cfg['mongo']['url'])
        self.db = self.mongo[self.cfg['mongo']['db']]
        self.bank = None

    def validate_authentication(self, username, apikey, handler):
        """Raises AuthenticationFailed if supplied username and
        password don't match the stored credentials, else return
        None.
        """
        msg = "Authentication failed."
        if apikey == 'anonymous':
            bank = self.db.banks.find_one({'name': username})
            if not bank:
                logging.error('Bank not found: ' + username)
                raise AuthenticationFailed('Bank does not exists')
            if bank['properties']['visibility'] != 'public':
                raise AuthenticationFailed('Not allowed to access to this bank')
            if len(bank['production']) == 0:
                raise AuthenticationFailed('No production release available')
            self.bank = bank
            return
        if apikey != 'anonymous':
            user = None
            if 'web' in self.cfg and 'local_endpoint' in self.cfg['web'] and self.cfg['web']['local_endpoint']:
                user_req =  requests.get(self.cfg['web']['local_endpoint'] + '/api/info/apikey/' + apikey)
                if not user_req.status_code == 200:
                    raise AuthenticationFailed('Wrong or failed authentication')
                user = user_req.json()
            else:
                user = BmajUser.get_user_by_apikey(apikey)

            bank = self.db.banks.find_one({'name': username})
            if not bank:
                logging.error('Bank not found: ' + username)
                raise AuthenticationFailed('Bank does not exists')
            if bank['properties']['visibility'] != 'public':
                if user['id'] != bank['properties']['owner']:
                    if 'members' not in bank['properties'] or user['id'] not in bank['properties']['members']:
                        raise AuthenticationFailed('Not allowed to access to this bank')

            if len(bank['production']) == 0:
                raise AuthenticationFailed('No production release available')
            self.bank = bank

    def get_home_dir(self, username):
        """Return the user's home directory.
        Since this is called during authentication (PASS),
        AuthenticationFailed can be freely raised by subclasses in case
        the provided username no longer exists.
        """
        bank = self.bank
        last = bank['production'][0]
        if bank['current']:
            for prod in bank['production']:
                if prod['session'] == bank['current']:
                    last = prod
                    break
        home_dir = os.path.join(last['data_dir'], last['dir_version'])
        if sys.version_info.major == 2:
            home_dir = home_dir.encode('utf-8')
        return home_dir

    def get_msg_login(self, username):
        """Return the user's login message."""
        return 'Welcome to BioMAJ FTP'

    def get_msg_quit(self, username):
        """Return the user's quitting message."""
        return 'Bye'

    def has_perm(self, username, perm, path=None):
        """Whether the user has permission over path (an absolute
        pathname of a file or a directory).
        Expected perm argument is one of the following letters:
        "elradfmwM".
        """
        user_perms = ['e', 'l', 'r']
        if perm in user_perms:
            return True
        return False

    def get_perms(self, username):
        """Return current user permissions."""
        return 'elr'

    def override_perm(self, username, directory, perm, recursive=False):
        return


class BiomajFTP(object):

    def __init__(self):
        config_file = 'config.yml'
        if 'BIOMAJ_CONFIG' in os.environ:
            config_file = os.environ['BIOMAJ_CONFIG']
        self.cfg = None
        with open(config_file, 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)

        if self.cfg['log_config'] is not None:
            for handler in list(self.cfg['log_config']['handlers'].keys()):
                self.cfg['log_config']['handlers'][handler] = dict(self.cfg['log_config']['handlers'][handler])
            logging.config.dictConfig(self.cfg['log_config'])
        self.logger = logging.getLogger('biomaj')

        BmajUser.set_config(self.cfg)

        authorizer = BiomajAuthorizer()
        authorizer.set_config(self.cfg)

        self.handler = FTPHandler
        self.handler.authorizer = authorizer

    def start(self):
        server = FTPServer((self.cfg['ftp']['listen'], self.cfg['ftp']['port']), self.handler)
        server.serve_forever()


ftp_handler = BiomajFTP()
ftp_handler.start()
