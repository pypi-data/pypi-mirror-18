from __future__ import unicode_literals
import hueobject


class Group(hueobject.LightDevice):
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__('groups', *args, **kwargs)

    @property
    def lights(self):
        l = []
        for l_id in self._json['lights']:
            l.append(self._bridge.light(hue_id=l_id))
        return l

    @property
    def state(self):
        return GroupState(self._json['state'])

    @property
    def all_on(self):
        return self.state.all_on

    @property
    def any_on(self):
        return self.state.any_on

    def _set_state(self, data):
        # Groups have a different endpoint for the "state" (/action)
        url = '{}/action'.format(self.API)
        res = self._request(
            method='PUT',
            url=url,
            data=data
        )
        self.update()
        return res


class GroupState(hueobject.HueObject):
    @property
    def all_on(self):
        return self._json['all_on']

    @property
    def any_on(self):
        return self._json['any_on']
