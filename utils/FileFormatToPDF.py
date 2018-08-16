from contextlib import closing
from utils import pdfconv
import os


def FileToPDF(sourcefile, tregetfile):
	if os.path.isfile(sourcefile):
		if os.path.splitext(os.path.basename(sourcefile))[1] in [".doc", ".docx", ".txt",".html"]:
			pdfconv.convert_document2pdf(sourcefile, tregetfile)
		else:
			pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)
