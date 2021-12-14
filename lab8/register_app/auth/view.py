import datetime
import threading

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from register_app.model import UserModel, OTPModel

mail = Mail()
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def send_mail(user):
    otp_model = OTPModel()
    msg = Message(subject="Register Confirmation",
                  body=f"Confirmation Link: http://127.0.0.1:5000/auth/email/{otp_model.otp}",
                  sender="japandomitori@gmail.com", recipients=[user.email])
    mail.send(msg)
    otp_model.db_insert(user)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if UserModel.query.filter_by(email=email).first():
        return {"error": "User with this email already exist"}, 400

    if UserModel.query.filter_by(username=username).first():
        return {"error": "User with this username already exist"}, 400

    if UserModel.query.filter_by(password=password).first():
        return {"error": "User with this password already exist"}, 400

    user = UserModel(username, email, password)
    user.db_insert()

    thread = threading.Thread(target=send_mail, args=(user,))
    thread.run()

    return {"msg": f"{user.username} is almost created. Please confirm creation in your mailbox"}, 200


@auth_blueprint.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = UserModel.query.filter_by(email=email).first()
    if user and user.verify_password_hash(password):
        login_user(user, duration=datetime.timedelta(minutes=3))
    else:
        return {"error": "Such user does not exist"}, 400

    return {"msg": f"{user.username} was logged in successfully"}


@auth_blueprint.route("/email/<string:token>")
def confirm_email(token):
    confirm_otp = OTPModel.query.filter_by(otp=token, user_id=current_user.id).first()

    if not confirm_otp:
        return {"error": "No such otp, please register"}, 400

    if current_user.email_confirmed:
        return {"msg": "Your email is already confirmed"}, 200

    if (datetime.datetime.now() - confirm_otp.creation_date) > datetime.timedelta(minutes=10):
        return {"error": "This OTP was deactivated"}, 400
    else:
        current_user.confirm_mail()
        return {"msg": "Mail was confirmed successfully"}, 200
