import json
from _lzma import _encode_filter_properties

import OneSignal.OSOperator

class OSPayload:


    def __init__(self):
        self.app_id = None
        self.filters = list()
        self.send_after = None
        self.delayed_option = None
        self.delivery_time_of_day = None
        self.ttl = None
        self.priority = None
        self.included_segments = None
        self.content = None

    @staticmethod
    def encodeFilters(obj):
        if isinstance(obj, OneSignal.OSFilter.OSFilter):
            return obj.__dict__
        elif isinstance(obj, OneSignal.OSOperator.OSOperator):
            return obj.__dict__
        return obj

