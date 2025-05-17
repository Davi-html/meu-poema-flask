from flask import render_template, flash, redirect, url_for, request
import os
from flask_login import login_user, logout_user, current_user, login_required

from meuPoema import app, avatars, database, bcrypt
from meuPoema.forms import SignupForm, SigninForm, FormEditProfile
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

            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login sem sucesso. Verifique seus dados de acesso', 'alert-danger')

    return render_template('signin.html', formsignin=formsignin)


@app.route("/config")
@login_required
def config():
    return render_template('config.html')

@app.route("/notification")
@login_required
def notification():
    return render_template('notification.html')


@app.route("/profile")
@login_required
def profile():
    profile_pictures = url_for('static', filename='profile_pictures/' + current_user.foto_perfil)
    return render_template('profile.html', avatars=avatars, profile_pictures=profile_pictures)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'logout feito com sucesso', 'alert-success')
    return render_template('home.html', avatars=avatars)


@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    email = current_user.email
    username = current_user.username
    profile_pictures = url_for('static', filename='profile_pictures/' + current_user.foto_perfil)

    if form.validate_on_submit() and "submit" in request.form:

        if form.name.data:
            current_user.username = form.name.data

        if form.email.data:
            current_user.email = form.email.data

        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('profile'))
    return  render_template('edit_profile.html', avatars=avatars, profile_pictures=profile_pictures, form=form, email=email, username=username)


@app.route("/post/create")
@login_required
def create_post():
    pass
