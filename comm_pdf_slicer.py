from data.utils import help_and_error, add_one_to_counter
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


def slice_to_list(intervals: str) -> list:
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


def selected_pages_decision() -> list:
  """
  This function does not stop until you decide what to do:
   1) you insert a VALID "slice"
   2) you exit by typing "--exit"
  """
  res = input("\n· Insert a slice for the pdf:\n  (type '--exit' to quit): ")
  
  if res == "--exit":
    sys.exit()
  else:
    try:
      return slice_to_list(res)
    except:
      return selected_pages_decision()


# funcion for adding ".pdf" when it is necessary
def must_end_with_pdf(fname: str) -> str:
  """
    This function makes sure that input str 'fname'
    ends or will be ending with ".pdf"
  """
  if not fname.endswith(".pdf"):
    return fname + ".pdf"
  return fname


def out_pdf_name_decision() -> str:
  """
    This function and next_decision let you decide what to do
    1) you exit by typing "--exit"
    2) you overwrite the file
    3) you choose an other name 

    Output: "out_name.pdf"
  """
  res = input("\n· Insert a name for the output pdf (it may or may not end with '.pdf'):\n  (type '--exit' to quit): ")

  if res == "--exit":
    sys.exit()
  else:
    cur_out_name = must_end_with_pdf(res)
  
    if os.path.isfile(cur_out_name):
      return next_decision(must_end_with_pdf(res))
    else:
      return cur_out_name
    

def next_decision(tmp_name: str) -> str:
  """
    This function takes in input an "non valid" name ending
    with .pdf and asks you what to do with it.
    
    This function does not stop until you decide what to do:
    1) you exit by typing "--exit"
    2) you overwrite the file
    3) you choose an other name

    oss: tmp_name ends with '.pdf'
  """
  decision = input(f"\n  Warning: '{tmp_name}' already exists. Do you want to overwrite it?\n  (type '--exit' to quit)\n  [y,n]: ")
  
  if decision == "--exit":
    sys.exit()

  elif decision == "y" or decision == "Y":
    return tmp_name
  
  elif decision == "n" or decision == "N":
    new_name = input("\n  Insert a new name: ")
    new_name = must_end_with_pdf(new_name)

    if os.path.isfile(new_name):
      return next_decision(new_name)
    else:
      return new_name
    
  else:
    return next_decision(tmp_name)


def extract_pages(input_path, output_path, page_numbers):
  with open(input_path, 'rb') as input_file:
    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    for page_number in page_numbers:
      if 1 <= page_number <= len(pdf_reader.pages):
        pdf_writer.add_page(pdf_reader.pages[page_number - 1])

    with open(output_path, 'wb') as output_file:
      pdf_writer.write(output_file)


selected_pages = selected_pages_decision()
output_pdf = out_pdf_name_decision()

extract_pages(pdf_name, output_pdf, selected_pages)


# +1 to usage counter
add_one_to_counter(SLICE_PDF_COMM)