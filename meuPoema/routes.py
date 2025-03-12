from flask import render_template, flash, redirect, url_for
from meuPoema import app, avatars
from meuPoema.forms import SignupForm, SigninForm
from meuPoema.models import User
from meuPoema import database
@app.route("/")
def home():
    return render_template('home.html', avatars=avatars)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    formsignup = SignupForm()

    if formsignup.validate_on_submit():
        user = User(username=formsignup.name.data, email=formsignup.email.data, password=formsignup.password.data)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada para o e-mail {formsignup.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signup.html', formsignup=formsignup)


@app.route("/signin", methods=['GET'])
def signin():
    formsignin = SigninForm()

    if formsignin.validate_on_submit():
        flash(f'Login feito com sucesso no e-mail {formsignin.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signin.html', formsignin=formsignin)


@app.route("/notification")
def notification():
    return render_template('notification.html')


@app.route("/profile")
def profile():
    return render_template('profile.html', avatars=avatars)

