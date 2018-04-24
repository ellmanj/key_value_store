import flask
import flask_sqlalchemy
import flask_restless

# Create the Flask application and the Flask-SQLAlchemy object.
from flask import render_template
from sqlalchemy.exc import IntegrityError

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


class Entry(db.Model):
    key = db.Column(db.Unicode, primary_key=True)
    value = db.Column(db.Unicode)

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints
manager.create_api(Entry, methods=['GET', 'POST', 'DELETE'],
                   validation_exceptions=[IntegrityError])


@app.route('/')
def hello():
    return render_template('index.html')
