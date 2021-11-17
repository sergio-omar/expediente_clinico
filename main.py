from flask import Flask
from flask import render_template, url_for, redirect,request, flash
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
#login_manager.login_view = "login"
login_manager.login_message = "Necesitas iniciar sesión."
login_manager.login_message_category = "alert alert-danger"
#global variables:
patient_counter = 0

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#scheme
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    user_names = db.Column(db.String(20),nullable=False,unique=False)
    user_first_lastname=db.Column(db.String(20),nullable=False,unique=False)
    user_second_lastname=db.Column(db.String(20),nullable=True,unique=False)
    password = db.Column(db.String(80),nullable=False)
    set_new_password = db.Column(db.Boolean(),nullable=False)
    #the user type will grant certain privileges
    user_type = db.Column(db.String(20),nullable=False)
    user_cedula = db.Column(db.String(20),nullable=True)
    #default false /// later the admin will accept the user
    active_user = db.Column(db.Boolean(),nullable=False)
    created_by = db.Column(db.String(80),nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Log(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30),unique=False,nullable=False)
    user_action = db.Column(db.String(200),unique=False,nullable=False)
    log_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    enter_id = db.Column(db.Integer,nullable=False,unique=True)
    enter_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    names = db.Column(db.String(20),nullable=False,unique=False)
    first_lastname = db.Column(db.String(20),nullable=False,unique=False)
    second_lastname = db.Column(db.String(20),nullable=False,unique=False)
    gender = db.Column(db.String(20),nullable=False)
    #the user type will grant certain privileges
    #default false /// later the admin will accept the user

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
    return render_template('dashboard.html')

@app.route('/antecedentes_heredofamiliares',methods=['GET','POST'])
def antecedentes_heredofamiliares():
    return render_template('antecedentes_heredofamiliares.html')

@app.route('/manage_accounts',methods=['GET','POST'])
@login_required
def manage_accounts():
    users = User.query.all()
    if request.method == "POST":
        data = request.form
        activated = False
        user_to_modify = User.query.filter_by(username=data["username"]).first()
        print("this is the name that is going to be modified")
        print(user_to_modify.username)
        if data["user_activated"] == "true":
            activated = True
            print("------------The user is now activated ------")
        else:
            activated = False
            print("-----The user is DESACTIVATED----")
        user_to_modify.active_user = activated
        db.session.commit()
        flash("Se modifico correctamente","alert alert-success")
    return render_template('manage_accounts.html',users=users)

@app.route('/ingreso_paciente',methods=['GET','POST'])
@login_required
def ingreso():
    global patient_counter 
    patient_counter += 1
    now = datetime.datetime.now()
    date_part = str(now.minute) + str(now.hour) + str(now.day) + str(now.month) + str(now.year)
    patient_id = str(patient_counter).rjust(3,"0") + date_part
    return render_template('ingreso_paciente.html',patient_id = patient_id)
    if request.method == 'POST':
        data = request.form
        new_patient = Patient(names=data['names'],
                enter_id = data['enter_id'],
                first_lastname = data['first_lastname'],
                second_lastname = data['second_lastname'],
                gender =data['gender'])

        db.session.add(new_Patient)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/set_new_password',methods=['GET','POST'])
@login_required
def set_new_password():
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        data = request.form
        if bcrypt.check_password_hash(current_user.password,data['user_temporal_password']):
            print('yea this is the password')
            user.password = bcrypt.generate_password_hash(data['user_new_password'])
            user.set_new_password = True
            db.session.commit()
            log_action(current_user.username,"Ha cambiado de passowrd.")
            flash("Cambio de contraseña exitoso","alert alert-success")
            return render_template('dashboard.html')

    return render_template('set_new_password.html')


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
            if bcrypt.check_password_hash(user.password,data['password']):
                login_user(user)
                if current_user.set_new_password == False:
                    return render_template('set_new_password.html')
                log_action(current_user.username,"Inició sesión")
                return redirect(url_for('dashboard'))
            else:
                flash("Password incorrecto","alert alert-danger")
        else:
            flash("Nombre de usuario incorrecto","alert alert-danger")
    return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if current_user.is_authenticated:
        log_action(current_user.username,"Cerro su sesión.")
        logout_user()
        flash("Tu sesión fue cerrada exitosamente.","alert alert-success")
        return redirect(url_for('login'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

#This route is for the log
@app.route('/log',methods=['GET','POST'])
@login_required
def log():
    if current_user.username == "Administrador":
        logs = Log.query.limit(100).all()
        return render_template('log.html',logs=logs)

def log_action(user,user_action):
    new_enter_log = Log(user=user,
            user_action = user_action)
    db.session.add(new_enter_log)
    db.session.commit()

#This route will take us to two types of register
@app.route('/register',methods=['GET','POST'])
@login_required
def register():
    if request.method == 'POST':
        data = request.form
        new_user = User(username=data['username'],
                user_names = data['user_names'],
                user_first_lastname = data['user_first_lastname'],
                user_second_lastname = data['user_second_lastname'],
                password = bcrypt.generate_password_hash(data['password']),
                user_type= data['user_type'],
                set_new_password = False,
                user_cedula = data['user_cedula'],
                created_by = data['created_by'],
                active_user = False)
        db.session.add(new_user)
        db.session.commit()
        log_action(current_user.username,"se creo la cuenta con nombre: %s y con privilegios tipo: %s"%(new_user.username,new_user.user_type))
        flash('El usuario fue creado correctamente','alert alert-success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/register_admin',methods=['GET','POST'])
def register_admin():
    if request.method == 'POST':
        data = request.form
        new_user = User(username=data['username'],
                user_names = data['user_names'],
                user_first_lastname = data['user_first_lastname'],
                user_second_lastname = data['user_second_lastname'],
                password = bcrypt.generate_password_hash(data['password']),
                user_type= data['user_type'],
                set_new_password = False,
                created_by = data['created_by'],
                active_user = False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register_admin.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

