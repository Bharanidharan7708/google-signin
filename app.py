from flask import Flask, abort, session, request, redirect
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import os
import pathlib
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google sign in")

@app.route("/login")
def login():
    return "login Page"

@app.route("/callback")
def callback():
    return "call back"

@app.route("/protected")
def protected():
    return "Protected Page"

@app.route("/logout")
def logout():
    return "logged out"

@app.route("/")
def index():
    return "Success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)