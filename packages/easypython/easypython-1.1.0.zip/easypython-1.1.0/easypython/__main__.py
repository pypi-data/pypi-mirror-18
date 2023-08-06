#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import traceback

from easypython.utils.logger import Logger
from easypython.utils.args_parser import ArgsParser
from easypython.modules.run_module import RunModule


class EasyPython:
    def __init__(self, startfolder, argv):
        self.startfolder = startfolder
        self.argv = argv
        self.options, self.configs = ArgsParser(self.argv).parse_args()

        logs_path = "/var/log/easypython" if os.path.isdir("/var/log") else os.path.join(self.startfolder, "logs")
        is_debug = True if "debug" in self.configs else False

        self.logger = Logger(logs_path, is_debug)

        self.core_commands = {
            "run": RunModule
        }

    def start(self):
        command = "run"
        if len(self.options) > 1:
            command = self.options[1].lower()
            if command not in self.core_commands:
                command = "run"

        try:
            core_command_cls = self.core_commands[command](
                self.startfolder,
                self.configs,
                self.options,
                self.logger
            )

            core_command_cls.start()
        except KeyboardInterrupt:
            pass
        except:
            try:
                self.logger.debug(traceback.format_exc())
            except:
                pass

    def show_help(self):
        banner = """easypython [path]
"""
        self.logger.info(banner)


def run():
    startfolder = os.path.dirname(sys.executable)
    if sys.argv[0][-3:] == ".py":
        startfolder = os.path.dirname(os.path.realpath(sys.argv[0]))

    easypython = EasyPython(startfolder, sys.argv)
    easypython.start()

if __name__ == '__main__':
    run()
