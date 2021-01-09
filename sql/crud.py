from sql.database import SessionL
from . import models

db = SessionL()


def get_user(user_id: int):
    return db.query(models.Users).filter_by(user_id=user_id).first()


def add_user(user_id: int, username: str, first_name: str, last_name: str):
    user = models.Users(user_id=user_id,
                        username=username,
                        first_name=first_name,
                        last_name=last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_notice(user_id: int, choice: str):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    user.notice = bool(int(choice))
    db.commit()
    db.refresh(user)
    return user


def get_amount_users():
    return db.query(models.Users).count()


def get_thread(thread_id: int):
    return db.query(models.Threads).filter_by(thread_id=thread_id).first()


def notice():
    return db.query(models.Users).filter_by(notice=True, disabled=False).all()


def add_thread(thread_id):
    thread = models.Threads(thread_id=thread_id)
    db.add(thread)
    db.commit()


def block(user_id):
    user = db.query(models.Users).filter_by(user_id=user_id).first()
    if user:
        user.disabled = True
        db.commit()
        db.refresh(user)
        return user
    return False
