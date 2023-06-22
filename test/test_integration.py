import unittest
from time import sleep

from db import populate_db, LocalDBConnector
from main import handle_send_message_requests
from models import RequestMessage
from queue_broker import LocalQueueConnector
from services.messages_distributor import start_messages_distributor
from services.social_platform_output import DummyTwitterApi


class TestSum(unittest.TestCase):
    def setUp(self) -> None:
        db_connector = LocalDBConnector()
        self.db = db_connector.connect()
        queue_connector = LocalQueueConnector()
        self.queue = queue_connector.connect()
        populate_db(self.db)
        self.twitter_api = DummyTwitterApi()
        self.stop_message_distrubutor = start_messages_distributor(db_connector=db_connector,
                                                                   queue_connector=queue_connector,
                                                                   twitter_api=self.twitter_api)

    def tearDown(self) -> None:
        self.stop_message_distrubutor()
        self.db, self.queue, self.stop_message_distrubutor = None, None, None

    def test_messages_end_up_in_db_and_twitter_api(self):
        """
        Test that requests is handlded gracefully and messages are processed by queue and db
        """
        handle_send_message_requests(self.db, self.queue, RequestMessage(to_user_id=2, text='test'))
        handle_send_message_requests(self.db, self.queue, RequestMessage(to_user_id=1, text='test'))
        sleep(1)
        all_messages = self.db.get_messages()
        self.assertEqual(len(all_messages), 2)
        self.assertEqual(all_messages[0].text, 'test')
        self.assertEqual(all_messages[0].from_user_id, 1)
        self.assertEqual(all_messages[0].to_user_id, 2)

        self.assertEqual(all_messages[1].text, 'test')
        self.assertEqual(all_messages[1].from_user_id, 2)
        self.assertEqual(all_messages[1].to_user_id, 1)

        self.assertListEqual(self.twitter_api.messages, [
            "I sent a message to Bob 'test'",
            "I got a message from Alice 'test'",
            "I sent a message to Alice 'test'",
            "I got a message from Bob 'test'",
        ])
