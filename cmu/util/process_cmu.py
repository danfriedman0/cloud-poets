# Process the CMU pronunciation dictionary and save it in a form more
# suited for poem generation.
#
# Dan Friedman, 11/4/2016

import os
import argparse
import json


# Process the dictionary


def num_syls(syls):
	"""Returns the number of syllables in a CMU syllable string."""
	return len([c for c in syls if c in ['0','1','2']])


def last_syl_perfect(syls):
	"""Returns a perfect rhyme syllable for a CMU syllable string"""
	syl_list = syls.split(' ')
	last_stress = len(syl_list) - 1
	for i in range(len(syl_list)-1,-1,-1):
		if '1' in syl_list[i]:
			last_stress = i
			break
	return ''.join(syl_list[i:])


def main():
	# Get the file paths.
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file", nargs="?",
						help="Path to input file relative to this file")
	parser.add_argument("output_file", nargs="?",
						help="Path to output file relative to this file")
	args = parser.parse_args()

	file_in = args.input_file if args.input_file else "../dict/cmudict-0.7b"
	file_out = args.output_file if args.output_file else "../dict/cmudict.json"
	p_in = os.path.join(os.path.dirname(__file__), file_in)
	p_out = os.path.join(os.path.dirname(__file__), file_out)



	# Create a dictionary to structure the CMU dict by syllable length
	# and rhyme syllable
	d = {}
	f_in = open(p_in, 'r')
	for line in f_in:
		if not line[0].isalpha():
			continue
		word, syls = line.split('  ')
		num = num_syls(syls)
		last = last_syl_perfect(syls)
		if num not in d:
			d[num] = {}
		if last not in d[num]:
			d[num][last] = []
		d[num][last].append(word.lower())
	f_in.close()

	# Save the dictionary to the output file in JSON
	f_out = open(p_out, 'w')
	json.dump(d, f_out, separators=(',', ':'))
	f_out.close()


if __name__ == '__main__':
	main()








