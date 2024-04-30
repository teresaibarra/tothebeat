import asyncio
import logging
from bleak import BleakScanner, BleakClient
from pythonosc import udp_client

# This constant should be changed to the name of your device. You should be able to find the name of
# your device with a tool like Bluetility: https://github.com/jnross/Bluetility
# Note that if you use a tool like Bluetility and forget to unpair your device from it, 
# this script will not be able to connect to your device.
DEVICE_NAME = "FitcentCL808_0602314"

# UUID of the Heart Rate Measurement characteristic
HR_UUID = '00002a37-0000-1000-8000-00805f9b34fb'

# Change these constants to the address and port of your OSC server
OSC_ADDR = "127.0.0.1"
OSC_PORT = 9000

# Setup logging
logging.basicConfig(level=logging.INFO)

async def find_device(device_name):
    async with BleakScanner() as scanner:
        logging.info(f"Looking for specified device '{device_name}'...")
        return await scanner.find_device_by_name(device_name)

async def notify_handler(client, osc_client):
    def callback(_, data):
        # Interpret heart rate based on format specified in flags
        flags = data[0]
        heart_rate_format = flags & 0x01 # Fetches least significant bit, which determines format

        # Heart rate is either one byte or two in little-endian format
        heart_rate = data[1] if heart_rate_format == 0 else (data[2] << 8) | data[1] 
        logging.info(f"Heart rate: {heart_rate}")
        osc_client.send_message("/heart_rate", heart_rate)

    await client.start_notify(HR_UUID, callback)

async def main():
    device = await find_device(DEVICE_NAME)
    if not device:
        logging.error("Your device was not found.")
        return
    
    try:
        osc_client = udp_client.SimpleUDPClient(OSC_ADDR, OSC_PORT)
        async with BleakClient(device) as client:
            logging.info("Device connected and OSC client has been set up.")
            await notify_handler(client, osc_client)
            await asyncio.Event().wait()  # Run indefinitely until an interrupt or error
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Program terminated.")

if __name__ == "__main__":
    asyncio.run(main())