"""
Entry point of the application
"""

from flask import Flask


app = Flask(__name__)


@app.route('/hello')
def hello_world():
    """
    Returns a greeting message.
    """
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
