from flask import Flask
from flask import render_template, url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager,login_required,logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import datetime
#create an application
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'expedienteClinicokey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#global variables:
patient_counter = 0

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(init(user_id))

#scheme
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    #the user type will grant certain privileges
    user_type = db.Column(db.String(20),nullable=False)
    #default false /// later the admin will accept the user
    active_user = db.Column(db.Boolean(),nullable=False)

#probably we wont use them
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4,max=20)],render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4,max=20)],render_kw={"placeholder":"Password"})
    submit = SubmitField("Register")
    user_type = StringField(validators=[InputRequired(),Length(min=4,max=20)],
            render_kw ={"placeholder":"Tipo de usuario"})
    def validate_username(self,username):
        existing_user_username=User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That user already exist, please choose a different one")
#we wont use this kind of forms, adds load to the backend
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4,max=20)],render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4,max=20)],render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/ingreso_paciente',methods=['GET','POST'])
def ingreso():
    global patient_counter 
    patient_counter += 1
    now = datetime.datetime.now()
    date_part = str(now.minute) + str(now.hour) + str(now.day) + str(now.month) + str(now.year)
    patient_id = str(patient_counter).rjust(3,"0") + date_part
    return render_template('ingreso_paciente.html',patient_id = patient_id)

@app.route('/login',methods=['GET','POST'])
def login():
  #  form = LoginForm()
  #  if form.validate_on_submit():
  #      user = User.query.filter_by(username=form.username.data).first()
  #      if user:
  #          if bcrypt.check_password_hash(user.password,form.password.data):
  #              return redirect(url_for('dashboard'))
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user:
            print('the user is' + user.username)
            print(user.password)
            print(data['password'])
            if bcrypt.check_password_hash(user.password,data['password']):
                return redirect(url_for('dashboard'))


    return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form
        print(data)
        new_user = User(username=data['username'],
                password = bcrypt.generate_password_hash(data['password']),
                user_type= data['user_type'],
                active_user = False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
#    form = RegisterForm()
#    if form.validate_on_submit():
#        hashed_password = bcrypt.generate_password_hash(form.password.data)
#        new_user = User(username=form.username.data, 
#                password=hashed_password,
#                user_type=form.user_type.data,
#                active_user=False)
#
#        db.session.add(new_user)
#        db.session.commit()
#        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

