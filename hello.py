import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from subprocess import call
import subprocess,re 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

sudoPassward ='2502'
command =['sudo', 'python', '/usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py' ]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyse_image(file_name):
   	p1=subprocess.Popen(['sudo','python', '/usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py','--image_file', file_name ],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	l=p1.communicate()[0]
	print l
	b = l.split('\n')
	z="{"
	for line in b:
	    for word in line.split(','):
		obj = re.match('(.+\(.+\))', word)
		if(obj):
		     l=obj.group().split('(')
		     return l[0]
		     
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    h=analyse_image(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return h
	     #return redirect(url_for('upload_file',
             #                       filename=filename))
    return '''
<!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
