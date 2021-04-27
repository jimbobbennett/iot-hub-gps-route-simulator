import argparse
import json
import os
import time
from azure.iot.device import IoTHubDeviceClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

try:
    device_connection_string = os.environ['DEVICE_CONNECTION_STRING']
except KeyError:
    device_connection_string = ''

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='file', type=str, help='The .gpx file to upload')
parser.add_argument('-cs', '--connection_string', metavar='connection_string', type=str, default=device_connection_string, help='The IoT Hub device connection string to use to connect. You can also set this in a .env file with the DEVICE_CONNECTION_STRING key')
parser.add_argument('-fq', '--frequency', metavar='frequency', type=int, default=5, help='The number of seconds to wait between sending each point')
parser.add_argument('-r', '--repeat', action='store_true', help='Set this to continuously send the file')
parser.add_argument('-rv', '--reverse', action='store_true', help='Set this to reverse the points in the file after they\'ve all been sent')

args = parser.parse_args()

file_name = args.file
device_connection_string = args.connection_string
frequency = args.frequency
repeat = args.repeat
reverse = args.reverse

if device_connection_string is None or device_connection_string == '':
    print('Missing connection string - either add it to a .env file with a key of DEVICE_CONNECTION_STRING, or pass it as a parameter using --connection_string <connection string>')
    exit()

device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

# Connect the client.
print('Connecting to Azure IoT Hub...')
device_client.connect()
print('Connected!')

def send_track_part(track_part):
    telemetry = {
        'lat' : track_part['lat'],
        'lon' : track_part['lon']
    }

    print('Sending telemetry:', telemetry)

    device_client.send_message(json.dumps(telemetry))

def send_file():
    print('Processing route file:', file_name)

    with open(file_name, 'r')  as gpx_file:
        soup = BeautifulSoup(gpx_file, 'lxml')
        track_parts = soup.find_all('trkpt')

        for track_part in track_parts:
            send_track_part(track_part)
            time.sleep(frequency)
        
        if reverse:
            print('Sending file in reverse')
            track_parts.reverse()

            for track_part in track_parts:
                send_track_part(track_part)
                time.sleep(frequency)


if repeat:
    while True: send_file()
else:
    send_file()

print('Done!')