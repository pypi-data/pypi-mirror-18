#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Purpose:
        Module configuration methods
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@nycresistor.com'
__copyright__ = 'Copyright 2016, Symphony Communication Services LLC'

import configparser
import getopt
import logging
import sys
import symphony


class Config:

    def __init__(self, config):
        ''' command line argument parsing '''
        opts, args = getopt.getopt(sys.argv[1:], 'hc:t:vV')
        self.opts = dict(opts)
        self.args = args
        self.__config__ = config

    def connect(self):
        ''' instantiate objects / parse config file '''
        # open config file for parsing
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        try:
            settings.read(self.__config__)
        except Exception, err:
            print 'config file not readable: %s' % err
            sys.exit(2)

        # Connect to Symphony
        symphony_p12 = settings.get('symphony', 'symphony_p12')
        symphony_pwd = settings.get('symphony', 'symphony_pwd')
        symphony_uri = settings.get('symphony', 'symphony_uri')
        symphony_sid = settings.get('symphony', 'symphony_sid')
        crypt = symphony.Crypt(symphony_p12, symphony_pwd)
        symphony_crt, symphony_key = crypt.p12parse()

        try:
            # instantiate auth methods
            auth = symphony.Auth(symphony_uri, symphony_crt, symphony_key)
            # get session token
            session_token = auth.get_session_token()
            logging.info("AUTH ( session token ): %s" % session_token)
            # get keymanager token
            keymngr_token = auth.get_keymanager_token()
            logging.info("AUTH ( key manager token ): %s" % keymngr_token)
            # instantiate agent methods
            agent = symphony.Agent(symphony_uri, symphony_crt, symphony_key, session_token, keymngr_token)
            logging.info("INSTANTIATION ( all objects successful)")
        except Exception, err:
            logging.error("Failed to authenticate and initialize: %s" % err)
            return 'you', 'have', 'failed'
        # return references and such
        return agent, symphony_sid
