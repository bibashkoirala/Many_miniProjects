import PyPDF2
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
input_paths = [os.path.join(script_directory, 'file1.pdf'), os.path.join(script_directory, 'file2.pdf')]

input_paths = ['file1.pdf', 'file2.pdf' ]
merger = PyPDF2.PdfMerger()
    
for path in input_paths:
        pdfFile = open(path, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFile)
        merger.append(path)
    
merger.write('merged.pdf')
pdfFile.close()

