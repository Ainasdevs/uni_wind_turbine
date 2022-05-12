import logging
import threading
import asyncio
import struct
import globals
from bleak import BleakClient


class Client(threading.Thread):
    def __init__(self, device):
        super().__init__(target=self._thread)
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(name=__name__)
        self.time = 0.25
        self.is_running = True
        self.device = device
        self.client = None
        self.start()

    def stop(self):
        self.is_running = False

    def _thread(self):
        asyncio.run(self._run())

    async def _run(self):
        async with BleakClient(self.device, timeout=10) as client:
            self.client = client
            while self.is_running:
                await asyncio.sleep(self.time)
                voltage = await self.client.read_gatt_char(globals.voltage_uuid)
                current = await self.client.read_gatt_char(globals.current_uuid)
                rpm = await self.client.read_gatt_char(globals.rpm_uuid)
                globals.gui.frame.voltage = struct.unpack("f", voltage[:4])[0]
                globals.gui.frame.current = struct.unpack("f", current[:4])[0]
                globals.gui.frame.rpm = struct.unpack("f", rpm[:4])[0]
