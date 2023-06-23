from db import DB
from models import RequestMessage


# TODO user_id comes from the Bearer token in the real scenario
def get_user_from_request(db: DB, message: RequestMessage):
    user_id = 2 if message.to_user_id == 1 else 1
    return db.get_user(user_id)
