from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

import time
from datetime import datetime
import os
import numpy as np
import cv2
import nibabel as nib

from to_PDF import generate_PDF


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/submit', methods=['POST'])
def submit():
	milli_sec = int(round(time.time() * 1000))
	dt_string = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
	folder = f'static/output/{milli_sec}'
	
	file = request.files['img']
	filename = secure_filename(file.filename)
	extension = filename.split('.')[-1]

	if extension not in ['nii', 'dcm']:
		return 'Please upload <b><i>.nii</i></b> or <b><i>.dcm</i></b> file!'

	os.mkdir(folder)
	file.save(f'{folder}/input.{extension}')

	nib_file = nib.load(f'{folder}/input.{extension}')
	data = nib_file.get_fdata()
	extract(folder, data)

	generate_PDF(folder)

	return render_template('report.html', time=dt_string, path=f'output/{milli_sec}/report.pdf')


def extract(folder, data):
	os.mkdir(f'{folder}/input')
	data = np.swapaxes(data, 2, 0)

	for i,img in enumerate(data):
		cv2.imwrite(f'{folder}/input/{i+1}.jpg', img)



if __name__ == '__main__':
	app.run(debug=True)