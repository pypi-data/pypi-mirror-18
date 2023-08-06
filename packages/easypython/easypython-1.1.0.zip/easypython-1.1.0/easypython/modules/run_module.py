#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import traceback
import zipfile
import requests
import webbrowser

from easypython.core import Core
from easypython.utils.logger import Logger
from easypython.utils.functions import zipdir


class RunModule(Core):
    def __init__(self, startfolder, configs, options, logger):
        Core.__init__(self, startfolder, configs, options, logger)

        self.folder = options[1] if len(options) > 1 else None

    def start(self):
        if self.folder is None:
            try:
                self.folder = input("please input sources folder: ")
            except:
                self.folder = raw_input("please input sources folder: ")

        if not os.path.isdir(self.folder):
            self.logger.error(u"please input sources folder")
            return

        manage_path = os.path.join(self.folder, "manage.py")
        if not os.path.isfile(manage_path):
            self.logger.error("invalid folder")
            return

        username, token, domain, port = self.login()
        target = os.path.join(self.startfolder, "%s.zip" % (token))

        if not zipdir(self.folder, target):
            self.logger.error("zip failed")
            return

        if not os.path.isfile(target):
            sel.logger.error("zip failed")
            return

        try:
            if not self.upload(username, token, target):
                self.logger.error("upload failed")
                return

            if not domain:
                domain = "%s:%s" % (self.easypython_host, port)
            self.logger.info("[%s] successfully! " % domain)
            webbrowser.open(domain)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)

    def login(self):
        try:
            username = input("please input your username: ")
            password = input("please input your password: ")
        except:
            username = raw_input("please input your username: ")
            password = raw_input("please input your password: ")
        url = "%s/login/" % self.easypython_host 
        params = {
            "username": username,
            "password": password
        }
        r = requests.post(url, data=params)
        if r.status_code != 200:
            self.logger.error(r.text)
            return

        json = r.json()
        return json["username"], json["token"], json["domain"], json["port"]

    def upload(self, username, token, zippath):
        try:
            url = "%s/upload/" % self.easypython_host 
            params = {
                "username": username,
                "token": token
            }
            r = requests.post(url, data=params, files={"file": open(zippath, "rb")})
            if r.status_code != 200:
                self.logger.error(r.text)
                return False

            return True
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)

        return False


