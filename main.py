import json
from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth import get_user_from_request
from db import LocalDBConnector, populate_db, DB
from models import RequestMessage
from queue_broker import LocalQueueConnector, Queue
from services.messages_distributor import start_messages_distributor
from services.social_platform_output import DummyTwitterApi

db_connector = LocalDBConnector()
db = db_connector.connect()
queue_connector = LocalQueueConnector()
queue = queue_connector.connect()
# populates our dummy db with data
populate_db(db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO this should be run in a separate task, because it is a good way to decouple it,
    #  we run it here in the same memory to share the local queue
    stop_message_distributor = start_messages_distributor(db_connector=db_connector, queue_connector=queue_connector,
                                                          twitter_api=DummyTwitterApi())
    yield
    # Clean up the ML models and release the resources
    stop_message_distributor()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def handle_send_message_requests(db: DB, queue: Queue, message: RequestMessage):
    user = get_user_from_request(db, message)
    message = db.add_message(user.id, message.to_user_id, message.text)
    queue.put(message.json())
    return message


# TODO we should have authentication here, Bearer token auth will do
@app.post("/send-message/")
async def send_message(message: RequestMessage):
    handle_send_message_requests(db, queue, message)
