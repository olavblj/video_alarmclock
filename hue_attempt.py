from phue import Bridge

b = Bridge('192.168.0.100')
b.connect()

lights = b.lights

print([l.__dict__ for l in lights])

for light in lights:
    b.set_light(light.light_id, 'on', True)
