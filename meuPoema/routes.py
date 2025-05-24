import os
import secrets
from PIL import Image

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from meuPoema import app, avatars, database, bcrypt
from meuPoema.forms import SignupForm, SigninForm, FormEditProfile
from meuPoema.models import User

@app.route("/")
def home():
    listaRankUsers = User.query.order_by(User.followers.desc()).limit(10).all()
    return render_template('home.html', avatars=avatars, listaRankUsers=listaRankUsers)


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
    listaRankUsers = User.query.order_by(User.followers.desc()).limit(10).all()
    return render_template('config.html', listaRankUsers=listaRankUsers)

@app.route("/notification")
@login_required
def notification():
    listaRankUsers = User.query.order_by(User.followers.desc()).limit(10).all()
    return render_template('notification.html', listaRankUsers=listaRankUsers)


@app.route("/profile/<int:id>")
@login_required
def profile(id):
    id = id
    user = User.query.filter_by(id=id).first()
    listaRankUsers = User.query.order_by(User.followers.desc()).limit(10).all()
    profile_pictures = url_for('static', filename='profile_pictures/' + user.foto_perfil)
    return render_template('profile.html', avatars=avatars, profile_pictures=profile_pictures, user=user, listaRankUsers=listaRankUsers)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'logout feito com sucesso', 'alert-success')
    return render_template('home.html', avatars=avatars)


def save_image(imagem):
    random_hex = secrets.token_hex(8)
    nome, ext = os.path.splitext(imagem.filename)
    name_imagem = nome + random_hex + ext
    caminho = os.path.join(app.root_path, 'static/profile_pictures', name_imagem)
    output_size = (300, 300)
    image_resize = Image.open(imagem)
    image_resize.thumbnail(output_size)
    image_resize.save(caminho)
    return name_imagem

@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    email = current_user.email
    username = current_user.username
    profile_pictures = url_for('static', filename='profile_pictures/' + current_user.foto_perfil)

    if form.validate_on_submit() and "submit" in request.form:
        current_user.username = form.name.data
        current_user.email = form.email.data

        if form.foto_perfil.data:
            name_image = save_image(form.foto_perfil.data)
            current_user.foto_perfil = name_image

        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('profile', id=current_user.id))
    return  render_template('edit_profile.html', profile_pictures=profile_pictures, form=form, email=email, username=username)


@app.route("/post/create")
@login_required
def create_post():
    pass
