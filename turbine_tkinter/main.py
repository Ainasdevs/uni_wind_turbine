import globals
import asyncio
from ui.TurbineGui import TurbineGui
from bleak import BleakScanner
from client import Client


async def main():
    print(f"Searching for with service uuid {globals.service_uuid}.")
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: ad.service_uuids and globals.service_uuid in ad.service_uuids
    )

    if not device:
        print(f"Device with service uuid {globals.service_uuid} not found. Exiting")
        exit()
    print(device)

    globals.client = Client(device)
    globals.gui = TurbineGui(width=300, height=400)
    globals.gui.mainloop()
    globals.client.stop()
    globals.client.join()


if __name__ == "__main__":
    asyncio.run(main())
