# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    html = open("plot.html").read()
    return html


if __name__ == '__main__':
    app.run()
