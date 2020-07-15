from flask import Flask, flash, request, redirect, url_for, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
import os
from schedule_maker import make_schedule

ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
			file = file.save(os.path.join(THIS_FOLDER, filename))
			make_schedule(filename)
			return send_file('/home/mkagan/' + filename + '.xlsx', as_attachment=True)

	return '''
	<!doctype html>
	<title>Schedule Maker!!!</title>
	<h1>Schedule Maker!!!</h1>
	<body style="fontsize : large">Please upload only saved JSON files from ms1 API /location/{location_id}/equipment/
	that have equipmentmetadata_set turned to true.....\n
	otherwise this program won't really help you</body>
	<form method=post enctype=multipart/form-data>
	  <input type=file name=file>
	  <input type=submit value=Upload>
	</form>
	'''

if __name__ == '__main__':
	app.run()
