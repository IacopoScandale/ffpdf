from data.utils import help_and_error, add_one_to_counter, choose_out_pdf_name
from data.strings import SLICE_PDF_COMM
from PyPDF2 import PdfReader, PdfWriter
import os, sys

help_message = f"""
This program takes in input a pdf file name (in the current folder).
1. It then asks you to type the slice you want e.g. '1-5,7'
2. It also asks you the output_pdf_name that can or cannot end with '.pdf'.
3. It will create a pdf output file with only the pages 1 to 5 and the page 7

USAGE: {SLICE_PDF_COMM} <input.pdf>
"""

help_and_error(help_message, sys.argv, 1, command_name=SLICE_PDF_COMM)


def num_pages(pdf_filename) -> int:
  """
  Returns the number of pages of the input pdf
  """
  with open(pdf_filename, 'rb') as pdf:
    pdf_reader = PdfReader(pdf)
    return len(pdf_reader.pages)


pdf_name = sys.argv[1]
page_number = num_pages(pdf_name)

print(f"\n  ('{pdf_name}' with {page_number} pages)")


def slice_to_list(intervals: str) -> list[int]:
  """
    This function converts a str "slice" into the list with all "page numbers"
  """
  def buck_interval_error(buck):
    raise ValueError(f"'{buck}' in '{intervals}' is not correct. Expexted 'a-b' with a,b positive numbers, a<=b")

  def buck_error(buck):
    raise ValueError(f"'{buck}' in '{intervals}' is not correct. Expexted a natural number")
  
  if "," not in intervals:
    if "-" in intervals:
      two_nums = intervals.split("-")

      if len(two_nums) == 2:
        a = two_nums[0]
        b = two_nums[1]
        if a.isnumeric() and b.isnumeric() and int(a) <= int(b):
          return list(range(int(a),int(b)+1))
        else:
          buck_interval_error(intervals)
      else:
        buck_interval_error(intervals)    

    elif intervals.isnumeric():
      return [int(intervals)]
    else:
      raise ValueError(f"'{intervals}' is not a correct slice")
    
  res = []
  bucks = intervals.split(",")

  
  for buck in bucks:
    if "-" in buck:
      two_nums = buck.split("-")

      if len(two_nums) == 2:
        a = two_nums[0]
        b = two_nums[1]
        if a.isnumeric() and b.isnumeric() and int(a) <= int(b):
          res.extend(list(range(int(a),int(b)+1)))
        else:
          buck_interval_error(buck)
      else:
        buck_interval_error(buck)

    elif buck.isnumeric():
      res.append(int(buck))

    else:
      buck_error(buck)

  return res


def selected_pages_decision() -> list[int]:
  """
  This function does not stop until you decide what to do:
   1) you insert a VALID "slice"
   2) you exit by typing signal interrtupt (^C) pressing Ctrl+c
  """
  
  try:
    res = input("\n· Insert a slice for the pdf:\n  (press Ctrl+c ('^C') to exit): ")
  except KeyboardInterrupt:
    print()
    sys.exit()

  try:
    return slice_to_list(res)
  except:
    return selected_pages_decision()
  

def extract_pages(input_path:str, output_path:str, page_numbers) -> None:
  with open(input_path, 'rb') as input_file:
    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    for page_number in page_numbers:
      if 1 <= page_number <= len(pdf_reader.pages):
        pdf_writer.add_page(pdf_reader.pages[page_number - 1])

    with open(output_path, 'wb') as output_file:
      pdf_writer.write(output_file)


selected_pages: list[int] = selected_pages_decision()
output_pdf: str = choose_out_pdf_name()



extract_pages(pdf_name, output_pdf, selected_pages)


# +1 to usage counter
add_one_to_counter(SLICE_PDF_COMM)