from evdev import InputDevice, list_devices, ecodes
import os
import json
import time

# 编译已连接的设备，寻找具有 Force Feedback 属性的设备
for name in list_devices():
    dev = InputDevice(name)
    if ecodes.EV_FF in dev.capabilities():
        break

print("[XInput INFO] Loading Config")
try:
    f = open("./data.json", "r")
    data = json.load(f)
    f.close()
except FileNotFoundError:
    f = open("./data.json", "w")
    data = {"leftPedal": 0.0, "rightPedal": 0.0, "syncInput": False}
    json.dump(data, f)
    f.close()

print("[XInput INFO] >>Session Start<<")
while(not os.path.exists("./XInput.lock")):
    try:
        for ev in dev.read_loop():

            if (os.path.exists("./XInput.lock")):
                print("[XInput INFO] >>Session Ended<<")
                exit(0)

            if (ev.code == 2):
                data["leftPedal"] = round(ev.value/1024.0, 2)

            if (ev.code == 5):
                data["rightPedal"] = round(ev.value/1024.0, 2)

            if(ev.code == 311):
                print("[XInput INFO] Input mode changed")
                data["syncInput"] = not data["syncInput"]

            f = open("./data.json", "w")
            print(data)
            json.dump(data, f, ensure_ascii=False)
            f.close()
    except OSError:
        # 设备断开时尝试重连
        print("[XInput WARN] Device Disconnected")
        print("[XInput INFO] Waiting for Reconect")
        time.sleep(3.0)
        for name in list_devices():
            dev = InputDevice(name)
            if ecodes.EV_FF in dev.capabilities():
                break
