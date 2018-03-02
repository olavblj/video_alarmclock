from phue import Bridge


class LightSystem:
    class __LightSystem:
        def __init__(self):
            self.bridge = Bridge('192.168.0.100')
            self.bridge.connect()

        def toggle(self):
            on_status = self.is_on()
            print("[LightSystem] {}".format(on_status))
            if on_status is None or not on_status:
                self.on()
            else:
                self.off()

        def on(self, transition_time=1):
            print("[LightSystem] Running on")

            lights = self.bridge.lights
            command = {'transitiontime': 10 * transition_time, 'on': True, 'bri': 254}

            for light in lights:
                self.bridge.set_light(light.light_id, command)

        def off(self, transition_time=1):
            print("[LightSystem] Running off")

            lights = self.bridge.lights
            command = {'transitiontime': 10 * transition_time, 'on': False, 'bri': 254}

            for light in lights:
                self.bridge.set_light(light.light_id, command)

        def is_on(self):
            on_statuses = [light.on for light in self.bridge.lights]
            print("[LightSystem] on_statuses: {}".format(on_statuses))
            if all(on_statuses):
                return True
            elif not any(on_statuses):
                return False
            else:
                return None

    instance = None

    def __init__(self):
        if not LightSystem.instance:
            LightSystem.instance = LightSystem.__LightSystem()

    def __getattr__(self, name):
        return getattr(self.instance, name)
