import secrets
from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

oauth = OAuth(app)

app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
app.config['GOOGLE_CLIENT_ID'] = "882149066733-o5cgtbi4bd3ptp26f4et6j75b6osidfl.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

app.config['GITHUB_CLIENT_ID'] = "c2ecf18e2474666ad241"
app.config['GITHUB_CLIENT_SECRET'] = "e5a9dd1be5508c18e00d735df7268c919f881620"

app.config['GITLAB_CLIENT_ID'] = "c556d35af018639e7a3a56af1c561ddee809133dfa17a9c6a1762c3a504fd59f"
app.config['GITLAB_CLIENT_SECRET'] = "3a78081ef556492eb2f487b9654f86bb32526b25fdfb030f8dff5ddbd8110fc2"

google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

github = oauth.register(
    name='github',
    client_id=app.config["GITHUB_CLIENT_ID"],
    client_secret=app.config["GITHUB_CLIENT_SECRET"],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
)

gitlab = oauth.register(
    name='gitlab',
    client_id=app.config["GITLAB_CLIENT_ID"],
    client_secret=app.config["GITLAB_CLIENT_SECRET"],
    access_token_url='https://gitlab.com/oauth/token',
    access_token_params=None,
    authorize_url='https://gitlab.com/oauth/authorize',
    authorize_params=None,
    api_base_url='https://gitlab.com/api/v4/',
)


# Default route
@app.route('/')
def index():
    return render_template('index.html')


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using google"


# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using github"


# Github login route
@app.route('/login/gitlab')
def gitlab_login():
    gitlab = oauth.create_client('gitlab')
    redirect_uri = url_for('gitlab_authorize', _external=True)
    return gitlab.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/gitlab/authorize')
def gitlab_authorize():
    gitlab = oauth.create_client('gitlab')
    token = gitlab.authorize_access_token()
    resp = gitlab.get('user').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using gitlab"


if __name__ == '__main__':
    app.run(debug=True)
