from flask import Flask, abort, session, request, redirect
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import os
import pathlib
from pip._vendor import cachecontrol
import google.auth.transport.requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"]= "1"

app = Flask("Google sign in")
app.secret_key = os.urandom(24)

GOOGLE_CLIENT_ID = "691256805079-57f60jv809m8godck08af0r9chn07p2r.apps.googleusercontent.com"

flow = Flow.from_client_secrets_file(client_secrets_file="client_secret.json", 
                                    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
                                    redirect_uri = "http://127.0.0.1:8080/callback")

def google_signin_required(function):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)
        else:
            return function()
    return wrapper

@app.route("/login")
def login():
    authorizaation_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorizaation_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response = request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.Session() 
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    global id_info
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session['google_id'] = id_info["email"]
    return redirect("/protected")

@app.route("/protected")
@google_signin_required
def protected():
    name = id_info["name"]
    return f"Welcome {name} to stock analyzer, Log out \n <a href='/logout'><button>Logout</button></a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return "Log in Please \n <a href='/login'><button>Login</button></a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)