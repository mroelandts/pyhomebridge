#!/usr/bin/env python3

import re
import requests
import sys
import json
import logging
import argparse

from typing import Dict, List, Optional, Tuple
from homebridge import HomeBridgeController, UnknownAccessory, InvalidAuthorization


def setup_logger(logger_name: str, create_new: bool = False, terminal: bool = True, logging_level=logging.INFO) -> logging.Logger:
    # create logger
    new_logger = None
    if create_new:
        new_logger = logger_name
    created_logger = logging.getLogger(new_logger)
    created_logger.setLevel(logging_level)
    log_formatter = logging.Formatter("%(asctime)s [%(module)-10.10s][%(levelname)-5.5s]: %(message)s")

    # file handler
    file_handler = logging.FileHandler("{0}/{1}.log".format('/tmp', logger_name))
    file_handler.setFormatter(log_formatter)
    created_logger.addHandler(file_handler)

    # console handler
    if terminal:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        created_logger.addHandler(console_handler)

    return created_logger


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Homebridge controller')
    parser.add_argument('-s', '--server', dest='server', type=str, action='store', help='specify the homebridge server')
    parser.add_argument('-p', '--port', dest='port', type=str, action='store', help='specify the homebridge port')
    parser.add_argument('-a', '--auth', dest='auth', type=str, action='store', help='specify the homebridge authorization code')
    parser.add_argument('-l', '--list', action='store_true', help='list all accessories in HomeBridge')
    parser.add_argument('-d', '--debug', action='store_true', help='activate debugging')
    parser.add_argument('-n', '--name', dest='name', type=str, action='store', help='specify the name of the accessory')
    parser.add_argument('--on', action='store_true', help='turn the accessory on')
    parser.add_argument('--off', action='store_true', help='turn the accessory off')
    parser.add_argument('--toggle', action='store_true', help='toogle the accessory')
    args = parser.parse_args()

    # read config file
    main_host = args.server
    main_port = args.port
    main_auth = args.auth
    if main_host is None:
        main_host ='raspberry-mini.local'
    if main_port is None:
        main_port = '51264'
    if main_auth is None:
        main_auth = '797-51-414'

    # create controller
    controller = HomeBridgeController(host=main_host, port=main_port, auth=main_auth, debug=args.debug)
    if args.list:
        controller.print_accessories()
        sys.exit(0)
    if args.name:
        if controller.accessory_exists(args.name) is False:
            print("Name '{}' does not exists!".format(args.name))
            sys.exit(1)
        if args.on or args.off or args.toggle:
            # set value on
            action_count = 0
            new_value = None
            if args.on:
                action_count += 1
                new_value = True
            if args.off:
                action_count += 1
                new_value = False
            if args.toggle:
                action_count += 1
                new_value = not controller.get_value(args.name)

            if action_count > 1:
                raise argparse.ArgumentError(None, message="You can only use one action! (on/off/toggle)")
            if new_value is not None:
                controller.set_value(args.name, new_value)
        else:
            # get value
            print(controller.get_value(args.name))

    sys.exit(0)
