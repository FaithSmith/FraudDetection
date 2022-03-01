from flask import Flask, render_template, abort,\
     Response, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pickle
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['UPLOAD_FOLDER'] = os.path.join('static','files')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
#upload model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload Image")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        # First grab the file
        file = form.file.data 
        filename = secure_filename(file.filename)
        abs_path_to_dir = os.path.abspath(os.path.dirname(__file__))
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(Response('Wrong File Format! Please Upload an image'))
            file.save(os.path.join(
                abs_path_to_dir,
                app.config['UPLOAD_FOLDER'],
                filename)) # Then save the file
            return redirect(url_for('predict',file=file))
    return render_template('index.html', form=form)

@app.route('/predict_disease')
def predict(file):
    file = 


if __name__ == '__main__':
    app.run(debug=False)