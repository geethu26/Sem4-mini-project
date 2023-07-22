from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy



app= Flask(__name__)

    

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookticket.db'
db = SQLAlchemy(app)

class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       fname = db.Column(db.String(80), nullable=False)
       lname = db.Column(db.String(80), nullable=False)
       phone = db.Column(db.String(80), nullable=False)
       email = db.Column(db.String(80),  nullable=False)
       gender= db.Column(db.String(80), nullable=False)
       time = db.Column(db.String(120), nullable=False)
       date = db.Column(db.String(120),  nullable=False)    
       age = db.Column(db.String(120),  nullable=False)
       time = db.Column(db.String(10), nullable=False)
       numt = db.Column(db.Integer , nullable=False)
       child = db.Column(db.Integer,  nullable=False)
       adult = db.Column(db.Integer,  nullable=False)
SQLAlchemy.create_all()



def __repr__(self):
            return '<User %r>' % self.fname


@app.route("/form",methods=['GET','POST'])
def form():
         if request.method=='POST':
                    pass
         return render_template("form.html")


@app.route("/",methods=['GET','POST'])
def home():
        return render_template("Home.html")


if __name__ =="__main__":
             app.run(debug = True)


    