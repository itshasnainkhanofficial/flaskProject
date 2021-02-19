from flask import Flask , render_template , request , redirect , flash ,  url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    useremail = db.Column(db.String(200), nullable=False)
    userpassword = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    def __repr__(self):
        return  "<Task %r>" % self.id

class EmpModel(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     empname = db.Column(db.String(200), nullable=False)
     empfname = db.Column(db.String(200), nullable=False)
     empnumber = db.Column(db.Integer, nullable=False)
     emp_date_created = db.Column(db.DateTime , default = datetime.utcnow)
     def __repr__(self):
        return  "<Task %r>" % self.id

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route('/allusers')
def allusers():
    AllUsers = UserModel.query.order_by(UserModel.date_created).all()
    return render_template("allUsers.html" ,  allusers = AllUsers)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginUser' , methods=["GET", "POST"])
def abc():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['pass']

        user = UserModel.query.filter_by(useremail=email).first()

        if not user :
            flash("email not exists")
            return redirect(url_for("login"))
        
        else :
            if not bcrypt.checkpw(password.encode('utf-8'), user.userpassword):
                flash("password did not matched")
                return redirect(url_for("login"))

            else :
                flash("user exists")
                return redirect(url_for("allusers"))


@app.route('/register')
def register():
    return render_template("registration.html")


@app.route('/registerUser' , methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = UserModel.query.filter_by(useremail=email).first()
        if user:
            flash("User with this email already exists")
            return redirect(url_for("register"))

        register = UserModel(username = name, useremail = email, userpassword = hashed)

        try:
            db.session.add(register)
            db.session.commit()
            flash("You have been registered")
            return redirect("/viewEmployees")
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


@app.route('/manageEmployees')
def manageEmp():
    AllEmps = EmpModel.query.order_by(EmpModel.emp_date_created).all()
    return render_template("manageemp.html" ,  emps = AllEmps)


@app.route("/viewEmployees")
def viewEmp():
    employees = EmpModel.query.order_by(EmpModel.emp_date_created).all()
    return render_template("viewemp.html" ,  employees = employees)



@app.route("/addemp" ,  methods=["GET", "POST"])
def addEmployee():
    if request.method == "POST":
        empname = request.form['empname']
        empfname = request.form['empfname']
        empnumber = request.form['empnumber']

        if not empname and not empfname and not empnumber :
            flash("please add employee details to add")
            return render_template("manageemp.html")

        addedEmp = EmpModel(empname = empname, empfname = empfname, empnumber = empnumber)

        try:
            db.session.add(addedEmp)
            db.session.commit()
            flash("You have added an employee")
            return redirect("/viewEmployees")
        except Exception as e:
            print(e)
            return "Error occur during adding employees"


    else:
        flash("add employee get hit")
        return redirect("/manageEmployees")




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)