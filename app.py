from genericpath import isdir
import stat
from time import sleep
#import picamera as pi_camera
import picamera 
from flask import Flask, flash, render_template, request, Response
import os
import NewSteps
app = Flask(__name__)

app.secret_key = "abc" 
camera = picamera.PiCamera()
camera.close()
IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
capturedFolder = os.path.join('static','capturedData')
CurrentDir = capturedFolder
index= 0
currentFile = 'snap'+str(index)+'.jpeg'

@app.route("/")
def Display_IMG():
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    print(IMG_LIST)
    return render_template("index.html", imagelist=IMG_LIST)

@app.route("/displayCurrFolder/<path:urlFilePath>")
def displayCurrFolder(urlFilePath):
    path = os.path.join(capturedFolder, urlFilePath)
    print(path)
    IMG_LIST = os.listdir(path)
    IMG_LIST = ['capturedData/'+urlFilePath+"/" + i for i in IMG_LIST]
    print(IMG_LIST)
    if len(IMG_LIST) ==0 :
        empt= True
    else:
        empt= False
    return render_template("index.html", imagelist=IMG_LIST, empt = empt) 

@app.route('/browser')
def browse():
    itemList = os.listdir(capturedFolder)
    return render_template('browse.html', itemList=itemList)

@app.route('/about')
def about():
    return render_template('about.html')

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
    global index
    global CurrentDir
    index=1
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

@app.route('/take_firstPic')
def take_firstPic():
    global index
    currentFile = 'snap'+str(index)+'.jpeg'
    camera= picamera.PiCamera()
    camera.rotation=180
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(3)
    currentSnap =os.path.join(CurrentDir, currentFile)
    camera.capture(currentSnap)
    print(currentSnap)
    camera.stop_preview()
    camera.close()
    index= index+1
    currentFile = 'snap'+str(index)+'.jpeg'
    index=index
    NewSteps.Rot('c')
    return render_template('home.html', currentSnap=currentSnap)

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
    app.run(host = "0.0.0.0", debug=True)

camera.stop_preview()
camera.close()