# Azure IoT Hub GPS route simulator

This repo contains a helper Python file that can take a track in [GPX](https://wikipedia.org/wiki/GPS_Exchange_Format) format and send track data to [Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=academic-0000-jabenn). It reads the track information and send each point sequentially, with a defined pause (defaulting to 5 seconds) between each send.

## To use this code

1. Create a Python virtual environment

1. Install the required Pip packages using the `requirements.txt` file

1. Get the connection string for your device from Azure IoT Hub. You can either:

    * Create a .env file with the connection string in it with a key of `DEVICE_CONNECTION_STRING`
    * Pass the connection string when running this file with the command line argument `--connection_string`

1. Run the `app.py` file in Python, passing in the file name as a parameter.

1. The GPX file will be read, and the `trkprt` nodes will be read in order and sent to IoT Hub, one every 5 seconds.

Each `trkprt` node will be sent as a telemetry message in the following format:

```json
{
    'lat': '47.73481',
    'lon': '-122.257'
}
```

## Arguments

```output
usage: app.py [-h] [-cs connection_string] [-fq frequency] [-r] [-rv] file

positional arguments:
  file                  The .gpx file to upload

optional arguments:
  -h, --help            show this help message and exit
  -cs connection_string, --connection_string connection_string
                        The IoT Hub device connection string to use to connect. You can also set this in a .env file with the DEVICE_CONNECTION_STRING key
  -fq frequency, --frequency frequency
                        The number of seconds to wait between sending each point
  -r, --repeat          Set this to continuously send the file
  -rv, --reverse        Set this to reverse the points in the file after they've all been sent
```
