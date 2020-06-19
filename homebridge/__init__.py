#!/usr/bin/env python3

# HomeBridgeController can control homebridge accessories
# Created by Matthias Roelandts, 2020
# https://github.com/mroelandts/pyhomebridge
# License: MIT

import re
import requests
import json
import logging

from typing import Dict, Tuple, List

__version__ = "0.0.3"


class HomeBridgeException(Exception):
    def __init__(self, *args):
        if args:
            self._message = args[0]
        else:
            self._message = None

    def __str__(self):
        if self._message:
            return str(self._message)
        else:
            return "A HomeBridgeException has been raised!"


class UnknownAccessoryError(HomeBridgeException):
    pass


class InvalidAuthorization(HomeBridgeException):
    pass


class HomeBridgeController:
    def __init__(self, host: str, port: int, auth: str, debug: bool = False):
        # homebridge info
        self._hostname = host
        self._port = port
        self._auth = auth
        if re.match(r'\d{3}-\d{2}-\d{3}', self._auth) is None:
            raise InvalidAuthorization("'{}' does not match a correct authorization code!".format(self._auth))
        self._base_url = 'http://{}:{}'.format(self._hostname, self._port)
        self._headers = {'Content-Type': 'Application/json', 'authorization': self._auth}

        # accessories info
        self._accessories = {}

        # setup logger
        logging_level = logging.INFO
        if debug:
            logging_level = logging.DEBUG
        created_logger = logging.getLogger('hombridge')
        created_logger.setLevel(logging_level)

        # load accessories
        if self._get_accessories() is False:
            raise HomeBridgeException("Failed to initialise HomeBridgeController!")

    @property
    def accessories(self) -> List[str]:
        return list(self._accessories.keys())

    def _get_accessories(self) -> bool:
        logging.debug('GETTING accessories of {}'.format(self._base_url))
        try:
            get_response = requests.get('{}/accessories'.format(self._base_url), headers=self._headers)
        except requests.exceptions.ConnectionError as err:
            logging.error(err)
            return False
        if get_response.status_code != 200:
            logging.error('GET accessories response: {}'.format(get_response.status_code))
        for accessory in get_response.json()['accessories']:
            a_name, a_info = self._get_info_of_accessory(accessory)
            if a_info['iid'] is not None:
                self._accessories[a_name] = a_info
        return True

    @staticmethod
    def _get_info_of_accessory(accessory_dict: Dict) -> Tuple[str, Dict]:
        a_id = accessory_dict['aid']
        a_name = None
        a_manufacturer = None
        a_iid = None
        a_type = None
        a_value = None
        a_active = None
        for service_info in accessory_dict['services']:
            for characteristic_info in service_info['characteristics']:
                if characteristic_info['description'] == 'Name':
                    if a_name is not None and a_name != characteristic_info['value']:
                        logging.warning("Found new name for {}! '{}' vs '{}'".format(a_id, a_name,
                                                                                     characteristic_info['value']))
                    else:
                        a_name = characteristic_info['value']
                if characteristic_info['description'] == 'Manufacturer':
                    if a_manufacturer is not None and a_manufacturer != characteristic_info['value']:
                        logging.warning("Found new manufacturer for {}! '{}' vs '{}'".format(a_id, a_manufacturer,
                                                                                             characteristic_info[
                                                                                                 'value']))
                    else:
                        a_manufacturer = characteristic_info['value']
                if characteristic_info['description'] == 'On':
                    if a_value is not None and a_value[1] != characteristic_info['value']:
                        logging.warning("Found new value(On) for {}! '{}' vs '{}'".format(a_id, a_value[1],
                                                                                          characteristic_info[
                                                                                              'value']))
                    else:

                        a_value = (characteristic_info['iid'], characteristic_info['value'],
                                   characteristic_info['format'])
                if characteristic_info['description'] == 'Model':
                    if a_type is not None and a_type != characteristic_info['value']:
                        logging.warning("Found new type for {}! '{}' vs '{}'".format(a_id, a_type,
                                                                                     characteristic_info['value']))
                    else:
                        a_type = characteristic_info['value']
                if characteristic_info['description'] == 'Active':
                    if a_active is not None and a_active[1] != characteristic_info['value']:
                        logging.warning("Found new active for {}! '{}' vs '{}'".format(a_id, a_active[1],
                                                                                       characteristic_info['value']))
                    else:
                        a_active = (characteristic_info['iid'], characteristic_info['value'],
                                    characteristic_info['format'])

        if a_name is None:
            a_name = a_manufacturer
        if a_value is None:
            a_value = a_active
        if a_value is not None:
            a_iid = a_value[0]
            a_value = a_value[1]
        return a_name, {'aid': a_id, 'iid': a_iid, 'type': a_type, 'value': a_value}

    def accessory_exists(self, accessory_name: str, refresh: bool = False) -> bool:
        # refresh accessories
        if refresh:
            if self._get_accessories() is False:
                raise HomeBridgeException("Failed to refresh accessories!")

        # get accessry
        if self._accessories.get(accessory_name, None) is None:
            logging.warning("Name '{}' does not exists in homebridge.".format(accessory_name))
            return False
        else:
            return True

    def get_value(self, accessory_name: str, refresh: bool = False):
        logging.debug('GET {}'.format(accessory_name))
        # refresh accessories
        if refresh:
            if self._get_accessories() is False:
                raise HomeBridgeException("Failed to refresh accessories!")

        # get value
        accessory_info = self._accessories.get(accessory_name, None)
        if accessory_info is None:
            raise UnknownAccessoryError("{} has not been found".format(accessory_name))
        return accessory_info.get('value', None)

    def set_value(self, accessory_name: str, value: bool) -> bool:
        logging.debug('SET {} to {}'.format(accessory_name, value))

        # get accessory
        accessory_info = self._accessories.get(accessory_name, None)
        if accessory_info is None:
            raise UnknownAccessoryError("{} has not been found".format(accessory_name))

        # setting value
        put_response = requests.put('{}/characteristics'.format(self._base_url), headers=self._headers,
                                    data=json.dumps({"characteristics": [{'aid': accessory_info['aid'],
                                                                          'iid': accessory_info['iid'],
                                                                          'value': value, "status": 0}]}))
        if put_response.status_code != 204:
            logging.error('PUT characteristics response: {}'.format(put_response.status_code))
            return False
        return True

    def print_accessories(self, enable_json: bool = False):
        if enable_json:
            print(json.dumps(self._accessories))
            return
        for key in self._accessories:
            accessory = self._accessories[key]
            print('* {}.{}'.format(accessory['aid'], accessory['iid']))
            print('  Name: {}'.format(key))
            print('  Type: {}'.format(accessory['type']))
            print('  Value: {}'.format(accessory['value']))
