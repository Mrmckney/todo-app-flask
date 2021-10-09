from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
# db.init_app(app)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45))
    password = db.Column(db.String(26))

@app.route("/")
def todo_page():
    todo_list = Todo.query.all()
    return render_template('todo.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add_todo():
    todo = request.form.get("todo")
    new_todo = Todo(todo=todo, completed=False)
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
    return render_template('login.html')

@app.route("/signup")
def sign_up_page():
    return render_template('signup.html')


if __name__ == "__main__":
    db.create_all()
    app.run(port=3000)
