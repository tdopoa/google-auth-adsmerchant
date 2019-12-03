from flask import Flask,render_template, url_for, request, Blueprint, session
from QD_GoogleAuth import app
from authlib.client import OAuth2Session

import google_auth_oauthlib.flow
import main
import functools
import os
import flask
import google.oauth2.credentials
import googleapiclient.discovery


ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

# SCOPES FOR ADS AND SHOPPING
AUTHORIZATION_SCOPE_SHOPPING ='https://www.googleapis.com/auth/adwords https://www.googleapis.com/auth/content'

AUTH_REDIRECT_URI = 'http://localhost:8040/auth' 
BASE_URI = 'http://localhost:8040'
CLIENT_ID = '834156519600-72auja8ptu9953noij2qvmpndkp0j1eh.apps.googleusercontent.com'
CLIENT_SECRET = 'rQ_PLNpQ1wDbmC052En_oKtA'
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

bp_GoogleAuth = Blueprint('google_auth', __name__)

def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')
    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()
    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)
    return oauth2_client.userinfo().get().execute()

def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


#-----------------------------------------------------------------------------------------------
@bp_GoogleAuth.route('/getAccessToken')
def getAccessToken():
    access_token = refreshToken(client_id, client_secret, refresh_token)
    credentials = google.oauth2.credentials.Credentials(access_token)
    return None

def refreshToken(client_id, client_secret, refresh_token):
        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
        } 

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"
        r = requests.post(authorization_url, data=params)
        if r.ok:
            return r.json()['access_token']
        else:
            return None

#---------------------------------------------------------------------------------------------

@bp_GoogleAuth.route('/login', methods=['POST'])
#@no_cache
def login():
    customerId = request.form['customerId']
    flask.session['customerId'] = customerId

    session = OAuth2Session(CLIENT_ID, 
                            CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE_SHOPPING,
                            redirect_uri=AUTH_REDIRECT_URI)

    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return flask.redirect(uri, code=302)


@bp_GoogleAuth.route('/auth')
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get('state', default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response('Invalid state parameter', 401)
        return response
    
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE_SHOPPING,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
                        ACCESS_TOKEN_URI,
                        authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

    return flask.redirect(BASE_URI, code=302)



@bp_GoogleAuth.route('/logout')
@no_cache
def logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)

