from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import datetime
import os

app = Flask( __name__ )
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
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
    email = request.args.get('email')
    indata = ArrivalTime(email)
    print(email)
    db.session.add(indata)
    db.session.commit()
    return 'Success!'

@app.route("/list", methods=["GET"])
def _slash_list():
    return "<br />".join(f"{e.email}: {e.time}" for e in ArrivalTime.query.all())

if __name__ == ' __main__':
    app.debug = True
    app.run()
