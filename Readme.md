# Idea
The task this repo is solving is the following
1) We have a messaging platform in our system, chat between 2 users, where they can send message to each other
2) When one user sends message through our api to another one, we save it in the database and also output on our social platforms, Twitter for now
3) We write on Twitter that a user got a message and also sent a message

## Limitations
1) db is in memory
2) queue is in memory
3) Twitter api is dummy
4) dummy authentication
5) little tests coverage with only 1 integration tests
6) various shortcuts along the way


## Architecture
1) Fast API Rest endpoint `/send-message/` that accepts a user to whom send the message and text
2) message ends up in the database and in the queue
3) queue consumer run as a background thread and reads from the queue
4) social outputs (only Twitter for now) react to all the message on the queue and write to the respective destinations


## Setup
### Requirements
1) Python 3.11 (3.7+ should work fine)
2) Pipenv 2023.2.18
### Start
`pipenv install`
`uvicorn main:app --reload`
### Tests
`python -m unittest`