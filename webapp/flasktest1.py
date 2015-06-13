#!/usr/bin/python

## I got started with the tips and outline from:
## https://beagle.whoi.edu/redmine/projects/ibt/wiki/Deploying_Flask_Apps_with_Apache_and_Mod_WSGI
## Together with that starter kit, the contents of this file and the associated Apache config in
##  ./celebratio are enough to get the site going.

import os
from flask import Flask, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename

## Awesome: this is what logs errors to the main apache error log!
## Uncomment for further debugging
# import logging, sys
# logging.basicConfig(stream=sys.stderr)

## And this turns on a nice debugger that, sadly, doesn't seem to work under WSGI/Apache
# from werkzeug.debug import DebuggedApplication
# application = DebuggedApplication(app, evalex=True)

import ims_legacy

UPLOAD_FOLDER = '/var/www/celebratio/apps/flasktest/ims_celebratio_uploads'
ALLOWED_EXTENSIONS = set(['tex', 'txt'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Only allow .tex and .txt files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Main point of interaction
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save the uploaded file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload biography in .tex format</title>
    <h1>Upload biography data in .tex format</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# Display contents - however, instead of displaying the TeX, we really
# would prefer to display the HTML.  There's a slight problem with the URL
# But if we can display the contents, that's at least something!
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    basename = filename.rsplit('.', 1)[0]
    htmlversion = filename.rsplit('.', 1)[0] + ".html"
    outfile = open(app.config['UPLOAD_FOLDER'] + "/" + htmlversion,'w')

    htmlcontent = "hello" 

    # print "upload folder: " + app.config['UPLOAD_FOLDER']
    htmlcontent = ims_legacy.make_one(app.config['UPLOAD_FOLDER'] + "/" + filename)

    outfile.write("<!doctype html><title>Data</title>Input: " + filename + "\nOutput: " + htmlversion + " <br><br> " + htmlcontent)
    outfile.close()

    # for demo purposes, let's just write the filename to an HTML file
    # subsequently we will put content there
    return send_from_directory(app.config['UPLOAD_FOLDER'], htmlversion)

if __name__ == '__main__':
    "Are we in the __main__ scope? Start test server."
    ## Set debug=True to debug locally, set debug=False (etc.) for production
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5000,debug=False)
