from pylatex import Document, Figure, SubFigure, Section, PageStyle, Head, Foot, MiniPage, \
	LargeText, MediumText, LineBreak, StandAloneGraphic, simple_page_number, TextColor, Command, NewLine, Tabu, Center, \
	TextBlock, VerticalSpace, NewPage
from pylatex.utils import italic, bold, NoEscape
import numpy as np


def generate_PDF(folder, in_time, out_time, num_files):
	doc = Document(geometry_options={'left': '0.625in', 'right': '0.625in', 'top': '0.75in', 'bottom': '0.75in', 'includeheadfoot': True})

	# Generating first page style
	first_page = PageStyle('firstpage')

	# Header image
	with first_page.create(Head('L')) as header_left:
		with header_left.create(MiniPage(width=NoEscape(r'0.49\textwidth'), pos='c')) as logo_wrapper:
			logo_wrapper.append(StandAloneGraphic(image_options='width=100px', filename='../../images/logo.png'))
			# logo_wrapper.append(LineBreak())
			# logo_wrapper.append(LineBreak())
			# logo_wrapper.append(StandAloneGraphic(image_options=r'width=525px', filename='images/banner.jpg'))

	# Header image
	with first_page.create(Head('R')) as header_right:
		with header_right.create(MiniPage(width=NoEscape(r'0.49\textwidth'), pos='c', align='r')) as title_wrapper:
			title_wrapper.append(simple_page_number())

	# Footer
	with first_page.create(Foot('C')) as footer:
		with footer.create(MiniPage(width=NoEscape(r'\textwidth'), pos='c', align='c')) as footer_wrapper:
			footer_wrapper.append(TextColor('gray', italic('Note that this stroke diagnosis report is for demo only, the results cannot be used in any clinics.')))

	doc.preamble.append(first_page)

	# Title
	with doc.create(Center()):
		doc.append(VerticalSpace("2mm"))
		doc.append(Command('fontsize', arguments=['20', '0']))
		doc.append(Command('selectfont'))
		doc.append(bold('Stroke Diagnosis Report'))
		doc.append(VerticalSpace("5mm"))

	# Patient info
	with doc.create(Tabu('X[l] X[2l] X[l] X[2l]', row_height=2)) as info:
		info.add_hline()
		info.add_empty_row()
		info.add_row(['Patient Name:', 'Sample Patient', 'Modality:', 'Computed Tomography (CT)'])
		info.add_row(['Date of Birth:', 'DD-MM-YYYY', 'Registered on:', in_time])
		info.add_row(['Gender:', 'Unknown', 'Reported on:', out_time])
		info.add_empty_row()
		info.add_hline()

	# Diagnosis tile and content
	with doc.create(Tabu('X[l]', row_height=2)) as diagnosis_title:
		diagnosis_title.add_empty_row()
		doc.append(Command('fontsize', arguments=['12', '0']))
		doc.append(Command('selectfont'))
		diagnosis_title.add_row([NoEscape(r'\underline{Diagnosis Report:}')], mapper=bold)

	with doc.create(Tabu('X[l]', row_height=2)) as diagnosis:
		diagnosis.add_row(['Each diagnosis is dependent on the symptoms and complexity of the condition that might be causing them, so there is no set timeline as to when you will know your results. It\'s important to stay in contact with your healthcare provider during your diagnostic process especially if you have any changes to your symptoms or medical history, which could affect the results of your diagnosis.'])
		diagnosis.add_empty_row()
		diagnosis.add_hline()

	# Lesion segmentation title
	with doc.create(Tabu('X[l]', row_height=2)) as title:
		title.add_empty_row()
		doc.append(Command('fontsize', arguments=['12', '0']))
		doc.append(Command('selectfont'))
		title.add_row([NoEscape(r'\underline{Lesion Segmentation:}')], mapper=bold)

	doc.change_document_style('firstpage')

	for i in range(1, num_files+1):
		if i % 2 == 1:
			# Begin second page, segmentation results
			doc.append(NewPage())

			# Title
			with doc.create(Center()):
				doc.append(Command('fontsize', arguments=['20', '0']))
				doc.append(Command('selectfont'))
				doc.append(bold('Stroke Diagnosis Report'))
				doc.append(VerticalSpace("5mm"))
		
		# Figure: input CT & segmentation
		with doc.create(Figure(position='h!')) as fig:
			doc.append(Command('centering'))
			with doc.create(SubFigure(position='b', width=NoEscape(r'0.48\linewidth'))) as original:
				original.add_image(f'input/{i}.jpg', width=NoEscape(r'0.95\linewidth'))
			with doc.create(SubFigure(position='b', width=NoEscape(r'0.48\linewidth'))) as segmentation:
				segmentation.add_image(f'output/{i}.jpg', width=NoEscape(r'0.95\linewidth'))
			fig.add_caption('Original CT scan (left) and stroke lesion segmentation (right).')


	doc.generate_pdf(f'{folder}/report', compiler='latexmk', clean=True, clean_tex=False, compiler_args=['-pdf'])