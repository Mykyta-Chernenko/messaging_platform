import abc

from db import DB
from models import UserID


class TwitterApi(abc.ABC):
    @abc.abstractmethod
    def send_post(self, message: str, api_key: str):
        raise NotImplemented()


class DummyTwitterApi(TwitterApi):
    def __init__(self):
        self.messages = []

    def send_post(self, message: str, api_key: str):
        self.messages.append(message)
        print(message)


class SocialPlatformOutput(abc.ABC):
    @abc.abstractmethod
    def handle_message_to(self, db: DB, from_user_id: UserID, to_user_id: UserID, text: str):
        raise NotImplemented()

    @abc.abstractmethod
    def handle_message_from(self, db: DB, from_user_id: UserID, to_user_id: UserID, text: str):
        raise NotImplemented()


class TwitterOutput(SocialPlatformOutput):
    twitter_characters_limit = 280

    def __init__(self, twitter_api: TwitterApi):
        self.twitter_api = twitter_api

    def handle_message_to(self, db: DB, from_user_id: UserID, to_user_id: UserID, text: str):
        self.handle_message(db, from_user_id, to_user_id, text, "I sent a message to")

    def handle_message_from(self, db: DB, from_user_id: UserID, to_user_id: UserID, text: str):
        self.handle_message(db, to_user_id, from_user_id, text, "I got a message from")

    def handle_message(self, db: DB, sender_id: UserID, receiver_id: UserID, text: str,
                       message_start: str):
        twitter_platform = db.get_user_social_platform(receiver_id, 'twitter')
        twitter_platform_api_key = twitter_platform.api_key
        sender = db.get_user(sender_id)
        sender_name = sender.name
        message = f"{message_start} {sender_name} '{text}'"[:self.twitter_characters_limit]
        self.twitter_api.send_post(message, twitter_platform_api_key)
