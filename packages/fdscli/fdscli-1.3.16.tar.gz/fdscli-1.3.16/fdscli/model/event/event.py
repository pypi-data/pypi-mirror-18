# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#

from enum import Enum, unique

import event_category
import model.event.event_severity
import event_type

# Sample server response:

# {
#     'messageKey': 'pm.service.startup',
#     'category': {},
#     'severity': {},
#     'initialTimestamp': 1480352595498,
#     'messageFormat': 'PM on node {0} is up',
#     'modifiedTimestamp': 1480352595498,
#     'state': {},
#     'defaultMessage': 'PM on node 3769979169947774912 is up',
#     'type': {},
#     'messageArgs': ['3769979169947774912']
# }

# TODO: Can't add enumerated values in the Event object until server response is valid.

class Event(object):
    '''Represents a persisted event.

    Events are stored with a generated id, a timestamp, type, category, severity, and a state.
    The event details include a message key and arguments.

    Attributes
    ----------
    :type __uuid: long TODO

    :type __creation_time: long
    :type __default_message: string

    :type __event_category: ``model.event.EventCategory``  TODO
    :type __event_severity: ``model.event.EventSeverity``  TODO
    :type __event_type: ``model.event.EventType``          TODO
    '''
    def __init__(self, uuid=-1, creation_time=0, default_message=None):

        self.creation_time = creation_time
        self.default_message = default_message

    @property
    def creation_time(self):
        return self.__creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        self.__creation_time = creation_time

    @property
    def default_message(self):
        return self.__default_message

    @default_message.setter
    def default_message(self, default_message):
        self.__default_message = default_message

