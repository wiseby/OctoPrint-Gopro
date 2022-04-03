import asyncio
import logging
from binascii import hexlify

from constants import *
import re
import json
import logging
from typing import Dict, Any, List, Callable
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class GoProCamera:
    def __init__(self) -> None:
        self.identifier = None
        self.devices: Dict[str, BleakDevice] = {}
        self.client: BleakClient
        self.event = asyncio.Event()

    def notification_handler(self, handle: int, data: bytes) -> None:
        logger.info(f'Received response at {handle=}: {hexlify(data, ":")!r}')

        # If this is the correct handle and the status is success, the command was a success
        if self.client.services.characteristics[handle].uuid == COMMAND_RSP_UUID and data[2] == 0x00:
            logger.info("Command sent successfully")
        elif self.client.services.characteristics[handle].uuid == SETTINGS_RSP_UUID and data[2] == 0x00:
            logger.info("Setting sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        self.event.set()

    async def initialize(self):
        logger.info("connecting client")
        await self.connect_ble(self.notification_handler)

    async def connect_ble(
        self, notification_handler: Callable[[int, bytes], None]
    ):
        # Scan for devices
        logger.info("Scanning for bluetooth devices...")
        # Scan callback to also catch nonconnectable scan responses

        def _scan_callback(device: BleakDevice, _: Any) -> None:
            # Add to the dict if not unknown
            if device.name != "Unknown" and device.name is not None:
                devices[device.name] = device

        devices: Dict[str, BleakDevice] = {}

        # Scan until we find devices
        matched_devices: List[BleakDevice] = []
        while len(matched_devices) == 0:
            # Now get list of connectable advertisements
            for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
                if device.name != "Unknown" and device.name is not None:
                    self.devices[device.name] = device
            # Log every device we discovered
            for d in self.devices:
                logger.info(f"\tDiscovered: {d}")
            # Now look for our matching device(s)
            token = re.compile(
                r"GoPro [A-Z0-9]{4}" if self.identifier is None else f"GoPro {self.identifier}")
            matched_devices = [device for name,
                               device in self.devices.items() if token.match(name)]
            logger.info(f"Found {len(matched_devices)} matching devices.")

        # Connect to first matching Bluetooth device
        device = matched_devices[0]

        logger.info(f"Establishing BLE connection to {device}...")
        self.client = BleakClient(device)
        await self.client.connect(timeout=15)
        logger.info("BLE Connected!")

        # Try to pair (on some OS's this will expectedly fail)
        logger.info("Attempting to pair...")
        try:
            await self.client.pair()
        except NotImplementedError:
            # This is expected on Mac
            pass
        logger.info("Pairing complete!")

        # Enable notifications on all notifiable characteristics
        logger.info("Enabling notifications...")
        for service in self.client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    logger.info(f"Enabling notification on char {char.uuid}")
                    await self.client.start_notify(char, notification_handler)
        logger.info("Done enabling notifications")

    async def configure_photo_mode(self):
        # Write to command request BleUUID adjust the settings
        logger.info("Changing to photo mode")
        self.event.clear()
        await self.client.write_gatt_char(COMMAND_REQ_UUID, bytearray(PHOTO_GROUP))
        await self.event.wait()  # Wait to receive the notification response

        logger.info("Changing to 4k resolution")
        self.event.clear()
        await self.client.write_gatt_char(SETTINGS_REQ_UUID, bytearray(RES4K))
        await self.event.wait()  # Wait to receive the notification response

    async def snap_photo(self):
        # Write to command request BleUUID adjust the settings
        logger.info("Taking a shoot")
        self.event.clear()
        await self.client.write_gatt_char(COMMAND_REQ_UUID, bytearray(SHUTTER_ON))
        await self.event.wait()  # Wait to receive the notification response

    async def disconnect_wifi(self):
        self.event.clear()
        if self.wifi.disconnect():
            logger.info("Wifi Disconnected!")

    def get_media_list(self):
        # Build the HTTP GET request
        url = MEDIA_LIST_URL

        logger.info(f"Getting the media list: sending {url}")
        response = requests.get(url, timeout=10, stream=False);
        # Check for errors (if an error is found, an exception will be raised)
        logger.info("Command sent successfully")
        raw_data = response.content.decode()
        parsed_data = json.loads(raw_data)
        for dir in parsed_data["media"]:
            for file in dir["fs"]:
                logger.info(f"{dir['d']}/{file['n']}")

        # Log response as json
        logger.info(f"Response: {json.dumps(response.json(), indent=2)}")
