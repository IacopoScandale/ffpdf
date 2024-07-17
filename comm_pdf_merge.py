from data.utils import help_and_error, must_end_with_pdf
from data.strings import MERGE_PDF_COMM
from PyPDF2 import PdfReader, PdfWriter
import sys, os

help_message = f"""
This program when run in a folder by terminal merges all the pdfs in input in one single
pdf file. The output file will be called as specified later in another input.

USAGE:   {MERGE_PDF_COMM} <f1.pdf f2.pdf ... fn.pdf>
EXAMPLE: {MERGE_PDF_COMM} in1.pdf in2.pdf in3.pdf
HELP:    {MERGE_PDF_COMM} --help

oss) case covered if output filename does not end with ".pdf"
"""


help_and_error(help_message, sys.argv, command_name=MERGE_PDF_COMM, min_arg_number=1)


# funcion for adding ".pdf" when it is necessary



output_name = input("Enter output filename: ")
output_name = must_end_with_pdf(output_name)
pdf_list = sys.argv[1:]


def name_decision(tmp_name: str) -> str:
  """
    This function takes in input an "non valid" name and
    asks you what to do with it.
    
    This function does not stop until you decide what to do:
    1) you overwrite the file
    2) you choose an other name
  """
  res = input(f"\nWarning: '{output_name[2:]}' already exists. Do you want to overwrite it?\n [Y,n]: ")
  if res in "yYsS":
    return tmp_name
  
  else:
    new_name = input("\nInsert a new name: ")
    new_name = must_end_with_pdf(new_name)

    if os.path.isfile(new_name):
      return name_decision(new_name)
    else:
      return new_name


# check if output_name alredy exists
if os.path.isfile(output_name):
  output_name = name_decision(output_name)


# merge pdfs
writer = PdfWriter()

for pdf in pdf_list:
  # check if there are only pdfs in the folder
  if not pdf.endswith(".pdf"):
    print("ERROR: all input files must end with .pdf")
    sys.exit()

  reader = PdfReader(pdf)

  for page in reader.pages:
    writer.add_page(page)

with open(output_name, "wb") as f:
  writer.write(f)