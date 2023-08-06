from __future__ import absolute_import
from __future__ import unicode_literals
from .basemodel import HueLLDevice


class Rule(HueLLDevice):
    def __init__(self, bridge, hue_id, json):
        super(Rule, self).__init__(bridge, 'rules', hue_id, json)

    @staticmethod
    def new(bridge, *args, **kwargs):
        raise NotImplementedError()
