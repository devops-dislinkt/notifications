from typing import Optional
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app import db

def get_all(model):
    data = model.query.all()
    return data


def create(instance: db.Model):
    ret = db.session.merge(instance)
    commit_changes()
    return ret


def delete_instance(instance):
    db.session.delete(instance)
    commit_changes()

def commit_changes():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(e)
