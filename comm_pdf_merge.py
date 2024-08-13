from data.utils import help_and_error, add_one_to_counter, choose_out_pdf_name
from data.strings import MERGE_PDF_COMM
from PyPDF2 import PdfReader, PdfWriter
import sys

help_message = f"""
This program when run in a folder by terminal merges all the pdfs in 
input in one single pdf file. The output file will be called as 
specified later in another input.

USAGE:   {MERGE_PDF_COMM} <f1.pdf f2.pdf ... fn.pdf>
EXAMPLE: {MERGE_PDF_COMM} in1.pdf in2.pdf in3.pdf
HELP:    {MERGE_PDF_COMM} --help

oss) case covered if output filename does not end with ".pdf"
"""

help_and_error(
  help_message, 
  sys.argv, 
  command_name=MERGE_PDF_COMM, 
  min_arg_number=1
)

pdf_list = sys.argv[1:]
output_pdf_name: str = choose_out_pdf_name()

# merge pdfs:
writer = PdfWriter()

for pdf in pdf_list:
  # check if there are only pdfs in the folder
  if not pdf.endswith(".pdf"):
    print("ERROR: all input files must end with .pdf")
    sys.exit()

  # read every pdf page and add it to the writer
  reader = PdfReader(pdf)

  for page in reader.pages:
    writer.add_page(page)

# save merged pdf
with open(output_pdf_name, "wb") as f:
  writer.write(f)


# +1 to usage counter
add_one_to_counter(MERGE_PDF_COMM)