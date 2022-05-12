import logging
import asyncio
import threading
import struct
import globals

from typing import Any, Dict
from bless import (BlessServer, BlessGATTCharacteristic, GATTCharacteristicProperties, GATTAttributePermissions)


class Server(threading.Thread):
    server: BlessServer
    gatt: Dict = {
        "0000181A-0000-1000-8000-00805F9B34FB": {
            globals.gatt[0]: {
                "Properties": (GATTCharacteristicProperties.read |
                               GATTCharacteristicProperties.indicate),
                "Permissions": GATTAttributePermissions.readable,
                "Value": bytearray(struct.pack("f", 0))
            },
            globals.gatt[1]: {
                "Properties": (GATTCharacteristicProperties.read |
                               GATTCharacteristicProperties.indicate),
                "Permissions": GATTAttributePermissions.readable,
                "Value": bytearray(struct.pack("f", 0))
            },
            globals.gatt[2]: {
                "Properties": (GATTCharacteristicProperties.read |
                               GATTCharacteristicProperties.indicate),
                "Permissions": GATTAttributePermissions.readable,
                "Value": bytearray(struct.pack("f", 0))
            }
        }
    }

    def __init__(self):
        super().__init__(target=self._thread)
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(name=__name__)
        self.trigger = threading.Event()
        self.start()

    def set_characteristic(self, uuid: str, value: float):
        characteristic = self.server.get_characteristic(uuid)
        characteristic.value = bytearray(struct.pack("f", value))
        self.logger.debug(f"{uuid} value set to {characteristic.value}")

    def _thread(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._run(loop))

    def _read_request(self, characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
        self.logger.debug(f"Reading {characteristic.value}")
        return characteristic.value

    def _write_request(self, characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        characteristic.value = value
        self.logger.debug(f"Char value set to {characteristic.value}")

    async def _run(self, loop):
        self.trigger.clear()

        # Instantiate the server
        self.server = BlessServer(name="Turbine test service", loop=loop)
        self.server.read_request_func = self._read_request
        self.server.write_request_func = self._write_request

        await self.server.add_gatt(self.gatt)
        await self.server.start()
        self.logger.debug("Advertising")
        self.trigger.wait()
        await self.server.stop()
