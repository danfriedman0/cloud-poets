# Process raw text files from gutenberg.
# Specifically clean up children's verse: get rid of excess whitespace
# and try to eliminate all of the non-rhyming paratext

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", nargs="?", help="path to the input file")
parser.add_argument("output_file", nargs="?", help="path to the output file")
args = parser.parse_args()

def process_raw_verse(input_path, output_path):
	input_file = open(input_path, 'r')
	output_file = open(output_path, 'w')
	open_tag = False
	newline = False
	for line in input_file:
		if line.startswith("[Illustration"): open_tag = True
		if line.endswith("]\n"): open_tag = False
		elif line == "\n":
			if not newline:
				output_file.write(line)
				newline = True
		elif not open_tag and not line[len(line)-2].isdigit():
			newline = False
			output_file.write(line)
	input_file.close()
	output_file.close()



input_file = args.input_file if args.input_file else "text/raw_verse.txt"
output_file = args.output_file if args.output_file else "text/verse.txt"

input_path = os.path.join(os.getcwd(), input_file)
output_path = os.path.join(os.getcwd(), output_file)
process_raw_verse(input_path, output_path)

