from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
from datetime import datetime

app = Flask( __name__ )
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
    indata = ArrivalTime(request.form['email'])
    data = copy(indata. __dict__ )
    del data["_sa_instance_state"]
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(data)))
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))

if __name__ == ' __main__':
    app.debug = True
    app.run()
