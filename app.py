from flask import Flask, redirect, url_for, render_template, request
from flask.globals import session
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
engine = create_engine('sqlite:///book.sqlite')

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(120))
    date = db.Column(db.String())
    completed = db.Column(db.Boolean)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(26), unique=True, nullable=False)
    

@app.route("/")
def home_page():
    return render_template("base.html")

@app.route("/todo")
def todo_page():
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list)

@app.route("/date")
def todo_date():
    todo_list = Todo.query.order_by(Todo.date).all()
    return render_template("todo.html", todo_list=todo_list)

@app.route("/completed")
def todo_completed():
    todo_list = Todo.query.order_by(Todo.completed.desc()).all()
    return render_template("todo.html", todo_list=todo_list)

@app.route("/notcompleted")
def todo_notcompleted():
    todo_list = Todo.query.order_by(Todo.completed).all()
    return render_template("todo.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add_todo():
    todo = request.form.get("todo")
    todo_date = request.form.get("date")
    new_todo = Todo(todo=todo, date=todo_date ,completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo_page"))

@app.route("/update/<int:todo_id>")
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("todo_page"))

@app.route("/remove/<int:todo_id>")
def remove_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo_page"))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def sign_up_page():
    return render_template("signup.html")

@app.route("/register/", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    session["logged_in"] = True 
    return render_template("todo.html") and redirect(url_for("todo_page"))

@app.route("/login/", methods = ["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
            session["logged_in"] = True 
            return render_template("todo.html") and redirect(url_for("todo_page"))
        else:
            flash("Username or Password Incorrect", 'Danger')
            return redirect(url_for("login_page"))
    return render_template("todo.html")

@app.route("/logout/")
def logout():
    session["logged_in"] = False
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    db.create_all()
    app.run(port=3000)
