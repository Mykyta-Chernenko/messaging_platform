import json
import threading
from queue import Empty
from typing import List

from db import DBConnector, DB
from models import UserMessage
from queue_broker import QueueConnector, Queue
from services.social_platform_output import TwitterOutput, SocialPlatformOutput, TwitterApi


def handle_user_message(db: DB, message: UserMessage, social_platform_outputs: List[SocialPlatformOutput]):
    for p in social_platform_outputs:
        p.handle_message_to(db, message.from_user_id, message.to_user_id, text=message.text)
        p.handle_message_from(db, message.from_user_id, message.to_user_id, text=message.text)


def process_queue_message(db: DB, queue: Queue, social_platform_outputs: List[SocialPlatformOutput]):

    try:
        message_string = queue.get(timeout=0.1)
    except Empty:
        pass
    else:
        message = json.loads(message_string)
        user_message = UserMessage.parse_obj(message)
        handle_user_message(db, user_message, social_platform_outputs)


def start_messages_distributor(db_connector: DBConnector, queue_connector: QueueConnector, twitter_api: TwitterApi):
    db = db_connector.connect()
    queue = queue_connector.connect()
    social_platform_outputs = [TwitterOutput(twitter_api)]

    stop_task = False

    def task():
        while not stop_task:
            process_queue_message(db, queue, social_platform_outputs)

    t1 = threading.Thread(target=task)
    t1.start()

    def stop():
        nonlocal stop_task
        stop_task = True
        t1.join()

    return stop
