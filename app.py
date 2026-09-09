from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import serial.tools.list_ports
import threading
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

socketio = SocketIO(app, cors_allowed_origins="*")

BAUD = 9600

def find_nodemcu_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        s = f"{p.device} {p.description} {p.manufacturer or ''}".lower()
        if any(k in s for k in ["ch340", "ch341", "usb-serial", "usb serial", "wch"]):
            return p.device
    return ports[0].device if len(ports) == 1 else None

@app.route("/")
def index():
    print("Opening Dashboard")
    print("Template Folder: ",app.template_folder)
    return render_template("index.html")

def serial_reader():
    while True:
        port = find_nodemcu_port()
        if not port:
            socketio.emit("system", {"connected": False, "message": "NodeMCU serial port not found"})
            time.sleep(2)
            continue
        try:
            with serial.Serial(port, BAUD, timeout=1) as ser:
                time.sleep(2)
                socketio.emit("system", {"connected": True, "port": port})
                while True:
                    line = ser.readline().decode(errors="ignore").strip()
                    if not line:
                        continue
                    print("ESP:", line)

                    if line == "EYE_OPEN":
                        socketio.emit("eye_status", {"status": "OPEN"})
                    elif line == "EYE_CLOSED":
                        socketio.emit("eye_status", {"status": "CLOSED"})
                    elif line.startswith("CLOSED_MS:"):
                        try: socketio.emit("closed_time", {"milliseconds": int(line.split(":",1)[1])})
                        except ValueError: pass
                    elif line.startswith("SENSOR:"):
                        try: socketio.emit("sensor", {"value": int(line.split(":",1)[1])})
                        except ValueError: pass
                    elif line.startswith("BRAKE:"):
                        try:
                            v = max(0, min(100, int(line.split(":",1)[1])))
                            socketio.emit("brake", {"percent": v})
                        except ValueError: pass
                    elif line.startswith("SPEED:"):
                        try: socketio.emit("speed", {"kmh": float(line.split(":",1)[1])})
                        except ValueError: pass
                    elif line == "HAZARD:ON":
                        socketio.emit("hazard", {"active": True})
                    elif line == "HAZARD:OFF":
                        socketio.emit("hazard", {"active": False})
                    elif line == "HORN:ON":
                        socketio.emit("horn", {"active": True})
                    elif line == "HORN:OFF":
                        socketio.emit("horn", {"active": False})
                    elif line == "VEHICLE_STOPPED":
                        socketio.emit("vehicle_stopped", {})
                    elif line == "SOS:TRIGGER":
                        socketio.emit("sos", {"active": True})
                    elif line.startswith("STATE:"):
                        socketio.emit("state", {"state": line.split(":",1)[1]})
        except (serial.SerialException, OSError) as e:
            socketio.emit("system", {"connected": False, "message": str(e)})
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=serial_reader, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000, debug=False, allow_unsafe_werkzeug=True)
