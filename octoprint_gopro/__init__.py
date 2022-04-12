# coding=utf-8
##################################################################################
# OctoPrint-GoPro - An OctoPrint Plugin that enables the use of a GoPro camera for timelapses
# Copyright (C) 2022  Lucas Wiseby
##################################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see the following:
# https://github.com/wiseby/OctoPrint-Gopro/main/LICENSE.txt
#
# You can contact the author either through the git-hub repository, or at the
# following email address: l.wiseby@gmail.com
##################################################################################

from __future__ import absolute_import

import flask
import asyncio
import octoprint.plugin
from octoprint.events import Events
from octoprint.plugin.core import logging
from octoprint_gopro.camera import GoProCamera

class GoproPlugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.StartupPlugin,
                  octoprint.plugin.EventHandlerPlugin,
                  octoprint.plugin.SimpleApiPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.camera = None
        self._console_logger = logging.getLogger(
            "octoprint.plugins.gopro.console"
        )

    ##~~ SettingsPlugin mixin

    def on_startup(self, host, port):
        self.camera = GoProCamera(self._console_logger)

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/gopro.js"],
            "css": ["css/gopro.css"],
            "less": ["less/gopro.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "gopro": {
                "displayName": "Gopro Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "wiseby",
                "repo": "OctoPrint-Gopro",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/wiseby/OctoPrint-Gopro/archive/{target_version}.zip",
            }
        }

    ##~~ SimpleApiPlugin mixin

    def get_api_commands(self):
        return dict(
            configure=['identifier', 'settings'],
            connect=['identifier']
        )

    def on_api_command(self, command, data):
        if command == 'configure':
            return flask.jsonify(dict(success=True, msg='Configured device with identifier ' + command['identifier']))
        if command == 'connect':
            self._console_logger.info('connecting to gopro...')
            self.camera.connect_ble()
            return flask.jsonify(dict(success=True, msg=str('Connection has been made')))

        else:
            return flask.jsonify(dict(success=False, msg=str('Missing operation')))


    def on_api_get(self, request):
        return super().on_api_get(request)

    ##~~ EventHandlerPlugin mixin

    def on_event(self, event, payload):
        if (event == Events.PRINT_STARTED):
            asyncio.run_coroutine_threadsafe(self.camera.connect_ble())
            asyncio.run_coroutine_threadsafe(self.camera.configure_photo_mode())
        if (event == Events.CAPTURE_START):
            self.camera.snap_photo()


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Gopro Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3.6,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = GoproPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
