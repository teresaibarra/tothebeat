import asyncio
from bleak import BleakScanner, BleakClient
from pythonosc import udp_client

MODEL_NBR_UUID = "2A37"

# OSC settings
OSC_SERVER_IP = "127.0.0.1"  # Change this to the IP address of your Max/MSP machine
OSC_SERVER_PORT = 9000  # Change this to the port number you're using in Max/MSP

async def main():
    # OSC client for sending messages
    osc_client = udp_client.SimpleUDPClient(OSC_SERVER_IP, OSC_SERVER_PORT)

    async with BleakScanner() as scanner:
        device = await scanner.find_device_by_name('FitcentCL808_0602312')
        
        if not device:
            print("Teresa's HR monitor was not found")
            return
        
        async with BleakClient(device) as client:
            # Callback function to process incoming heart rate data
            def callback(sender, data):
                # Read flags byte
                flags = data[0]

                # Interpret heart rate based on format specified in flags
                heart_rate_format = flags & 0x01  # Bit 0: Heart Rate Value Format
                if heart_rate_format == 0:
                    heart_rate = data[1]  # Heart rate is a single byte
                else:
                    heart_rate = (data[2] << 8) | data[1]  # Heart rate is two bytes (little endian)
                    
                print("Heart rate:", heart_rate)

                # Send heart rate over OSC
                osc_client.send_message("/heart_rate", heart_rate)

            # Start notifications for heart rate characteristic
            await client.start_notify(27, callback)

            while True:
                # Sleep for a while to avoid consuming too much CPU
                await asyncio.sleep(0.5)

    print("Scanner has terminated")

asyncio.run(main())