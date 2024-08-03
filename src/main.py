import logging
from flask import Flask, redirect, request, render_template, session, url_for

app = Flask(__name__)
logging.basicConfig(level = logging.INFO)
log = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    A function rendering landing page.
    """

    if request.method == 'GET':
        try:
            # Render landing page
            return render_template('index.html', error = False)
        except Exception as e:
            log.error(f"Exception: {e}")
    
    return render_template('login.html',error = False)