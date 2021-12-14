from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@main_blueprint.route('/frontend/register')
def frontend_register():
    return render_template("signup.html")


@main_blueprint.route('/frontend/login')
def frontend_login():
    return render_template("signin.html")


@main_blueprint.route('/confirmed/welcome')
@login_required
def confirmed_welcome():
    if current_user.email_confirmed:
        return {"msg": "Congrats, your mail is confirmed"}, 200
    else:
        return {"error": "Mail is not confirmed, you are the teapot"}, 418
