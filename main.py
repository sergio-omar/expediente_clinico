#covid version
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

class Atencion_medica(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer, nullable=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    informacion_introducida_por = db.Column(db.String(20),nullable=False)
    peso = db.Column(db.Float(),nullable=False)
    altura = db.Column(db.Float(),nullable=False)
    imc = db.Column(db.Float(),nullable=False)
    ta_sistolica = db.Column(db.Float(),nullable=False)
    ta_diastolica = db.Column(db.Float(),nullable=False)
    frecuencia_cardiaca = db.Column(db.Float(),nullable=False)
    frecuencia_respiratoria = db.Column(db.Float(),nullable=False)
    temperatura = db.Column(db.Float(),nullable=False)
    padecimiento_actual = db.Column(db.Text)
    detalles_exploracion_fisica = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    nombre_del_medico = db.Column(db.String(50),nullable=False)
    cedula = db.Column(db.String(20),nullable=False)

    
class Patient(db.Model, UserMixin):
    ct = datetime.datetime.now()
    id = db.Column(db.Integer, primary_key=True)
    enter_id = db.Column(db.Integer,nullable=False,unique=True)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    names = db.Column(db.String(20),nullable=False,unique=False)
    first_lastname = db.Column(db.String(30),nullable=False,unique=False)
    second_lastname = db.Column(db.String(30),nullable=False,unique=False)
    dia_nacimiento = db.Column(db.String(3),nullable=False)
    mes_nacimiento = db.Column(db.String(3),nullable=False)
    ano_nacimiento = db.Column(db.String(5),nullable=False)
    address_street = db.Column(db.String(30),nullable=False)
    address_number = db.Column(db.String(30),nullable=False)
    address_cp = db.Column(db.String(30),nullable=False)
    address_colonia = db.Column(db.String(40),nullable=False)
    address_municipio = db.Column(db.String(40),nullable=False)
    address_estado = db.Column(db.String(40),nullable=False)
    address_pais = db.Column(db.String(40),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    prueba_covid = db.Column(db.String(20),nullable=False)
    saturacion = db.Column(db.String(5),nullable=False)
    padecimientos = db.Column(db.String(250),nullable=False)
    alergias = db.Column(db.String(40))
    persona_responsable_nombre = db.Column(db.String(50),nullable=False)
    persona_responsable_parentesco = db.Column(db.String(30),nullable=False)
    persona_responsable_tel = db.Column(db.String(15))
    persona_informante_nombre = db.Column(db.String(50),nullable=False)
    persona_informante_parentesco = db.Column(db.String(30),nullable=False)
    persona_informante_tel = db.Column(db.String(15))
    ant_heredo_familiares = db.Column(db.Boolean(),default = False)
    ant_personales_no_pat = db.Column(db.Boolean(),default = False)
    ant_personales_pat = db.Column(db.Boolean(), default = False)
    ant_pediatricos = db.Column(db.Boolean(), default = False)
    ant_gineco = db.Column(db.String(), default = False)
    somatometria = db.Column(db.Boolean(), default = False)

    #the user type will grant certain privileges
    #default false /// later the admin will accept the user
class Somatometria(db.Model, UserMixin):
    id = db.Column(db.Integer(), autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer, nullable=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    peso = db.Column(db.Float(),nullable=False)
    altura = db.Column(db.Float(),nullable=False)
    imc = db.Column(db.Float(),nullable=False)
    ta_sistolica = db.Column(db.Float(),nullable=False)
    ta_diastolica = db.Column(db.Float(),nullable=False)
    frecuencia_cardiaca = db.Column(db.Float(),nullable=False)
    frecuencia_respiratoria = db.Column(db.Float(),nullable=False)
    temperatura = db.Column(db.Float(),nullable=False)
    
class Antecedentes_personales_no_patologicos(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=True,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    religion = db.Column(db.String(30),unique=False, nullable=False)
    lugar_de_nacimiento = db.Column(db.String(40),unique=False,nullable=False)
    estado_civil = db.Column(db.String(30),unique=False,nullable=False)
    escolaridad = db.Column(db.String(30),unique=False,nullable=False)
    higiene_personal = db.Column(db.String(30),unique=False,nullable=False)
    actividad_fisica = db.Column(db.String(30),unique=False,nullable=False)
    tipo_de_actividad = db.Column(db.String(30),unique=False,nullable=True)
    frecuencia_num = db.Column(db.String(30),unique=False,nullable=True)
    frecuencia_unidad = db.Column(db.String(30),unique=False,nullable=False)
    preferencia_sexual = db.Column(db.String(30),unique=False,nullable=False)
    numero_de_parejas =db.Column(db.String(30),unique=False,nullable=False)
    grupo_sanguineo = db.Column(db.String(30),unique=False,nullable=False)
    calidad_de_alimentacion = db.Column(db.String(30),unique=False,nullable=False)
    caracteristicas_de_habitacion = db.Column(db.String(30),unique=False,nullable=False)

class Antecedentes_pediatricos(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=True,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    antecedentes_pediatricos_entrevista = db.Column(db.Text)
    
#ce = cuidado_enfermero
class Ce_diagnosticos_enfermeria(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    diagnosticos_enfermeria = db.Column(db.Text())
    resultados_esperados = db.Column(db.Text())

class Ce_prevencion_caidas(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    tipo_prevencion = db.Column(db.String(60))

class Ce_prevencion_ulceras(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    tipo_prevencion = db.Column(db.String(60))

class Ce_cuidado_heridas(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    tipo_cuidado = db.Column(db.String(60))

class Ce_cuidado_acceso(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    tipo_cuidado = db.Column(db.String(60))
    lugar_anatomico = db.Column(db.String(60))

class Ce_oxigenoterapia(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)

class Ce_constantes_vitales(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=False,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    turno = db.Column(db.String(20),unique=False,nullable=False)
    hora= db.Column(db.Integer(),unique=False)
    minuto = db.Column(db.Integer(),unique=False)
    day = db.Column(db.Integer(),unique=False)
    month = db.Column(db.Integer(),unique=False)
    year = db.Column(db.Integer(),unique=False)
    ta_sistolica = db.Column(db.Float(),unique=False)
    ta_diastolica = db.Column(db.Float(),unique=False)
    frecuencia_cardiaca = db.Column(db.Float(),unique=False)
    frecuencia_respiratoria = db.Column(db.Float(),unique=False)
    temperatura = db.Column(db.Float(),unique=False)
    oximetria = db.Column(db.Float(),unique=False)

class Antecedentes_personales_patologicos(db.Model,UserMixin):
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    enter_id = db.Column(db.Integer(),unique=True,nullable=False)
    informacion_introducida_por = db.Column(db.String(20),nullable=False,unique=False)
    enter_date = db.Column(db.DateTime, default = datetime.datetime.now)
    antecedentes_patologicos_entrevista = db.Column(db.Text) 

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

#this function will help us the get the current age of the person based on her
#day of birth
def get_age(day,month,year):
    dt = datetime.datetime.today()
    cur_day = dt.day
    cur_month = dt.month
    cur_year = dt.year
    age = cur_year - year
    print(f"day={day} month={month} year={year}")
    if cur_month < month:
        age -=1
        return age
    elif(cur_month==month and cur_day<=day):
        age -= 1
        return age
    return age

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('dashboard.html')
#routes for "Historia Clinica"
#Historia Clinica
#		-Ant. Heredo Familiares
#		-Ant. Personales No patológicos
#		-Ant. Personales Patológicos (Super larga)
#		-Ant. Pediatricos
#		-Ant. Gineco Obstétricos

@app.route('/antecedentes_heredo_familiares')
@login_required
def antecedentes_heredo_familiares():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient =  Patient.query.filter_by(enter_id = enter_id).first()
        return render_template("antecedentes_heredo_familiares.html",names=patient.names,id=patient.enter_id,first_lastname=patient.first_lastname)



@app.route('/antecedentes_personales_patologicos', methods=["GET","POST"])
@login_required
def antecedentes_persolanes_patologicos():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("antecedentes_personales_patologicos.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month)
    if request.method == 'POST':
        data = request.form
        antecedentes_patologicos = Antecedentes_personales_patologicos(enter_id = data["enter_id"],
        antecedentes_patologicos_entrevista = data["antecedentes_patologicos_entrevista"], 
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(antecedentes_patologicos)
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route('/antecedentes_pediatricos', methods=["GET","POST"])
@login_required
def antecedentes_pediatricos():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("antecedentes_pediatricos.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month)
    if request.method == 'POST':
        data = request.form
        antecedentes_pediatricos = Antecedentes_pediatricos(enter_id = data["enter_id"],
        antecedentes_pediatricos_entrevista = data["antecedentes_pediatricos_entrevista"], 
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(antecedentes_pediatricos)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route('/cuidado_enfermero', methods=["GET","POST"])
@login_required
def cuidado_enfermero():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("cuidado_enfermero.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today=today)
    if request.method == 'POST':
        data = request.form
        new_ce_diagnostico_enfermeria = Ce_diagnosticos_enfermeria(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        diagnosticos_enfermeria = data['diagnosticos_enfermeria'],
        resultados_esperados = data['resultados_esperados'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_ce_diagnostico_enfermeria)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success") 
        return redirect(url_for("cuidado_enfermero",enter_id=data["enter_id"]))

@app.route('/prevencion_caidas', methods=["GET","POST"])
@login_required
def prevencion_caidas():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("prevencion_caidas.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)
    if request.method == 'POST':
        data = request.form
        new_ce_prevencion_caidas = Ce_prevencion_caidas(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        tipo_prevencion = data['tipo_prevencion'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_ce_prevencion_caidas)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("prevencion_caidas",enter_id=data["enter_id"]))

@app.route('/prevencion_ulceras', methods=["GET","POST"])
@login_required
def prevencion_ulceras():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("prevencion_ulceras.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)
    if request.method == 'POST':
        data = request.form
        new_ce_prevencion_ulceras = Ce_prevencion_ulceras(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        tipo_prevencion = data['tipo_prevencion'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_ce_prevencion_ulceras)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("prevencion_ulceras",enter_id=data["enter_id"]))

@app.route('/cuidado_heridas', methods=["GET","POST"])
@login_required
def cuidado_heridas():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("cuidado_heridas.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)
    if request.method == 'POST':
        data = request.form
        new_ce_cuidado_heridas = Ce_cuidado_heridas(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        tipo_cuidado = data['tipo_cuidado'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_ce_cuidado_heridas)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("cuidado_heridas",enter_id=data["enter_id"]))

@app.route('/cuidado_accesos', methods=["GET","POST"])
@login_required
def cuidado_accesos():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("cuidado_accesos.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)

    if request.method == 'POST':
        data = request.form
        new_ce_cuidado_heridas = Ce_cuidado_heridas(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        tipo_cuidado = data['tipo_cuidado'],
        lugar_anatomico = data['lugar_anatomico'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_ce_cuidado_heridas)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("cuidado_accesos",enter_id=data["enter_id"]))


@app.route('/oxigenoterapia', methods=["GET","POST"])
@login_required
def oxigenoterapia():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("oxigenoterapia.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)

    if request.method == 'POST':
        data = request.form
        new_oxigenoterapia = Ce_oxigenoterapia(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_oxigenoterapia)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("oxigenoterapia",enter_id=data["enter_id"]))

@app.route('/constantes_vitales', methods=["GET","POST"])
@login_required
def constantes_vitales():
    if request.method == "GET":
        today = datetime.date.today()
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("constantes_vitales.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,today = today)
    if request.method == 'POST':
        data = request.form
        new_constantes_vitales = Ce_constantes_vitales(enter_id = data["enter_id"],
        turno = data['turno'],
        hora = data['hora'],
        minuto = data['minuto'],
        day = data["day"],
        month = data["month"],
        year = data["year"],
        informacion_introducida_por = data['informacion_introducida_por'],
        ta_sistolica = data['ta_sistolica'],
        ta_diastolica = data['ta_diastolica'],
        frecuencia_cardiaca = data['frecuencia_cardiaca'],
        frecuencia_respiratoria = data['frecuencia_respiratoria'],
        temperatura = data['temperatura'],
        oximetria = data['oximetria'])
        db.session.add(new_constantes_vitales)
        db.session.commit()
        flash("Información guardada exitosamente.","alert alert-success")
        return redirect(url_for("constantes_vitales",enter_id=data["enter_id"]))


@app.route('/antecedentes_gineco_obstetricos')
@login_required
def antecedentes_gineco_obstetricos():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient =  Patient.query.filter_by(enter_id = enter_id).first()
        return render_template("antecedentes_gineco_osbtetricos.html",names=patient.names,id=patient.enter_id,first_lastname=patient.first_lastname)
def format_spanish_month(month):
    month = int(month)
    if month == 1:
        return "Enero"
    elif month == 2:
        return "Febrero"
    elif month == 3:
        return "Marzo"
    elif month == 4:
        return "Abril"
    elif month == 5:
        return "Mayo"
    elif month == 6:
        return "Junio"
    elif month == 7:
        return "Julio"
    elif month == 8:
        return "Agosto"
    elif month == 9:
        return "Septiembre"
    elif month == 10:
        return "Octubre"
    elif month == 11:
        return "Noviembre"
    else:
        return "Diciembre"

@app.route('/somatometria',methods=['GET','POST'])
@login_required
def somatometria():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("somatometria.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month)

    if request.method == 'POST':
        data = request.form
        patient = Patient.query.filter_by(enter_id=data["enter_id"]).first()
        new_somatometria = Somatometria(enter_id = data["enter_id"],
        peso = data['peso'],
        altura = data['altura'],
        imc = data['imc'],
        ta_sistolica = data['ta_sistolica'],
        ta_diastolica = data['ta_diastolica'],
        frecuencia_cardiaca = data['frecuencia_cardiaca'],
        frecuencia_respiratoria = data['frecuencia_respiratoria'],
        temperatura = data['temperatura'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_somatometria)
        db.session.commit()
        log_action(current_user.username,"se creo somatometria del paciente: %s %s %s"%(patient.names,patient.first_lastname,patient.second_lastname))

        return redirect(url_for("dashboard"))

@app.route('/patient_dashboard',methods=['GET','POST'])
@login_required
def patient_dashboard():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        somatometria = Somatometria.query.filter_by(enter_id=enter_id).first()
        atencion_medica = Atencion_medica.query.filter_by(enter_id=enter_id).first()
        antecedentes_personales_no_patologicos = Antecedentes_personales_no_patologicos.query.filter_by(enter_id=enter_id).first()
        antecedentes_pediatricos = Antecedentes_pediatricos.query.filter_by(enter_id=enter_id).first()
        ce_diagnosticos_enfermeria = Ce_diagnosticos_enfermeria.query.filter_by(enter_id=enter_id).all()
        ce_prevencion_caidas = Ce_prevencion_caidas.query.filter_by(enter_id=enter_id).all()
        ce_prevencion_ulceras = Ce_prevencion_ulceras.query.filter_by(enter_id=enter_id).all()
        ce_cuidado_heridas = Ce_cuidado_heridas.query.filter_by(enter_id=enter_id).all()
        ce_oxigenoterapia = Ce_oxigenoterapia.query.filter_by(enter_id=enter_id).all()
        ce_constantes_vitales = Ce_constantes_vitales.query.filter_by(enter_id=enter_id).all()
        label_chart = create_label_chart(ce_constantes_vitales)
        print(label_chart)
        temp_chart = create_data_chart(ce_constantes_vitales,"temperatura")
        oximetria_chart = create_data_chart(ce_constantes_vitales,"oximetria")
        antecedentes_personales_patologicos = Antecedentes_personales_patologicos.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("patient_dashboard.html",names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month,somatometria=somatometria,atencion_medica=atencion_medica,antecedentes_personales_no_patologicos=antecedentes_personales_no_patologicos,antecedentes_pediatricos=antecedentes_pediatricos,antecedentes_personales_patologicos=antecedentes_personales_patologicos,ce_diagnosticos_enfermeria=ce_diagnosticos_enfermeria,ce_prevencion_caidas=ce_prevencion_caidas,ce_prevencion_ulceras=ce_prevencion_ulceras,ce_cuidado_heridas=ce_cuidado_heridas,ce_oxigenoterapia=ce_oxigenoterapia,ce_constantes_vitales=ce_constantes_vitales,label_chart=label_chart,temp_chart=temp_chart,oximetria_chart=oximetria_chart)

def create_label_chart(input):
    output = []
    for e in input:
        label = "`{h}:{m} {d}-{mon}`".format(h=str(e.hora).zfill(2),m=str(e.minuto).zfill(2),d=e.day,mon=e.month)
        output.append(label)
        output_string = ",".join(output)
        output_string = "["+ output_string + "]"
    return output_string

def create_data_chart(input,data):
    output = []
    for e in input:
        output.append(str(getattr(e,data)))
        output_string = ",".join(output)
        output_string = "[" + output_string +"]"
    return output_string



@app.route('/atencion_medica',methods=['GET','POST'])
@login_required
def atencion_medica():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("atencion_medica.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month)
    if request.method == 'POST':
        data = request.form
        new_atencion_medica = Atencion_medica(enter_id = data["enter_id"],
        informacion_introducida_por = data["informacion_introducida_por"],
        padecimiento_actual = data["padecimiento_actual"],
        detalles_exploracion_fisica = data["detalles_exploracion_fisica"],
        peso = data['peso'],
        altura = data['altura'],
        imc = data["imc"],
        ta_sistolica = data['ta_sistolica'],
        ta_diastolica = data['ta_diastolica'],
        frecuencia_cardiaca = data['frecuencia_cardiaca'],
        frecuencia_respiratoria = data['frecuencia_respiratoria'],
        temperatura = data['temperatura'],
        tratamiento = data["tratamiento"],
        nombre_del_medico = data["nombre_del_medico"],
        cedula = data["cedula"])
        db.session.add(new_atencion_medica)
        db.session.commit()
        return redirect(url_for("dashboard"))


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
        else:
            activated = False
        user_to_modify.active_user = activated
        db.session.commit()
        flash("Se modifico correctamente","alert alert-success")
    return render_template('manage_accounts.html',users=users)

@app.route('/patients',methods=['GET','POST'])
@login_required
def patients():
   patients = Patient.query.all()
   print(patients)
   return render_template('patients.html',patients=patients)


@app.route('/panel_paciente',methods=['GET','POST'])
@login_required
def panel_paciente():
    patient = "sergio"
    return render_template("panel_paciente.html",patient=patient)

@app.route('/antecedentes_personales_no_patologicos',methods=['GET','POST'])
@login_required
def antecedentes_personales_no_patologicos():
    if request.method == "GET":
        data = request.args
        enter_id = data.get("enter_id")
        patient = Patient.query.filter_by(enter_id=enter_id).first()
        age = get_age(int(patient.dia_nacimiento),int(patient.mes_nacimiento),int(patient.ano_nacimiento))
        enter_date = patient.enter_date
        enter_date = f"{enter_date.day} de {format_spanish_month(enter_date.month)} {enter_date.year} "
        return render_template("antecedentes_personales_no_patologicos.html", names=patient.names,enter_id=patient.enter_id,first_lastname=patient.first_lastname,gender=patient.gender,age=age,enter_date=enter_date,patient=patient,format_spanish_month=format_spanish_month)
    if request.method == 'POST':
        data = request.form
        new_antecedentes_personales_no_patologicos = Antecedentes_personales_no_patologicos(enter_id = data["enter_id"],
        religion = data['religion'],
        lugar_de_nacimiento = data['lugar_de_nacimiento'],
        estado_civil = data['estado_civil'],
        escolaridad = data['escolaridad'],
        higiene_personal = data['higiene_personal'],
        actividad_fisica = data['actividad_fisica'],
        tipo_de_actividad = data['tipo_de_actividad'],
        frecuencia_num = data['frecuencia_num'],
        frecuencia_unidad = data['frecuencia_unidad'],
        preferencia_sexual = data['preferencia_sexual'],
        numero_de_parejas = data['numero_de_parejas'],
        grupo_sanguineo = data['grupo_sanguineo'],
        calidad_de_alimentacion = data['calidad_de_alimentacion'],
        caracteristicas_de_habitacion = data['caracteristicas_de_la_habitacion'],
        informacion_introducida_por = data['informacion_introducida_por'])
        db.session.add(new_antecedentes_personales_no_patologicos)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route('/ingreso_paciente', methods=['GET','POST'])
@login_required
def ingreso():
    global patient_counter 
    patient_counter += 1
    now = datetime.datetime.now()
    date_part = str(now.minute) + str(now.hour) + str(now.day) + str(now.month) + str(now.year)
    patient_id = str(patient_counter).rjust(3,"0") + date_part
    if request.method == 'POST':
        data = request.form
        for d in data:
            print(d)
        new_patient = Patient(names=data['names'],
                enter_id = data['enter_id'],
                informacion_introducida_por = data['informacion_introducida_por'],
                first_lastname = data['first_lastname'],
                second_lastname = data['second_lastname'],
                address_street = data['address_street'],
                address_number = data['address_number'],
                address_cp = data['address_cp'],
                address_colonia = data['address_colonia'],
                address_municipio = data['address_municipio'],
                address_estado = data['address_estado'],
                address_pais = data['address_pais'],
                dia_nacimiento = data['dia_nacimiento'],
                mes_nacimiento = data['mes_nacimiento'],
                ano_nacimiento = data['ano_nacimiento'],
                gender = data['gender'],
                saturacion = data['saturacion'],
                prueba_covid = data['prueba_covid'],
                alergias = data['alergias'],
                persona_informante_nombre = data['persona_informante_nombre'],
                persona_informante_parentesco = data['persona_informante_parentesco'],
                persona_informante_tel = data['persona_informante_tel'],
                persona_responsable_nombre = data['persona_responsable_nombre'],
                persona_responsable_parentesco = data['persona_responsable_parentesco'],
                persona_responsable_tel = data['persona_responsable_tel'],
                padecimientos = data['padecimientos'])

        db.session.add(new_patient)
        db.session.commit()
        flash("Ingreso de paciente exitoso","alert alert-success")
        return redirect(url_for('patients'))

    return render_template('ingreso_paciente.html',patient_id = patient_id)

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

