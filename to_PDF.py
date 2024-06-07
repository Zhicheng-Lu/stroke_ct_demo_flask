from latexdocs import Document, TikZFigure, Image
from pylatex import Alignat, Matrix, Math, Tabular, Plot
from pylatex.utils import italic
import numpy as np

def generate_PDF(folder):
	doc = Document()

	img = Image(filename='../../images/logo.png', position='h!', width='100px')
	doc.append(img)

	doc.build().generate_pdf(f'{folder}/report', compiler='pdflatex')