import logging
from flask import Flask, render_template

app = Flask(__name__)
logging.basicConfig(level = logging.INFO)
log = logging.getLogger(__name__)

@app.route('/', methods = ['GET'])
def index():
    """
    A function rendering landing page.
    """

    return render_template('index.html', error = False)
