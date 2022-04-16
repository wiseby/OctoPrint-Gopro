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

import asyncio
from binascii import hexlify
from octoprint_gopro.constants import *
import re
from bleak import BleakScanner, BleakClient

class GoProCamera:
    def __init__(self, logger):
        self.identifier = None
        self.logger = logger
        self.devices = {}
        self.client = None
        self.event = asyncio.Event()

    def notification_handler(self, handle, data):
        self.logger.info(f'Received response at {handle}: {hexlify(data, ":")!r}')

        # If this is the correct handle and the status is success, the command was a success
        if self.client.services.characteristics[handle].uuid == COMMAND_RSP_UUID and data[2] == 0x00:
            self.logger.info("Command sent successfully")
        elif self.client.services.characteristics[handle].uuid == SETTINGS_RSP_UUID and data[2] == 0x00:
            self.logger.info("Setting sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            self.logger.error("Unexpected response")

        # Notify the writer
        self.event.set()

    async def createClient(self):
        # Scan for devices
        self.logger.info("Scanning for bluetooth devices...")
        # Scan callback to also catch nonconnectable scan responses

        def _scan_callback(device, _) -> None:
            # Add to the dict if not unknown
            if device.name != "Unknown" and device.name is not None:
                devices[device.name] = device

        devices = {}

        # Scan until we find devices
        matched_devices = []
        while len(matched_devices) == 0:
            # Now get list of connectable advertisements
            for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
                if device.name != "Unknown" and device.name is not None:
                    self.devices[device.name] = device
            # Log every device we discovered
            for d in self.devices:
                self.logger.info(f"\tDiscovered: {d}")
            # Now look for our matching device(s)
            token = re.compile(
                r"GoPro [A-Z0-9]{4}" if self.identifier is None else f"GoPro {self.identifier}")
            matched_devices = [device for name,
                               device in self.devices.items() if token.match(name)]
            self.logger.info(f"Found {len(matched_devices)} matching devices.")

        # Connect to first matching Bluetooth device
        device = matched_devices[0]

        self.logger.info(f"Establishing BLE connection to {device}...")
        self.client = BleakClient(device)

    async def reset_connection(self):
        if self.client is not None:
            await self.client.disconnect()
        await self.connect_ble()

    async def connect_ble(self):
        if self.client is None:
            self.logger.info('Creating a new client')
            await self.createClient()


        self.logger.info('Connecting client...')
        await self.client.connect(timeout=15)
        self.logger.info("BLE Connected!")

        # Try to pair (on some OS's this will expectedly fail)
        self.logger.info("Attempting to pair...")
        try:
            await self.client.pair()
        except NotImplementedError:
            # This is expected on Mac
            pass
        self.logger.info("Pairing complete!")

        # Enable notifications on all notifiable characteristics
        self.logger.info("Enabling notifications...")
        for service in self.client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    self.logger.info(f"Enabling notification on char {char.uuid}")
                    await self.client.start_notify(char, self.notification_handler)
        self.logger.info("Done enabling notifications")

    async def configure_photo_mode(self):
        # Write to command request BleUUID adjust the settings
        self.logger.info("Changing to photo mode")
        self.event.clear()
        await self.client.write_gatt_char(COMMAND_REQ_UUID, bytearray(PHOTO_GROUP))
        await self.event.wait()  # Wait to receive the notification response
        self.event.clear()

    async def snap_photo(self):
        await self.client.write_gatt_char(COMMAND_REQ_UUID, bytearray(SHUTTER_ON)),
        await self.event.wait()
        self.event.clear()
