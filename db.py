import abc
import time
from typing import List

from models import User, UserSocialPlatform, UserMessage, UserID, UserSocialPlatformType, UserMessageID


class DB(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, id: UserID) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user_social_platform(self, platform: UserSocialPlatform) -> UserSocialPlatform:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_social_platform(self, user_id: UserID,
                                 type: UserSocialPlatformType) -> UserSocialPlatform:
        raise NotImplementedError

    @abc.abstractmethod
    def add_message(self, from_user_id: UserID,
                    to_user_id: UserID,
                    text: str) -> UserMessage:
        raise NotImplementedError

    @abc.abstractmethod
    def get_message(self, id: UserMessageID) -> UserMessage:
        raise NotImplementedError

    @abc.abstractmethod
    def get_messages(self) -> List[UserMessage]:
        raise NotImplementedError


# TODO this is a very simple in memory database, can be replaced with PostgresSQL
class LocalDB(abc.ABC):
    def __init__(self):
        self.users: List[User] = []
        self.platforms: List[UserSocialPlatform] = []
        self.messages: List[UserMessage] = []

    def add_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def get_user(self, id: UserID) -> User:
        # TODO handle NotFound
        return [x for x in self.users if x.id == id][0]

    def add_user_social_platform(self, platform: UserSocialPlatform) -> UserSocialPlatform:
        self.platforms.append(platform)
        return platform

    def get_user_social_platform(self, user_id: UserID,
                                 type: UserSocialPlatformType) -> UserSocialPlatform:
        # TODO handle NotFound
        return [x for x in self.platforms if x.user_id == user_id and x.type == type][0]

    def add_message(self, from_user_id: UserID,
                    to_user_id: UserID,
                    text: str) -> UserMessage:
        message = UserMessage(id=time.time_ns(), from_user_id=from_user_id, to_user_id=to_user_id, text=text)
        self.messages.append(message)
        return message

    def get_message(self, id: UserMessageID) -> UserMessage:
        # TODO handle NotFound
        return [x for x in self.messages if x.id == id][0]

    def get_messages(self) -> List[UserMessage]:
        return self.messages


class DBConnector(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> DB:
        """returns queue connection"""
        raise NotImplementedError


class LocalDBConnector(DBConnector):
    def __init__(self):
        self.db = LocalDB()

    def connect(self):
        return self.db


def populate_db(db: DB):
    db.add_user(User(id=1, name='Bob'))
    db.add_user(User(id=2, name='Alice'))
    db.add_user_social_platform(UserSocialPlatform(id=1, user_id=1, type='twitter', api_key='dummy_key'))
    db.add_user_social_platform(UserSocialPlatform(id=2, user_id=2, type='twitter', api_key='dummy_key'))
