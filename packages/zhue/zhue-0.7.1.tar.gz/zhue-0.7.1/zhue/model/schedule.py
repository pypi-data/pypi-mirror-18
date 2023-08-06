# coding: utf-8

from __future__ import unicode_literals
import api_response
import basemodel


class Schedule(basemodel.HueLLDevice):
    def __init__(self, *args, **kwargs):
        super(Schedule, self).__init__('schedules', *args, **kwargs)

    @staticmethod
    def new(bridge, command, localtime, status='enabled', name='',
            description='', autodelete=True, recycle=True):
        response = bridge._request(
            url='{}/schedules'.format(bridge.API),
            method='POST',
            data={
                'command': command,
                'name': name,
                'description': description,
                'status': status,
                'localtime': localtime,
                # 'autodelete': autodelete, # FIXME
                'recycle': recycle
            }
        )
        if type(response) is api_response.HueSuccessResponse:
            return bridge.schedule(hue_id=response._json['id'])
        return response

    @property
    def description(self):
        return self._json['description']

    @property
    def created(self):
        return self._json['created']

    @property
    def time(self):
        return self._json['time']

    @property
    def localtime(self):
        return self._json['localtime']

    @property
    def command(self):
        return ScheduledCommand(self._json['command'])

    @property
    def device(self):
        return self._bridge.from_address(self.command.address)

    @property
    def status(self):
        return self._json['status']

    @property
    def recycle(self):
        return self._json['recycle']


class ScheduledCommand(basemodel.HueJsonObject):
    @property
    def method(self):
        return self._json['method']

    @property
    def body(self):
        return self._json['body']

    @property
    def address(self):
        '''
        Override the address property because if does not contain the
        bridge hostname
        '''
        return self._json['address']
