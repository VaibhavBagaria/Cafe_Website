from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer
from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tasks(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.String(250), nullable=False)
    done = db.Column(db.String(250), nullable=False)

@app.route('/')
def home():
    # db.create_all()
    tasks=Tasks.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/', methods=['GET','POST'])
def add_task():
    task_name=request.form['name']
    date=request.form['date']
    new_task=Tasks(
        name=task_name,
        due_date=date,
        done="not done"
        )
    
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/<task>')
def delete_task(task):
    task_to_delete = Tasks.query.get(task)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)