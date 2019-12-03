from flask import Flask,render_template, url_for, request
from QD_GoogleAuth import app

import os
import main
import flask
import functools
import google_auth
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow

from google_auth import bp_GoogleAuth
from oauthlib.oauth2 import WebApplicationClient

app.register_blueprint(bp_GoogleAuth)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        return render_template('logout.html');
        #user_info = google_auth.get_user_info()
        #return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return render_template('quartile_googleAuth.html');
    #return flask.redirect('/google/login')


@app.route('/home')
def home():
    return flask.redirect('/google_auth/google/login')
    #return render_template('quartile_googleAuth.html');
