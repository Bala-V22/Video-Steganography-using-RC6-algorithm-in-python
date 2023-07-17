from flask import Flask,render_template,request
import os
from werkzeug.utils import secure_filename
from encrypt import *
from decrypt import *
from main import *
import webview


app=Flask(__name__)
# window = webview.create_window('bala', app)


@app.route('/')
def home():
    return render_template("home.html")
    
@app.route("/imghome")
def img_home():
    return render_template("img.html")  

@app.route("/vidhome")
def vid_home():
    return render_template("vid.html")  

@app.route("/image",methods=['GET', 'POST'])
def image():
    if request.method=="POST":
        key=request.form["key"]
        sentence=request.form["string"]
        file=request.files["upload"]
        
        print(key)
        print(sentence)
        print(file)
        files=file.filename
        basepath = os.path.dirname(__file__)
        print(basepath)
        file_path = os.path.join(basepath, 'uploads', secure_filename(file.filename))
        file.save(file_path)   
        print(file_path)
        esentence,message,key=main(key,sentence,files)
        # main()
        
             
    # else:
    #     key = request.args.get('key')
    #     string = request.args.get('time')
    #     file = request.args.get('Airport Names')   
    return render_template("img.html",key=key,message=message,Encrypt_Key=esentence )           

@app.route("/deimg", methods=["POST"])
def deimg():
    file=request.files["uploads"]
    key=request.form["dkey"]
    files=file.filename
    basepath = os.path.dirname(__file__)
    print(basepath)
    file_path = os.path.join(basepath, 'uploads', secure_filename(file.filename))
    file.save(file_path)
    hidden_data,sentence=dmain(key,files) 
    return render_template("img.html",hd=hidden_data,dmessage=sentence)           


@app.route("/video", methods=["POST"])
def video():
    key=request.form["vkey"]
    input_string=request.form["vstring"]
    file=request.files["vupload"]
    print(key)
    print(input_string)
    print(file)
    files=file.filename
    print(files)
    basepath = os.path.dirname(__file__)
    print(basepath)
    file_path = os.path.join(basepath, 'uploads', secure_filename(file.filename))
    file.save(file_path)   
    print(file_path)
    esentence,input_string,key=vmain(key,input_string,files)
    return render_template("vid.html",ensentence=esentence,message=input_string,key=key)       

@app.route("/devid", methods=["POST"])
def devid():
    key=request.form["vdkey"]
    file=request.files["vuploads"]
    files=file.filename
    print(files)
    basepath = os.path.dirname(__file__)
    print(basepath)
    file_path = os.path.join(basepath, 'uploads', secure_filename(file.filename))
    file.save(file_path)   
    print(file_path)
    sentence,secret_dec=decode_string(key,files)

    return render_template("vid.html",dmessage=sentence,hd=secret_dec)       


if __name__ == "__main__":
    app.run(debug=True)
    # webview.start()