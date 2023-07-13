from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from random import choice
from tkinter import messagebox
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
class add_cafe(FlaskForm):
    name=StringField("What name does the cafe place have?...", validators=[DataRequired()])
    image=StringField("Image url:", validators=[DataRequired(), URL()])
    
    city=StringField("In which country or city is the cafe located?", validators=[DataRequired()])
    map_url=StringField("Google map link:", validators=[DataRequired(), URL()])
    
    
    seats=StringField("Number of seats available(e.g.30-50):", validators=[DataRequired()])
    coffee_price=StringField("Coffee Price:", validators=[DataRequired()])
    
    sockets=StringField("Do they have sockets?", validators=[DataRequired()])
    toilets=StringField("Do they have toilets?", validators=[DataRequired()])
    wifi=StringField("Do they have wifi?", validators=[DataRequired()])
    calls=StringField("Can we take calls?", validators=[DataRequired()])
    submit=SubmitField("Submit")
    
show=5
is_admin=False
@app.route("/")
def home():
    global show
    show=5
    cafes=Cafe.query.all()[::-1]
    return render_template("index.html", cafes=cafes, show=show, admin=is_admin)

@app.route('/all_cafes')
def read_more():
    global show
    show+=5
    cafes=Cafe.query.all()[::-1]
    if show > len(cafes):
        show=len(cafes)
    return render_template("index.html", cafes=cafes, show=show, cafes_len=len(cafes), admin=is_admin)

@app.route('/add-cafe', methods=['GET','POST'])
def new_cafe():
    form=add_cafe()
    if form.validate_on_submit():
        if (form.sockets.data).lower() == 'yes':
            sockets=1
        else:
            sockets=0
            
        if (form.toilets.data).lower() == 'yes':
            toilets=1
        else:
            toilets=0
            
        if (form.wifi.data).lower() == 'yes':
            wifi=1
        else:
            wifi=0
            
        if (form.calls.data).lower() == 'yes':
            calls=1
        else:
            calls=0
        
        new_cafe=Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.image.data,
            location = (form.city.data).capitalize() ,
            seats = form.seats.data,
            has_toilet = toilets,
            has_wifi = wifi,
            has_sockets = sockets,
            can_take_calls = calls,
            coffee_price = form.coffee_price.data,
            )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
        
        
    return render_template("new_cafe.html", form=form)
    

@app.route('/filter', methods=['POST'])
def search():
    cafes=[]
    filter_by=request.form['filter_by']
    search=request.form['search']
    if filter_by == 'Name':
        cafes=Cafe.query.filter_by(name=search)
    else:
        cafes=Cafe.query.filter_by(location=(search).capitalize())
            
    return render_template("search.html", cafes=cafes, search=search, filter_by=filter_by)

@app.route('/delete/<cafe_id>')
def delete_cafe(cafe_id):
    
    cafe=Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
def Logout():
    global is_admin
    is_admin=False
    return redirect(url_for('home'))

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    global is_admin
    username=request.form['username']
    password=request.form['password']
    
    if username=="Vaibhav" and password=="12345":
        is_admin=True
        return redirect(url_for('home'))
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
