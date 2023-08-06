# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#

from enum import Enum, unique

import event_category
import event_severity
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
# categories, in new event model, are just a list of strings.

class Event(object):
    '''Represents a persisted event.

    Events are stored with a generated id, a timestamp, type, category, severity, and a state.
    The event details include a message key and arguments.

    Attributes
    ----------
    :type __uuid: long TODO

    :type __message_key: string
    :type __creation_time: long
    :type __default_message: string

    :type __categories: ``model.event.EventCategory``  TODO
    :type __severity: ``model.event.EventSeverity``  TODO
    :type __event_type: ``model.event.EventType``          TODO
    '''
    def __init__(self, uuid=-1, message_key="", creation_time=0, default_message=None, severity=None, categories=None,
                 message_args=None):

        # This prevents issues with using lists as default parameters in methods
        # e.g. : http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments
        if categories is None:
            categories = []

        # Working with key value pairs is much easier, so we'll pack whatever list we received in the dict
        # this way any additional args can be assigned with a k/v pair instead of simply relying on position in the list
        if type(message_args) is None or type(message_args) is list:
            self.__message_args = {'listArgs': message_args}
        elif type(message_args) is dict:
            self.__message_args = message_args
        else:
            self.message_args = {}

        self.__message_key = message_key
        self.__uuid = uuid
        self.__creation_time = creation_time
        self.__default_message = default_message
        self.__categories = categories
        self.__severity = severity

    @property
    def message_key(self):
        return self.__message_key

    @message_key.setter
    def message_key(self, message_key):
        self.__message_key = message_key

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

    @property
    def severity(self):
        return self.__severity

    @severity.setter
    def severity(self, severity):
        self.__severity = severity

    @property
    def categories(self):
        return self.__categories

    @categories.setter
    def categories(self, categories):
        self.__categories = categories

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def message_args(self):
        return self.__message_args

    @message_args.setter
    def message_args(self, value):
        if type(value) is list:
            self.__message_args = {'listArgs': value}
        elif type(value) is dict:
            self.__message_args = value
        else:
            self.__message_args = {}
