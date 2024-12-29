from flask import Flask, render_template
from flask_avatars import Avatars

app = Flask(__name__)
avatars = Avatars(app)

@app.route("/")
def hello_world():
    return render_template('home.html', avatars=avatars)

if __name__ == "__main__":
    app.run(debug=True)
