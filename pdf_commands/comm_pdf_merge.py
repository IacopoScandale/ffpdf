from .data.utils import add_one_to_counter, choose_out_pdf_name
from .data.strings import MERGE_PDF_COMM
from PyPDF2 import PdfReader, PdfWriter
from argparse import ArgumentParser, Namespace
import sys


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "This program when run in a folder by terminal merges all the "
      "pdfs in input in one single pdf file. The output file will be "
      "called as specified later in another input."
    ),
    usage=f"{MERGE_PDF_COMM} [h] f1.pdf f2.pdf ... fn.pdf"
  )
  parser.add_argument('pdfs', nargs='+', help='One or more pdf file')
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()
  output_pdf_name: str = choose_out_pdf_name()

  # merge pdfs:
  writer = PdfWriter()

  for pdf in args.pdfs:
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