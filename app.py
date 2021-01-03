from flask import Flask , render_template , request , redirect , flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    useremail = db.Column(db.String(200), nullable=False)
    userpassword = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return  "<Task %r>" % self.id



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/register')
def register():
    return render_template("registration.html")

@app.route('/allusers')
def allusers():
    AllUsers = User.query.order_by(User.date_created).all()
    return render_template("allUsers.html" ,  allusers = AllUsers)

@app.route('/registerUser' , methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        register = User(username = name, useremail = email, userpassword = hashed)

        try:
            db.session.add(register)
            db.session.commit()
            flash("You have been registered")
            return redirect("/")
        except Exception as e:
            print(e)
            return "Error occur during registration"

    else:
        return redirect("/allusers")


@app.route('/about')
def about():
    frompython = "hasnain from python file"
    list = [1,3,4,5]
    return render_template("about.html" , about = frompython , list = list)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)