# coding: utf-8

from __future__ import unicode_literals
import basemodel


class Schedule(basemodel.HueLLDevice):
    def __init__(self, *args, **kwargs):
        super(Schedule, self).__init__('schedule', *args, **kwargs)
