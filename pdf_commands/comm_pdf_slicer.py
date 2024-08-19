from .data.utils import add_one_to_counter, choose_out_pdf_name, must_end_with_pdf
from .data.strings import SLICE_PDF_COMM
from PyPDF2 import PdfReader, PdfWriter
from argparse import ArgumentParser, Namespace
import sys


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "This program takes in input a pdf file name (in the current "
      "folder). It asks you to insert the slice you want e.g. '1-5,7'. "
      "It also asks you the output_pdf_name that may or may not end "
      "with '.pdf'. Then it will create a pdf output file with only "
      "the pages 1 to 5 and the page 7"
    )
  )
  parser.add_argument("input_pdf")
  parser.add_argument(
    "slice", 
    nargs="?",
    default=None,
    help="Optional: e.g.: '1-5,7' will select pages 1 to 5 and page 7",
  )
  parser.add_argument(
    "out_pdf_name", 
    nargs="?",
    default=None,
    help="Optional: e.g.: 'my_pdf' or 'file.pdf'",
  )
  args: Namespace = parser.parse_args()
  return args


def num_pages(pdf_filename: str) -> int:
  """
  Returns the number of pages of the input pdf
  """
  with open(pdf_filename, 'rb') as pdf:
    pdf_reader = PdfReader(pdf)
    return len(pdf_reader.pages)


def slice_to_list(intervals: str) -> list[int]:
  """
  This function converts a str "slice" into the list with all 
  "page numbers"
  """
  def buck_interval_error(buck):
    raise ValueError(f"'{buck}' in '{intervals}' is not correct. "
                      "Expexted 'a-b' with a,b positive numbers, a<=b")

  def buck_error(buck):
    raise ValueError(f"'{buck}' in '{intervals}' is not correct. "
                      "Expexted a natural number")
  
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
      two_nums: list[str] = buck.split("-")

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
    res: str = input(
      "\n· Insert a slice for the pdf:"
      "\n  (press Ctrl+c ('^C') to exit): "
    )
  except KeyboardInterrupt:
    print()
    sys.exit()

  try:
    return slice_to_list(res)
  except ValueError as e:
    print(f"\n  Error:\n  {e}\n  try again...")
    return selected_pages_decision()
  

def extract_pages(
  input_path: str, 
  output_path: str, 
  page_numbers: list[int]
) -> None:
  with open(input_path, 'rb') as input_file:
    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    for page_number in page_numbers:
      if 1 <= page_number <= len(pdf_reader.pages):
        pdf_writer.add_page(pdf_reader.pages[page_number - 1])

    with open(output_path, 'wb') as output_file:
      pdf_writer.write(output_file)


def main() -> None:
  args: Namespace = get_arguments()
  page_number = num_pages(args.input_pdf)

  # slice
  if args.slice is None:
    print(f"\n  ('{args.input_pdf}' with {page_number} pages)")
    selected_pages: list[int] = selected_pages_decision()
  else:
    try:
      selected_pages: list[int] =  slice_to_list(args.slice)
    except ValueError as e:
      print(f"\n  Error:\n  {e}\n  try again...")
      print(f"\n  ('{args.input_pdf}' with {page_number} pages)")
      selected_pages: list[int] = selected_pages_decision()
    
  # out pdf name
  if args.out_pdf_name is None:
    output_pdf: str = choose_out_pdf_name()
  else:
    output_pdf: str = must_end_with_pdf(args.out_pdf_name)

  extract_pages(args.input_pdf, output_pdf, selected_pages)

  # +1 to usage counter
  add_one_to_counter(SLICE_PDF_COMM)