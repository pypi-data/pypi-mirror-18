import sys
import logging
import logging.config
import os
import yaml

import consul
from pymongo import MongoClient
import requests
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from biomaj_user.user import BmajUser
from biomaj_core.utils import Utils
from biomaj_core.config import BiomajConfig



class BiomajAuthorizer(DummyAuthorizer):

    def set_config(self, cfg):
        self.cfg = cfg
        self.mongo = MongoClient(BiomajConfig.global_config.get('GENERAL', 'db.url'))
        self.db = self.mongo[BiomajConfig.global_config.get('GENERAL', 'db.name')]
        self.bank = None
        self.logger = logging

    def set_logger(self, logger):
        self.logger = logger

    def validate_authentication(self, username, apikey, handler):
        """Raises AuthenticationFailed if supplied username and
        password don't match the stored credentials, else return
        None.
        """
        # msg = "Authentication failed."
        if apikey == 'anonymous':
            bank = self.db.banks.find_one({'name': username})
            if not bank:
                self.logger.error('Bank not found: ' + username)
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
                user_req = requests.get(self.cfg['web']['local_endpoint'] + '/api/user/info/apikey/' + apikey)
                if not user_req.status_code == 200:
                    raise AuthenticationFailed('Wrong or failed authentication')
                user = user_req.json()
            else:
                user = BmajUser.get_user_by_apikey(apikey)

            bank = self.db.banks.find_one({'name': username})
            if not bank:
                self.logger.error('Bank not found: ' + username)
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
            Utils.service_config_override(self.cfg)

        # There is an issue with tcp checks, see https://github.com/cablehead/python-consul/issues/136
        '''
        if self.cfg['consul']['host']:
            consul_agent = consul.Consul(host=self.cfg['consul']['host'])
            consul_agent.agent.service.register('biomaj-ftp',
                service_id=self.cfg['consul']['id'],
                address=self.cfg['consul']['id'],
                port=self.cfg['ftp']['port'],
                tags=['biomaj'])
            check = consul.Check.tcp(host= self.cfg['consul']['id'],
                port=self.cfg['ftp']['port'],
                interval=20)
            consul_agent.agent.check.register(self.cfg['consul']['id'] + '_check',
                check=check,
                service_id=self.cfg['consul']['id'])
        '''

        if self.cfg['log_config'] is not None:
            for handler in list(self.cfg['log_config']['handlers'].keys()):
                self.cfg['log_config']['handlers'][handler] = dict(self.cfg['log_config']['handlers'][handler])
            logging.config.dictConfig(self.cfg['log_config'])
        self.logger = logging.getLogger('biomaj')

        BiomajConfig.load_config(self.cfg['biomaj']['config'])

        BmajUser.set_config(self.cfg)

        authorizer = BiomajAuthorizer()
        authorizer.set_config(self.cfg)
        authorizer.set_logger(self.logger)

        self.handler = FTPHandler
        self.handler.authorizer = authorizer

    def start(self):
        server = FTPServer((self.cfg['ftp']['listen'], self.cfg['ftp']['port']), self.handler)
        server.serve_forever()


ftp_handler = BiomajFTP()
ftp_handler.start()
