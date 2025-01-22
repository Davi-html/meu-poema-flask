from flask import Flask, render_template
from flask_avatars import Avatars
from forms import SignupForm, SigninForm

app = Flask(__name__)
avatars = Avatars(app)

app.config['SECRET_KEY'] = '21737b39a5ceb6794d89e31a745de937'

@app.route("/")
def home():
    return render_template('home.html', avatars=avatars)


@app.route("/signup")
def signup():
    formsignup = SignupForm()
    return render_template('signup.html', formsignup=formsignup)


@app.route("/signin")
def signin():
    formsignin = SigninForm()
    return render_template('signin.html', formsignin=formsignin)


@app.route("/notification")
def notification():
    return render_template('notification.html')


if __name__ == "__main__":
    app.run(debug=True)
