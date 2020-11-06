from flask import render_template, url_for, redirect, flash
from app import app
from app.forms import LoginForm

@app.route("/")
def index():
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    # user = {'username': 'Lucie'}
    form = LoginForm()
    # form validate on submit process the form
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.email.data))
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)



@app.route("/register")
def register():
    return render_template('register.html', title='Registration')

@app.route("/home")
def home():
    user = {'email': 'Lucie'}
    return render_template('home.html', title='home', user=user)


@app.route("/test")
def test():
    return app.config['SECRET_KEY']