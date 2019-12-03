
"""
This script runs the QD_GADS application using a development server.
"""

from os import environ
from QD_GoogleAuth import app


if __name__ == '__main__':

    """
    HOST = environ.get('HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('PORT', '8040'))
    except ValueError:
        PORT = 8040
    app.run(HOST, PORT)
    """

    app.run()
