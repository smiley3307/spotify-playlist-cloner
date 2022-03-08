import base64
import datetime as dt

import pkce
import requests
from flask import Flask, request

import config

token_url = "https://accounts.spotify.com/api/token"
auth_url = "https://accounts.spotify.com/authorize"

client_id = config.client_id
client_secret = config.client_secret
client_credentials = f"{client_id}:{client_secret}"
b64_client_credentials = base64.b64encode(client_credentials.encode())

code_verifier = pkce.generate_code_verifier(128)
code_challenge = pkce.get_code_challenge(code_verifier)


def get_access():
    app = Flask(__name__)

    redirect_uri = "http://localhost:8888/callback"
    authorization_code = None

    # initiate the auth-flow, by requesting the authorization_code
    def get_access_code():
        scopes = ["playlist-modify-public", "playlist-modify-private",
                  "playlist-read-private", "playlist-read-collaborative", ]
        auth_params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(scopes),
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }

        res = requests.get(auth_url, params=auth_params)
        print("CLICK THE FOLLOWING URL")
        print(res.url)
        app.run(port=8888)

    # get the authorization_code from the callback
    @app.route("/callback")
    def callback():
        nonlocal authorization_code
        authorization_code = request.args["code"]
        request.environ.get("werkzeug.server.shutdown")()
        return "<h1>Authorization completed, you can close the tab.</h1>"

    # exchange the authorization_code for an authorization_token
    def get_access_token(code):
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": code_verifier,
        }
        headers = {
            "Authorization": f"Basic {b64_client_credentials.decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        res = requests.post(token_url, headers=headers, data=token_data).json()
        return res["access_token"], res["refresh_token"], dt.datetime.now() + dt.timedelta(seconds=res["expires_in"])

    get_access_code()
    return get_access_token(authorization_code)


def refresh(refresh_token):
    token_data = {
        "grant_type": "refresh_code",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }
    headers = {
        "Authorization": f"Basic {b64_client_credentials.decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    res = requests.post(token_url, headers=headers, data=token_data)
    return res["access_token"], res["refresh_token"], dt.datetime.now() + dt.timedelta(seconds=res["expires_in"])
