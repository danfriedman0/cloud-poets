# Use the gutenberg API to download a bunch of books and concatenate them
# into a text file in the text directory

import os
import argparse
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

# get a filename and a book list from the command line
parser = argparse.ArgumentParser()
parser.add_argument("output_name", nargs="?", help="The name of the output file")
parser.add_argument("book_ids", type=int, nargs="*",
	help="A list of gutenberg book IDs")
args = parser.parse_args()


# these are my defaults: the filename is 'verse.txt' and the book_ids are a list
# I made of books of children's poetry books
output_name = 'verse.txt'
book_ids = [10912, 24485, 24449, 24108, 22014, 17782, 13646, 13648, 13650, 20113, 13647, 23545, 21189, 19389, 19722, 9380, 24560, 27424, 10607, 39784, 23794, 27175, 17283, 19541, 10131, 11095, 22888, 18909, 17282, 23433, 5868, 27176, 22529, 23749, 38562, 16686, 40134, 19469, 2670, 50994]
if args.output_name: output_name = args.output_name
if args.book_ids: book_ids = args.book_ids

# download the books one by one and write them to the output file
output_path = os.path.join(os.getcwd(), 'text/' + output_name)
f = open(output_path, 'w')
for i, book_id in enumerate(book_ids):
	text = strip_headers(load_etext(book_id)).strip()
	f.write(text)
f.close()
