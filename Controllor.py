from jetbot import Robot
from evdev import InputDevice, ecodes, ff, list_devices
import time
import os
import json


class Controllor:

    def __init__(self) -> None:
        # 编译已连接的设备，寻找具有 Force Feedback 属性的设备
        for name in list_devices():
            self.dev = InputDevice(name)
            if ecodes.EV_FF in self.dev.capabilities():
                break
        self.robot = Robot()

    def syncXInputData(self) -> None:
        try:
            f = open("data.json", "r")
            self.data = json.load(f)
            f.close()
        except:
            pass

    def joystickMotionBind(self) -> None:

        while (not os.path.exists("./XInput.lock")):

            self.syncXInputData()

            if (self.data["leftPedal"] == 0 and self.data["rightPedal"] == 0):
                self.robot.stop()
            else:
                self.forceFeedback()

        print("[Controllor] JoyStick Disconnected")

    def forceFeedback(self) -> None:

        duration_ms = 100
        # 震动数值
        rumble = ff.Rumble(strong_magnitude=int((self.data["leftPedal"]+self.data["rightPedal"]/2.0)*65535),
                           weak_magnitude=int((self.data["leftPedal"]+self.data["rightPedal"]/2.0)*20000))
        # 震动效果
        effect = ff.Effect(
            ecodes.FF_RUMBLE, -1, 0,
            ff.Trigger(0, 0),
            ff.Replay(duration_ms, 0),
            ff.EffectType(ff_rumble_effect=rumble)
        )

        effect_id = self.dev.upload_effect(effect)
        self.dev.write(ecodes.EV_FF, effect_id, 1)
        if(self.data["syncInput"]):
            self.robot.forward(self.data["rightPedal"])
        else:
            self.robot.set_motors(
                self.data["leftPedal"], self.data["rightPedal"])
        time.sleep(0.1)
        self.dev.erase_effect(effect_id)

if __name__ == "__main__":
    controllor = Controllor()
    controllor.joystickMotionBind()
