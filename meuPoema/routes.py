import os
import secrets
from PIL import Image

from sqlalchemy import func

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from meuPoema import app, avatars, database, bcrypt
from meuPoema.forms import SignupForm, SigninForm, FormEditProfile, FollowForm, SaveConfig, FormPost, FormCriarPost
from meuPoema.models import User, Post, Follow, Notification, Messages


@app.route("/", methods=['GET', 'POST'])
def home():
    rank = lista_rank()
    formCriarPost = FormCriarPost()

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    profile_pictures = url_for('static', filename='profile_pictures/')

    if formCriarPost.validate_on_submit() and "criarPost" in request.form:
        if current_user.is_authenticated:
            return redirect(url_for('postPoem'))
        else:
            flash('Você precisa estar logado para criar um poema', 'alert-danger')

    return render_template('home.html', avatars=avatars, rank=rank, formCriarPost=formCriarPost, posts=posts, current_user=current_user, profile_pictures=profile_pictures, get_user=get_user)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    formsignup = SignupForm()
    rank = lista_rank()
    if formsignup.validate_on_submit():
        crypt_password = bcrypt.generate_password_hash(formsignup.password.data)
        user = User(username=formsignup.name.data, email=formsignup.email.data, password=crypt_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada para o e-mail {formsignup.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signup.html', formsignup=formsignup, rank=rank)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    formsignin = SigninForm()
    rank = lista_rank()
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

    return render_template('signin.html', formsignin=formsignin, rank=rank)


@app.route("/config", methods=['GET', 'POST'])
@login_required
def config():
    rank = lista_rank()
    saveConfig = SaveConfig()

    if saveConfig.validate_on_submit() and "submit" in request.form:
        current_user.configNotifications = saveConfig.checkboxNotifications.data
        current_user.configRanking = saveConfig.checkboxRanking.data
        database.session.commit()
        flash(f'Configurações salvas com sucesso', 'alert-success')
        return redirect(url_for('config'))

    if current_user.configNotifications:
        saveConfig.checkboxNotifications.data = True
    else:
        saveConfig.checkboxNotifications.data = False

    if current_user.configRanking:
        saveConfig.checkboxRanking.data = True
    else:
        saveConfig.checkboxRanking.data = False

    return render_template('config.html', rank=rank, saveConfig=saveConfig)

@app.route("/notification")
@login_required
def notification():
    notification = Notification.query.filter_by(recever_id=current_user.id).order_by(Notification.date_created.desc()).all()
    rank = lista_rank()
    return render_template('notification.html', notification=notification, current_user=current_user, rank=rank)

@app.route("/profile/<int:id>", methods=['GET', 'POST'])
@login_required
def profile(id):
    id = id
    rank = lista_rank()
    user = User.query.filter_by(id=id).first()
    followers = Follow.query.filter_by(followed_id=user.id).all()
    following = Follow.query.filter_by(follower_id=user.id).all()
    post = Post.query.filter_by(user_id=id).order_by(Post.date_posted.desc()).all()
    followform = FollowForm()

    profile_pictures = url_for('static', filename='profile_pictures/' + user.foto_perfil)

    is_following = False
    if current_user.is_authenticated:
        is_following = database.session.query(Follow).filter_by(
            follower_id=current_user.id,
            followed_id=user.id
        ).first() is not None

    if followform.validate_on_submit() and "follow" in request.form:
        if user.id != current_user.id:
            for follow in Follow.query.all():
                if follow.follower_id == current_user.id and follow.followed_id == user.id:
                    flash(f'Você já segue {user.username}', 'alert-danger')
                    return redirect(url_for('profile', id=user.id))

            follow = Follow(follower_id=current_user.id, followed_id=user.id)
            database.session.add(follow)
            database.session.commit()

            notification = Notification(recever_id=user.id, sender_id=current_user.id, message=f'comecou a seguir voce', is_read=False)

            # Verifica se a notificação já existe
            existing_notification = Notification.query.filter_by(
                recever_id=user.id,
                sender_id=current_user.id
            ).first()

            if existing_notification:
                flash(f'{current_user.username} começou a seguir {user.username}', 'alert-danger')
                return redirect(url_for('profile', id=user.id))
            else:
                database.session.add(notification)
                database.session.commit()
            flash(f'{current_user.username} começou a seguir {user.username}', 'alert-danger')
            return redirect(url_for('profile', id=user.id))
        else:
            flash(f'Você não pode seguir a si mesmo', 'alert-danger')

    if followform.validate_on_submit() and "unfollow" in request.form:
        if user.id != current_user.id:
            for follow in Follow.query.all():
                if follow.follower_id == current_user.id and follow.followed_id == user.id:
                    database.session.delete(follow)
                    database.session.commit()
                    flash(f'{current_user.username} deixou de seguir {user.username}', 'alert-danger')
                    return redirect(url_for('profile', id=user.id))
        else:
            flash(f'ocê não pode deixar de seguir a si mesmo', 'alert-danger')

    return render_template('profile.html', avatars=avatars, profile_pictures=profile_pictures, user=user, post=post, followform=followform, following=following, followers=followers, is_following=is_following, rank=rank)

def lista_rank():
    rank = (database.session.query(User)
            .outerjoin(User.followers)
            .group_by(User.id)
            .order_by(func.count(User.followers).desc())
            .limit(5)
            .all())
    return rank
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
    rank = lista_rank()

    if form.validate_on_submit() and "submit" in request.form:
        current_user.username = form.name.data
        current_user.email = form.email.data

        if form.foto_perfil.data:
            name_image = save_image(form.foto_perfil.data)
            current_user.foto_perfil = name_image

        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('profile', id=current_user.id))
    return  render_template('edit_profile.html', profile_pictures=profile_pictures, form=form, email=email, username=username, rank=rank)

@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def postPoem():
    formPost = FormPost()
    rank = lista_rank()

    if formPost.validate_on_submit() and "submit" in request.form:
        if current_user.is_authenticated:
            post = Post(title=formPost.title.data, content=formPost.content.data, user_id=current_user.id)
            database.session.add(post)
            database.session.commit()
            flash(f'Poema criado com sucesso', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Você precisa estar logado para criar um poema', 'alert-danger')
    return render_template('postPoem.html', current_user=current_user, avatars=avatars, rank=rank, formPost=formPost)


def get_user(user_id):
    return User.query.get(user_id)


@app.route("/profile/<int:id>/followers")
@login_required
def followers(id):
    user = User.query.filter_by(id=id).first()
    user_followers = Follow.query.filter_by(followed_id=user.id).all()

    return render_template('followers.html', user=user, user_followers=user_followers, get_user=get_user)

@app.route("/profile/<int:id>/following")
@login_required
def following(id):
    user = User.query.filter_by(id=id).first()
    user_following = Follow.query.filter_by(follower_id=user.id).all()

    return render_template('following.html', user=user, user_following=user_following, get_user=get_user)

@app.route("/message")
@login_required
def messagePage():
    rank = lista_rank()

    message = Messages.query.order_by(Messages.date_created.desc()).all()
    return render_template('messagePage.html', rank=rank, message=message, current_user=current_user, get_user=get_user)