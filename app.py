from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/')
# def hello():
#     return "<p>Hello James! I love you!</p>"

@app.route('/')
def index():
    return render_template('index.html')