from __future__ import unicode_literals
import hueobject


class Light(hueobject.HueDevice):
    def __init__(self, *args, **kwargs):
        super(Light, self).__init__('lights', *args, **kwargs)

    @property
    def state(self):
        return LightState(self._json['state'])

    def __on_off(self, state):
        assert state in ['on', 'off'], 'Unknown state: {}'.format(state)
        return self._set_state(data={'on': state == 'on'})

    def on(self):
        return self.__on_off('on')

    def off(self):
        return self.__on_off('off')

    def is_on(self):
        return self.state.on

    def delete(self):
        return self._request(method='DELETE')


class LightState(hueobject.HueObject):
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
    def ct(self):
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
