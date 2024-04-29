## To The Beat (WIP)

This project finds a wearable heart rate monitor (Bluetooth Low Energy device) and streams its heart rate data over UDP. The script in the MaxMSP patch listens in on the port to create a metronome that changes depending on the wearer's heart rate. This project was named after the [Hilary Duff](https://www.youtube.com/watch?v=gua14Z09HR4) song and was created at [Recurse Center](http://recurse.com/) in March 2024.

This project is very much a work in progress, so it's not the prettiest.

### Usage
Run `python ble_info.py`, then run the MaxMSP patch.

To play around with the "heart rate", check out this GIF:
![2024-04-18 21 26 33](https://github.com/teresaibarra/tothebeat/assets/7967489/ee3486e3-2126-4181-9212-8f44d0cd3f70)
