from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
from datetime import datetime
import os

app = Flask( __name__ )
app.config.from_object(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)


class ArrivalTime(db.Model):
    __tablename__ = "ArrivalTime"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text())
    time = db.Column(db.DateTime())

    def __init__ (self, email):
        self.email = email
        self.time = datetime.now()


@app.route("/late", methods=["GET"])
def post_to_db():
    email = request.args.get('email')
    indata = ArrivalTime(email)
    print(email)
    db.session.add(indata)
    db.session.commit()
    return 'Success!'

if __name__ == ' __main__':
    app.debug = True
    app.run()
