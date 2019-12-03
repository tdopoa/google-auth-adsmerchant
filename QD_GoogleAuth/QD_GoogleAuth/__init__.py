from flask import Flask, session
app = Flask(__name__)

app.secret_key = 'QUARTILEGOOGLEAUTH'

import QD_GoogleAuth.views
