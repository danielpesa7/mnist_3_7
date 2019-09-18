from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from predictions import predict
from fastai.vision import open_image, load_learner
from PIL import Image
import io, os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
			# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
	file = request.files['file']
	# if user does not select file, browser also
	# submit an empty part without filename
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		model_path = 'model/'
		learn = load_learner(model_path)
		img = open_image(UPLOAD_FOLDER + filename)
		prediction = learn.predict(img)
		return render_template('result.html', number = prediction[0], score = prediction[2])
	return 'Null'

if __name__ == '__main__':
    app.run(debug=True)