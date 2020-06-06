from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
db=SQLAlchemy(app)

class Data(db.Model):
    #creating table and its field
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    idea_=db.Column(db.String(500))

    def __init__(self, email_, idea_):
        self.email_=email_
        self.idea_=idea_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        idea=request.form["idea"]
        print(email, idea)
        if db.session.query(Data).filter(Data.email_ == email).count()== 0:
            data=Data(email,idea)
            db.session.add(data)
            db.session.commit()
            send_email(email, idea)
            return render_template("success.html", text="Your idea: %s" %(idea))
    return render_template('index.html', text="Seems like we got something from that email once!")

if __name__ == '__main__':
    app.debug=True
    app.run(port=5005)
