from flask import Flask, render_template, flash, redirect, url_for
from flask_avatars import Avatars
from unicodedata import category
from flask_sqlalchemy import SQLAlchemy

from forms import SignupForm, SigninForm

app = Flask(__name__)
avatars = Avatars(app)

app.config['SECRET_KEY'] = '21737b39a5ceb6794d89e31a745de937'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('home.html', avatars=avatars)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    formsignup = SignupForm()

    if formsignup.validate_on_submit():
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


if __name__ == "__main__":
    app.run(debug=True)
