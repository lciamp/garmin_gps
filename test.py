import time
from lxml import objectify
from datetime import datetime
from flask import Flask, render_template, url_for, redirect
from forms import UploadForm
from garmin import GarminParser
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os

#namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

# example data
Austin = 'activity_2506525849.tcx'
Brooklyn = 'activity_2710384216.tcx'
NYC = 'activity_2298934172.tcx'
Garmin = 'garmin.tcx'

# flask app quick setup
bootstrap = Bootstrap()

app = Flask(__name__)
bootstrap.init_app(app)
app.config['UPLOAD_FOLDER'] = "./files/"
app.config['WTF_CSRF_SECRET_KEY'] = 'o8gyuvkghqwfaeber'
app.config['SECRET_KEY'] = 'ajhdsfglasdflj'

file = app.config['UPLOAD_FOLDER'] + Brooklyn

'''
myFile = GarminParser(file)
track = myFile.points
center = myFile.center
total_time = myFile.total_time
distance = myFile.distance_total
pace = myFile.pace
'''

@app.route('/<file>')
def index(file):
    file = app.config['UPLOAD_FOLDER'] + file
    myFile = GarminParser(file)
    track = myFile.points
    center = myFile.center
    total_time = myFile.total_time
    distance = myFile.distance_total
    pace = myFile.pace
    return render_template('index.html',
                           track=track,
                           center=center,
                           total_time=total_time,
                           distance=distance,
                           bounds=myFile.bounds,
                           pace=pace)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join('./files/', filename))

        return redirect(url_for('index', file=f.filename))

    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


