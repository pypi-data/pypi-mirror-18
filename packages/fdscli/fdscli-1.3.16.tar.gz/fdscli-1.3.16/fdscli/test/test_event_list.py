# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#

from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.event.event import Event
from model.fds_error import FdsError
from services.event.event_client import EventClient
from services.fds_auth import FdsAuth

def mock_put_request(session, url, data):
    print url
    response = FdsError()
    return response

def mock_get_url_preamble():
    return "http://localhost:7777/fds/config/v09"

def mock_list_events():
    '''Request list of events.

    Returns
    -------
    :type ``model.FdsError`` or list(``Event``)
    '''
    events = []
    event = Event(default_message="Message for event 1.", creation_time=0)
    events.append(event)
    event2 = Event(default_message="Message for event 2.", creation_time=1)
    events.append(event2)
    return events

class EventListTest( BaseCliTest ):
    '''Tests plugin and service client functionality for 'event list' command.

    IS-A unittest.TestCase.
    '''
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.event.event_client.EventClient.list_events", side_effect=mock_list_events)
    def test_list_events_subcommand(self, mock_list, mock_write):
        '''Tests the event plugin for 'event list' subcommand.

        The service calls are replaced by mock functions.

        Parameters
        ----------
        :type mock_list: ``unittest.mock.MagicMock``
        :type mock_write: ``unittest.mock.MagicMock``
        '''
        args = ["event", "list"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mock_list.call_count == 1

        print("test_list_events_subcommand passed.\n\n")

    @patch("services.abstract_service.AbstractService.get_url_preamble", side_effect=mock_get_url_preamble)
    @patch("services.rest_helper.RESTHelper.put", side_effect=mock_put_request)
    def test_client_list_events(self, mock_put, mock_url):
        '''Directly tests the real EventClient.list_events API.

        Parameters
        ----------
        :type mock_put: ``unittest.mock.MagicMock``
        :param mock_put: Replace REST helper put() with mock empty

        :type mock_url: ``unittest.mock.MagicMock``
        :param mock_url: Returns the string to prepend for PUT Url
        '''
        session = FdsAuth()
        client = EventClient(session)
        client.list_events()

        # The client list_subscription is a url producer
        assert mock_put.call_count == 1
        url = mock_put.call_args[0][1]
        assert url == "http://localhost:7777/fds/config/v09/events"

        print("test_client_list_events passed.\n\n")

