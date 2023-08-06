# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
from model.fds_error import FdsError
from model.task.completion_status import CompletionStatus
from model.task.safeguard_task_status import SafeGuardTaskStatus, SafeGuardTaskType
from services.fds_auth import FdsAuth
from services.safeguard.safeguard_task_client import SafeGuardTaskClient
import mock_functions

def mock_list_safeguard_tasks():

    tasks_with_status = []

    task = SafeGuardTaskStatus()
    task.uuid = "65bf8849-c080-49c9-aff2-60d95fa9144a"
    task.description = "an export task"
    task.volume_id = int(5)
    task.status = CompletionStatus.failed
    task.task_type = SafeGuardTaskType.volume_export

    task2 = SafeGuardTaskStatus()
    task2.uuid = "65bf8849-dddd-49c9-aff2-60d95fa9144a"
    task2.description = "an import task"
    task2.volume_id = int(5)
    task2.status = CompletionStatus.running
    task2.task_type = SafeGuardTaskType.volume_import

    tasks_with_status.append(task)
    tasks_with_status.append(task2)
    return tasks_with_status

def mock_get_request(session, url):
    print url
    response = FdsError()
    return response

def mock_get_url_preamble():
    return "http://localhost:7777/fds/config/v09"

class TestSafeGuardTaskStatus(BaseCliTest):
    '''Tests basic class functionality for ``model.task.SafeGuardTaskStatus``.
    '''
    def test_properties(self):

        task_status1 = SafeGuardTaskStatus(uuid=5150, description="task 1")
        assert task_status1.volume_id == -1
        assert task_status1.status == CompletionStatus.unknown
        print "status: {}".format(task_status1.status)
        assert task_status1.status.name == "unknown"
        print "type: {}".format(task_status1.task_type)
        assert task_status1.task_type.name == "unknown"

        # Test custom string value for 'running' status
        task_status1.status = CompletionStatus.running
        print "status: {}".format(task_status1.status)
        assert str(task_status1.status) == "in_progress"
        assert task_status1.status.name == "running"

        # Test custom string value for 'volume_export" task type
        task_status1.task_type = SafeGuardTaskType.volume_export
        print "type: {}".format(task_status1.task_type)
        assert str(task_status1.task_type) == "export"
        assert task_status1.task_type.name == "volume_export"

        # Create a second task status
        task_status2 = SafeGuardTaskStatus(uuid=538, description="task 2")
        task_status2.status = CompletionStatus.initiated
        print "status: {}".format(task_status2.status)
        assert task_status2.status.name == "initiated"

        # Validate that task1 values remain unchanged when task2 modified
        assert task_status1.status.name == "running"
        assert task_status1.task_type == SafeGuardTaskType.volume_export

    @patch("services.safeguard.safeguard_task_client.SafeGuardTaskClient.list_tasks_with_status",
        side_effect=mock_list_safeguard_tasks)
    def test_plugin(self, mockListTasks):
        '''Command 'volume safeguard tasks' lists the data migration tasks.

        A parser for the command is created in the VolumePlugin. All service client calls are mocked.

        Parameters
        ----------
        :type mockListTasks: ``unittest.mock.MagicMock``
        '''

        print("Plugin test: volume safeguard tasks")

        args = ["volume", "safeguard", "tasks"]
        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockListTasks.call_count == 1

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.abstract_service.AbstractService.get_url_preamble", side_effect=mock_get_url_preamble)
    @patch("services.rest_helper.RESTHelper.get", side_effect=mock_get_request)
    def test_safeguard_task_client(self, mockServiceGet, mockUrlPreamble, mockTabular, mockPretty):
        '''Directly tests the real SafeGuardTaskClient API.

        Parameters
        ----------
        :type mockServiceGet: ``unittest.mock.MagicMock``
        :param mockServiceGet: Replace REST helper get() with mock empty

        :type mockUrlPreamble: ``unittest.mock.MagicMock``
        :param mockUrlPreamble: Returns the string to prepend for GET Url

        :type mockTabular: ``unittest.mock.MagicMock``
        :type mockPretty: ``unittest.mock.MagicMock``
        '''
        volume_id = 11
        snapshot_id = 111

        session = FdsAuth()
        client = SafeGuardTaskClient(session)
        client.list_tasks_by_volume(volume_id)

        # The client list_subscription is a url producer
        assert mockServiceGet.call_count == 1
        url = mockServiceGet.call_args[0][1]
        assert url == "http://localhost:7777/fds/config/v09/volumes/11/safeguard/tasks"

        client.list_tasks_by_snapshot(snapshot_id)
        assert mockServiceGet.call_count == 2
        url = mockServiceGet.call_args[0][1]
        assert url == "http://localhost:7777/fds/config/v09/snapshots/111/safeguard/tasks"

        print("test_safeguard_task_client passed.\n\n")

