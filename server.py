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
	# Get time, create folder.
	milli_sec = int(round(time.time() * 1000))
	in_time = datetime.now().strftime('%B %d, %Y - %H:%M:%S')
	folder = f'static/output/{milli_sec}'
	
	# Extract uploaded file infomation
	file = request.files['img']
	filename = secure_filename(file.filename)
	extension = filename.split('.')[-1]

	# Extract file and save to local dir
	if extension not in ['nii', 'dcm']:
		return 'Please upload <b><i>.nii</i></b> or <b><i>.dcm</i></b> file!'

	os.mkdir(folder)
	file.save(f'{folder}/input.{extension}')

	nib_file = nib.load(f'{folder}/input.{extension}')
	data = nib_file.get_fdata()
	extract(folder, data)
	extract1(folder, data)

	# Out time
	out_time = datetime.now().strftime('%B %d, %Y - %H:%M:%S')

	generate_PDF(folder, in_time, out_time, num_files=data.shape[2])

	return render_template('report.html', folder=f'output/{milli_sec}', in_time=in_time, out_time=out_time, num_files=data.shape[2])
	# return ''


def extract(folder, data):
	os.mkdir(f'{folder}/input')
	data = np.swapaxes(data, 2, 0)

	for i,img in enumerate(data):
		cv2.imwrite(f'{folder}/input/{i+1}.jpg', img)

def extract1(folder, data):
	os.mkdir(f'{folder}/output')
	data = np.swapaxes(data, 2, 0)

	for i,img in enumerate(data):
		cv2.imwrite(f'{folder}/output/{i+1}.jpg', img)



if __name__ == '__main__':
	app.run(debug=True)