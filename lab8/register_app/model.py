import datetime
import math
from random import random

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    email_confirmed = db.Column(db.Boolean, default=False)
    one_time_passwords = db.ForeignKey("OTPModel", backref="user", lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def db_insert(self):
        db.session.add(self)
        db.session.commit()

    def confirm_mail(self):
        self.email_confirmed = True
        db.session.commit()

    def verify_password_hash(self, enter_password):
        return check_password_hash(self.password, enter_password)


class OTPModel(db.Model):
    OTP_LEN = 64

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    otp = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    def __init__(self):
        self.otp = self.__generate_otp()

    def db_insert(self, user):
        self.user_id = user.id
        db.session.add(self)
        db.session.commit()

    def __generate_otp(self):
        charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        otp = ""
        for _ in range(self.OTP_LEN):
            otp += charset[math.floor(random() * len(charset))]

        return otp
