from __future__ import unicode_literals
import basemodel


class Light(basemodel.LightDevice):
    def __init__(self, bridge, hue_id, json):
        super(Light, self).__init__(bridge, 'lights', hue_id, json)

    @property
    def state(self):
        return basemodel.LightDeviceState(self._json['state'])

    def __str__(self):
        return '<Light: {}{}>'.format(self.name, ' (*)' if self.is_on else '')
