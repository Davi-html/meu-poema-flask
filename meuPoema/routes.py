from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from meuPoema import app, avatars, database, bcrypt
from meuPoema.forms import SignupForm, SigninForm
from meuPoema.models import User

@app.route("/")
def home():
    return render_template('home.html', avatars=avatars)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    formsignup = SignupForm()

    if formsignup.validate_on_submit() and "submit" in request.form:
        crypt_password = bcrypt.generate_password_hash(formsignup.password.data)
        user = User(username=formsignup.name.data, email=formsignup.email.data, password=crypt_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada para o e-mail {formsignup.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signup.html', formsignup=formsignup)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    formsignin = SigninForm()

    if formsignin.validate_on_submit():
        user = User.query.filter_by(email=formsignin.email.data).first()

        if user and bcrypt.check_password_hash(user.password, formsignin.password.data):
            login_user(user, remember=formsignin.rememberPassword.data)
            flash(f'Login feito com sucesso no e-mail {formsignin.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Login sem sucesso. Verifique seus dados de acesso', 'alert-danger')

    return render_template('signin.html', formsignin=formsignin)


@app.route("/config")
def config():
    return render_template('config.html')

@app.route("/notification")
def notification():
    return render_template('notification.html')


@app.route("/profile")
def profile():
    return render_template('profile.html', avatars=avatars)


@app.route("/logout")
def logout():
    logout_user()
    flash(f'logout feito com sucesso', 'alert-success')
    return render_template('home.html', avatars=avatars)

@app.route("/post/create")
def create_post():
    pass
