from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import datetime
import os

app = Flask( __name__ )
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)


class ArrivalTime(db.Model):
    __tablename__ = "ArrivalTime"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text())
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__ (self, email):
        self.email = email


@app.route("/late", methods=["GET"])
def post_to_db():
    if not request.args.get('email'):
        return render_template('late.html', error="Bad email")
    elif request.args.get('API_KEY') == API_KEY:
        email = request.args.get('email')
        indata = ArrivalTime(email)
        db.session.add(indata)
        db.session.commit()
        return render_template('late.html', success="Success")
    else:
        return render_template('late.html', error="Bad API_KEY")

@app.route("/list", methods=["GET"])
def _slash_list():
    if request.args.get('API_KEY') == API_KEY:
        entries = ((e.email, e.time - datetime.timedelta(hours=8)) for e in ArrivalTime.query.all())
        return render_template('list.html', entries=entries)
    else:
        return render_template('list.html', error='Bad API_KEY')

if __name__ == ' __main__':
    app.debug = True
    app.run()
