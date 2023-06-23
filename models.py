from typing import Literal

from pydantic import BaseModel

UserID = int


class User(BaseModel):
    id: UserID
    name: str


UserSocialPlatformId = int
UserSocialPlatformType = Literal['twitter', 'mastodon']


class UserSocialPlatform(BaseModel):
    id: UserSocialPlatformId
    user_id: UserID
    type: UserSocialPlatformType
    # TODO better to be encrypted
    api_key: str


UserMessageID = int


class UserMessage(BaseModel):
    id: UserMessageID
    from_user_id: UserID
    to_user_id: UserID
    text: str


### requests ###

class RequestMessage(BaseModel):
    to_user_id: UserID
    text: str
