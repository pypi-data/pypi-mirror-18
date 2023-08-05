#!/usr/bin/env python
#
# core: core nebulizer classes and functions

import os
import re
import fnmatch
import logging
from bioblend import galaxy
from bioblend.galaxy.client import ConnectionError

class Credentials:
    """Class for managing credentials for Galaxy instances

    Credentials for different galaxy instances can be
    stored in a file under $HOME/.nebulizer

    Entries in the file consist of lines with three tab
    separated values:

    ALIAS   URL    API_KEY

    Blank lines or lines starting '#' are skipped.

    """

    def __init__(self,key_file=None):
        """
        Create a new Credentials instance

        Arguments:
          key_file (str): if supplied then should specify
            the path to the credentials file (defaults to
            $HOME/.nebulizer)

        """
        if key_file is None:
            key_file = os.path.join(os.path.expanduser("~"),
                                    '.nebulizer')
        self._key_file = os.path.abspath(key_file)

    def list_keys(self):
        """
        List aliases for API keys stored in credentials file

        Returns:
          List: list of aliases.

        """
        key_names = []
        if os.path.exists(self._key_file):
            with open(self._key_file,'r') as fp:
                for line in fp:
                    if line.startswith('#') or not line.strip():
                        continue
                    key_names.append(line.strip().split('\t')[0])
        return key_names

    def store_key(self,name,url,api_key):
        """
        Store a Galaxy API key

        Appends an entry to the key file.

        Arguments:
          name (str): alias to store the key against
          url (str): URL of the Galaxy instance
          api_key (str): API key for the Galaxy instance 

        """
        with open(self._key_file,'a') as fp:
            fp.write("%s\t%s\t%s\n" % (name,url,api_key))

    def remove_key(self,name):
        """
        Remove a Galaxy API key

        Removes a key entry from the key file.

        Arguments:
          name (str) alias of the key to be removed

        """
        key_names = self.list_keys()
        if name not in key_names:
            logging.error("'%s': not found" % name)
            return
        # Store the keys
        cached_keys = {
            name: list(self.fetch_key(name))
            for name in key_names
        }
        # Wipe the key file
        with open(self._key_file,'w') as fp:
            fp.write("#.nebulizer\n#Aliases\tGalaxy URL\tAPI key\n")
        # Store the cached keys again
        for alias in key_names:
            if name != alias:
                url,api_key = cached_keys[alias]
                self.store_key(alias,url,api_key)

    def update_key(self,name,new_url=None,new_api_key=None):
        """
        Update a Galaxy API key

        Updates the stored information in the key file.

        Arguments:
          name (str): alias of the key entry to be updated
          new_url (str): optional, new URL for the Galaxy
            instance
          new_api_key (str): optional, new API key for the
            Galaxy instance
        
        """
        try:
            url,api_key = self.fetch_key(name)
        except KeyError:
            logging.error("'%s': not found" % name)
            return
        if new_url:
            url = new_url
        if new_api_key:
            api_key = new_api_key
        self.remove_key(name)
        self.store_key(name,url,api_key)

    def fetch_key(self,name):
        """
        Fetch credentials associated with a Galaxy instance

        Returns the credentials (i.e. Galaxy URL and API key)
        associated with the specified alias

        Raises a KeyError if no entry matching the alias is
        found.

        Arguments:
          name (str): alias of the key entry to fetch

        Returns:
          Tuple: consisting of (GALAXY_URL,API_KEY)

        """
        if os.path.exists(self._key_file):
            with open(self._key_file,'r') as fp:
                for line in fp:
                    if line.startswith('#') or not line.strip():
                        continue
                    alias,url,api_key = line.strip().split('\t')
                    if alias == name or url == name:
                        return (url,api_key)
        raise KeyError("'%s': not found" % name)

def get_galaxy_instance(galaxy_url,api_key=None,email=None,password=None,
                        verify=True):
    """
    Return Bioblend GalaxyInstance

    Attempts to connect to the specified Galaxy instance and
    verify that the connection is working by requesting the
    config for that instance.

    Arguments:
      galaxy_url (str): URL for the Galaxy instance to connect to
      api_key (str): API key to use when accessing Galaxy
      email (str): Galaxy e-mail address corresponding to the user
        (alternative to api_key; also need to supply a password)
      password (str): password of Galaxy account corresponding to
        email address (alternative to api_key)
      verify (bool): if True then turn off verification of SSL
        certificates for HTTPs connections

    Returns:
      GalaxyInstance: a bioblend GalaxyInstance for the connection,
        or None if the connection failed or couldn't be verified.

    """
    try:
        galaxy_url,stored_key = Credentials().fetch_key(galaxy_url)
    except KeyError,ex:
        logging.warning("Failed to find credentials for %s" %
                        galaxy_url)
        stored_key = None
    if api_key is None:
        api_key = stored_key
    print "## Connecting to %s" % galaxy_url
    if email is not None:
        gi = galaxy.GalaxyInstance(url=galaxy_url,email=email,
                                   password=password)
    else:
        gi = galaxy.GalaxyInstance(url=galaxy_url,key=api_key)
    gi.verify = verify
    try:
        galaxy.config.ConfigClient(gi).get_config()
    except ConnectionError,ex:
        print ex
        return None
    try:
        user = galaxy.users.UserClient(gi).get_current_user()
        print "## Connected as user %s" % user['email']
    except ConnectionError:
        print "## Unable to determine associated user"
    return gi

def turn_off_urllib3_warnings():
    """
    Turn off the warnings from urllib3

    Use this to suppress warnings (e.g. about unverified HTTPS
    certificates) that would otherwise be written out for each
    request in bioblend.

    """
    import requests
    requests.packages.urllib3.disable_warnings()
