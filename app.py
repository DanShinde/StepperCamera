
from asyncio.windows_events import NULL
from email import message
from genericpath import isdir
import stat
from flask import Flask, flash, render_template, request
import os

app = Flask(__name__)
app.secret_key = "abc" 

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
capturedFolder = 'capturedData'
CurrentDir = capturedFolder

@app.route("/")
def Display_IMG():
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    return render_template("index.html", imagelist=IMG_LIST)

@app.route('/browser')
def browse():
    itemList = os.listdir(capturedFolder)
    return render_template('browse.html', itemList=itemList)

@app.route("/home",  methods =["GET", "POST"])
def homepage():
    FolderName = "Test"
    if request.method == "POST":
       # getting input with name = fname in HTML form
       FolderName = request.form.get("FolderName")
       return "Your name is "+ FolderName 
    return render_template("home.html", FolderN = FolderName)


@app.route('/create', methods =["GET", "POST"])
def create():
    name = request.args['url1']
    print(type(name))
    newFolder = os.path.join(capturedFolder, name)
    print("inmy")
    if os.path.isdir(newFolder):
        message = "Directory already exists"
        flash(message=message)
        print(message)
    else:
        os.mkdir(newFolder)
        message = "Directory Created Sussessfully"
        print(message)
        flash(message=message)
        CurrentDir = newFolder
        print(CurrentDir)
    return render_template('home.html', forward_message=message)



@app.route('/browser/<path:urlFilePath>')
def browser(urlFilePath):
    nestedFilePath = os.path.join(capturedFolder, urlFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        print(len(itemList))
        if len(itemList) == 0:
            length = 0
            flash("Empty Directory")
        fileProperties = {"filepath": nestedFilePath}
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('browse.html', urlFilePath=urlFilePath, itemList=itemList)
    if os.path.isfile(nestedFilePath):
        fileProperties = {"filepath": nestedFilePath}
        sbuf = os.fstat(os.open(nestedFilePath, os.O_RDONLY)) #Opening the file and getting metadata
        fileProperties['type'] = stat.S_IFMT(sbuf.st_mode) 
        fileProperties['mode'] = stat.S_IMODE(sbuf.st_mode) 
        fileProperties['mtime'] = sbuf.st_mtime 
        fileProperties['size'] = sbuf.st_size 
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('file.html', currentFile=nestedFilePath, fileProperties=fileProperties, length= length) 
    return 'something bad happened'


if __name__=='__main__':
    app.run(debug=True)

