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

# UUIDs to write to and receive responses from
GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"
GOPRO_BASE_URL = "http://10.5.5.9:8080"

COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format("0074")
SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format("0075")

WIFI_AP_SSID_UUID = GOPRO_BASE_UUID.format("0002")
WIFI_AP_PASSWORD_UUID = GOPRO_BASE_UUID.format("0003")

# Capture Groups:
VIDEO_GROUP = [0x04, 0x3E, 0x02, 0x03, 0xE8]
PHOTO_GROUP = [0x04, 0x3E, 0x02, 0x03, 0xE9]
TIMELAPSE_GROUP = [0x04, 0x3E, 0x02, 0x03, 0xEA]

# Presets:
CINEMATIC = [0x06, 0x40, 0x04, 0x00, 0x00, 0x00, 0x02]
SLO_MO = [0x06, 0x40, 0x04, 0x00, 0x00, 0x00, 0x03]
BURST_PHOTO = [0x06, 0x40, 0x04, 0x00, 0x01, 0x00, 0x02]
NIGHT_PHOTO = [0x06, 0x40, 0x04, 0x00, 0x00, 0x00, 0x03]

# Commands:
SHUTTER_OFF = [0x03, 0x01, 0x01, 0x00]
SHUTTER_ON = [0x03, 0x01, 0x01, 0x01]
SLEEP = [0x01, 0x05]

# FPS:
FPS24 = [0x03, 0x03, 0x01, 0x0A]
FPS60 = [0x03, 0x03, 0x01, 0x05]
FPS240 = [0x03, 0x03, 0x01, 0x00]

# Resolutions:
RES1080 = [0x03, 0x02, 0x01, 0x09]
RES27K = [0x03, 0x02, 0x01, 0x04]
RES4K = [0x03, 0x02, 0x01, 0x18]

# Wifi:
ENABLE_WIFI_AP = [0x03, 0x17, 0x01, 0x01]
MEDIA_LIST_URL = GOPRO_BASE_URL + "/gp/gpMediaList"
CONTROL_URL = GOPRO_BASE_URL + "/gp/gpControl"
CONTROL_STATUS_URL = GOPRO_BASE_URL + "gp/gpControl/status"
SETTINGS_URL = GOPRO_BASE_URL + "gp/gpControl/setting"
COMMAND_URL = GOPRO_BASE_URL + "gp/gpControl/command/"
EXECUTE_URL = GOPRO_BASE_URL + "gp/gpControl/execute?"
WEBCAM_URL = GOPRO_BASE_URL + "gp/gpWebcam/"
TURBO_URL = GOPRO_BASE_URL + "gp/gpTurbo"

# Wifi Params:
DELETE_ALL = "DA"
DELETE_ALL = "DA"


# Misc:
ENABLE_ANALYTICS = [0x01, 0x50]
