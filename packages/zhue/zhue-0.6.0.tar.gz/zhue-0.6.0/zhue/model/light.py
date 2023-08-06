from __future__ import unicode_literals
import basemodel


class Light(basemodel.LightDevice):
    def __init__(self, *args, **kwargs):
        super(Light, self).__init__('lights', *args, **kwargs)

    @property
    def is_on(self):
        return self.state.on

    @property
    def state(self):
        return LightState(self._json['state'])

    def __str__(self):
        return 'Light: {}{}'.format(self.name, ' (*)' if self.is_on else '')


class LightState(basemodel.HueJsonObject):
    @property
    def alert(self):
        return self._json['alert']

    @property
    def on(self):
        return self._json['on']

    @property
    def brightness(self):
        return self._json['bri']

    @property
    def colormode(self):
        return self._json['colormode']

    @property
    def color_temperature(self):
        return self._json['ct']

    @property
    def effect(self):
        return self._json['effect']

    @property
    def hue(self):
        return self._json['hue']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def saturation(self):
        return self._json['sat']

    @property
    def xy(self):
        return self._json['xy']
