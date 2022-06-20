from app import db


class Notification(db.Model):
    __tablename__ = "notification"
  
    subscriber_username = db.Column(db.String(100), nullable=False, primary_key=True)
    observed_username = db.Column(db.String(100), nullable=False, primary_key=True)

    def __init__(self, fields: dict) -> None:
    # merge dictionaries
        self.__dict__ = {**self.__dict__, **fields}

class SocketConnection(db.Model):
    __tablename__ = "socker_connections"

    username = db.Column(db.String(100), primary_key=True)
    connection_id = db.Column(db.String(100), nullable=False)

    def __init__(self, fields: dict) -> None:
    # merge dictionaries
        self.__dict__ = {**self.__dict__, **fields}