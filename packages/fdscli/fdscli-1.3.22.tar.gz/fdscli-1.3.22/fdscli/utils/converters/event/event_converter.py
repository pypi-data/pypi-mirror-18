# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
import json
from model.event.event import Event

class EventConverter(object):
    '''Helper class for marshalling between Event and JSON formatted string.

    The term 'to marshal' means to convert some data from internal to external form
    (in an RPC buffer for instance). The term 'unmarshalling' refers to the reverse
    process. We presume that the server will use reflection to create a Java object
    given the JSON formatted string.
    '''

    @staticmethod
    def to_json(event):
        """
        :param event: ``model.event.Event`` object to convert to JSON dict
        :return: a dict representing the ``model.event.Event`` object that follows the JSON convention
        """

        json_d = dict()

        json_d["uuid"] = event.uuid
        json_d["messageKey"] = event.message_key
        json_d["defaultMessage"] = event.default_message
        json_d["initialTimestamp"] = event.creation_time
        json_d["severity"] = event.severity
        json_d["categories"] = event.categories
        json_d["messageArgs"] = event.message_args

        return json_d

    @staticmethod
    def to_json_string(event):
        '''Converts ``model.event.Event`` object into a JSON formatted string.

        We presume that the recipient (a server) uses a package like Gson and passes the type
        literal when deserializing the JSON formatted string.

        Parameters
        ----------
        :type event: ``model.event.Event`` object

        Returns
        -------
        :type string
        '''

        d = EventConverter.to_json(event)

        result = json.dumps(d)
        return result

    @staticmethod
    def build_from_json(j_str):
        '''Produce a ``model.event.Event`` object from deserialized server response

        Parameters
        ----------
        :type j_str: dict or json-encoded string representing a JSON object

        Returns
        -------
        :type ``model.event.Event``
        '''
        event = Event()

        # If given argument not a dict, decode to a dict
        if not isinstance(j_str, dict):
            j_str = json.loads(j_str)

        if "messageArgs" in j_str:
            event.message_args = j_str.pop("messageArgs", event.message_args)

        if "messageKey" in j_str:
            event.message_key = j_str.pop("messageKey", event.message_key)

        if "uuid" in j_str:
            event.uuid = j_str.pop("uuid", event.uuid)

        if "defaultMessage" in j_str:
            event.default_message = j_str.pop("defaultMessage", event.default_message)

        if 'initialTimestamp' in j_str:
            event.creation_time = j_str.pop("initialTimestamp", event.creation_time)

        if 'severity' in j_str:
            event.severity = j_str.pop("severity", event.severity)

        # v08 model only supported a single category, but event service model is 
        # a list
        if 'categories' in j_str:
            event.categories = j_str.pop("categories", event.categories)
        elif 'category' in j_str:
            #event.categories = []
            #event.categories.append(j_str.pop("category", event.categories))
            event.categories = j_str.pop("category", event.categories)
            
        return event
