#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import tempfile

from . import EASYPYTHON_VERSION, EASYPYTHON_HOST
from easypython.utils.config_parser import ConfigParser


class Core():
    def __init__(self, startfolder, configs, options, logger):
        self.startfolder = startfolder
        self.configs = configs
        self.options = options
        self.logger = logger

        self.easypython_version = EASYPYTHON_VERSION

        self.easypython_host = EASYPYTHON_HOST

        if "http://" not in self.easypython_host and "https://" not in self.easypython_host:
            self.easypython_host = "http://%s" % self.easypython_host

        if self.easypython_host[-1] == "/":
            self.easypython_host = self.easypython_host[:-1]

        self.easypython_tmps_path = os.path.join(tempfile.gettempdir(), "easypython")
        self.easypython_settings_path = os.getenv("EASYPYTHON_SETTINGS_PATH")

        if self.easypython_settings_path is None:
            settings_path = os.path.join(self.startfolder, "settings")
            if not os.path.isdir(settings_path):
                if os.getenv("APPDATA") is None:
                    if os.path.isdir("/etc/opt"):
                        self.easypython_settings_path = "/etc/opt/easypython"
                    else:
                        self.easypython_settings_path = os.path.join(self.easypython_tmps_path, "settings")
                else:
                    self.easypython_settings_path = os.path.join(os.getenv("APPDATA"), "easypython", "settings")
            else:
                self.easypython_settings_path = settings_path

        self.configs = dict(self.get_setting(), **self.configs)

    def get_setting(self, key=None):
        ini_path = os.path.join(self.easypython_settings_path, "easypython.ini")
        if not os.path.isfile(ini_path):
            return {}

        cf = ConfigParser(ini_path)

        if key is None:
            return cf.get()
        return cf

    def set_setting(self, key, value):
        ini_path = os.path.join(self.easypython_settings_path, "easypython.ini")
        if not os.path.isdir(self.easypython_settings_path):
            os.makedirs(self.easypython_settings_path)

        cf = ConfigParser(ini_path)
        cf.set("default", key, value)
        cf.write(ini_path)
