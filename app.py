
from flask import Flask, render_template
import os

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route("/")
def Display_IMG():
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    return render_template("index.html", imagelist=IMG_LIST)

@app.route("/home")
def homepage():
    
    return render_template("home.html")


if __name__=='__main__':
    app.run(debug=True)

