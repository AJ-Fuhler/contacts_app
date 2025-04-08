import secrets
from flask import (Flask,
                   g,
                   redirect,
                   redirect,
                   render_template,
                   session,
                   url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def is_authenticated():
    return 'user_id' in session

from contacts.database_persistence import DatabasePersistence

@app.before_request
def load_storage():
    g.storage = DatabasePersistence()

@app.route("/")
def index():
    if not is_authenticated():
        return redirect(url_for('signin'))
    

@app.route("/signin", methods=['GET'])
def signin():
    if is_authenticated():
        return redirect(url_for('index'))
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)