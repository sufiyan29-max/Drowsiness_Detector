# Driver Guard 3D

Local 3D dashboard for a NodeMCU ESP8266 drowsiness-detector prototype.

## Run
1. Connect NodeMCU with a USB data cable.
2. Close Arduino Serial Monitor.
3. Open a terminal in this folder.
4. Run: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Open: `http://127.0.0.1:5000`

The Python bridge looks for CH340/CH341/WCH serial devices at 9600 baud.

Expected serial messages:
EYE_OPEN
EYE_CLOSED
CLOSED_MS:5100
SENSOR:620
STATE:NORMAL
STATE:MONITORING
STATE:DROWSY
BRAKE:40
HAZARD:ON
HAZARD:OFF
HORN:ON
HORN:OFF
SPEED:0
VEHICLE_STOPPED
SOS:TRIGGER

Notes:
- Three.js and Socket.IO browser client are loaded from CDNs, so the laptop needs internet access to load them.
- NodeMCU communicates only over USB; NodeMCU Wi-Fi is not required.
- Browser geolocation is requested after SOS:TRIGGER.
- This is a simulation only. It does not control a real vehicle or contact emergency services.


## Version 3 additions

- Procedural engine sound using the browser Web Audio API.
- Emergency horn sound follows `HORN:ON` / `HORN:OFF`.
- Click **ENABLE AUDIO** once after opening the dashboard because browsers block automatic audio.
- 3D wheels rotate with simulated speed.
- Road moves with vehicle speed.
- Car body dips under simulated braking.
- Brake lamps illuminate according to braking percentage.
- Hazard lamps flash on the 3D car.

No external audio files are required.

## ESP compatibility

This dashboard works with the ESP8266/NodeMCU code as long as Serial is set to `9600` and the sketch emits the supported text commands.
