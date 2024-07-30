
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aladinh00-010montext'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Creating the database within the app context
with app.app_context():
    db.create_all()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=200)])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[InputRequired(), Length(min=1)])

@app.route('/')
def index():
    form = NoteForm()
    if 'user_id' in request.cookies:
        user_id = int(request.cookies.get('user_id'))
        user = User.query.get(user_id)
        if user:
            notes = user.notes
            return render_template('index.html', user=user, notes=notes, form=form)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            resp = redirect(url_for('index'))
            resp.set_cookie('user_id', str(user.id))
            return resp
        flash('Invalid username or password')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    resp = redirect(url_for('login'))
    resp.delete_cookie('user_id')
    return resp

@app.route('/add_note', methods=['POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        if 'user_id' in request.cookies:
            user_id = int(request.cookies.get('user_id'))
            user = User.query.get(user_id)
            if user:
                new_note_content = form.note.data
                new_note = Note(content=new_note_content, user=user)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added successfully')

    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' in request.cookies:
        user_id = int(request.cookies.get('user_id'))
        user = User.query.get(user_id)
        if user:
            note = Note.query.get(note_id)
            if note and note.user == user:
                db.session.delete(note)
                db.session.commit()
                flash('Note deleted successfully')

    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
