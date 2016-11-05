# Generate a rhyming poem using random words from the CMU pronouncing dictionary.

import os
import sys
import json
import random
import argparse

class CloudPoet0:
	def __init__(self, filename, pattern, counts, stanzas):
		f_in = open(filename).read()
		self.dict = json.loads(f_in)
		#print(str(1) in self.dict)
		self.pattern = pattern
		self.counts = counts
		self.stanzas = stanzas

	def get_random_word(self, num_syls):
		"""
		Get a random word from the dictionary of length <= num_syls.
		Return (word, num_syls_in_word, last_syl)
		"""
		lens = list(range(1, num_syls+1))
		random.shuffle(lens)
		for l in lens:
			if str(l) in self.dict:
				last_syl, words = random.choice(list(self.dict[str(l)].items()))
				word = random.choice(words)
				return (word, l, last_syl)
		# If we didn't find a word something has gone wrong
		print("No word. Exiting.")
		sys.exit(0)

	def get_rhyming_word(self, num_syls, last_syl, used):
		"""
		Get a word from the dictionary that ends with last_syl and is not
		used. Get a random word if there is none.
		Return (word, num_syls_in_word, last_syl)
		"""
		lens = list(range(1, num_syls+1))
		random.shuffle(lens)
		for l in lens:
			if str(l) in self.dict and last_syl in self.dict[str(l)]:
				words = [word for word in self.dict[str(l)][last_syl] if word != used]
				if len(words):
					return (random.choice(words), l, last_syl)
		return self.get_random_word(num_syls)


	def generate_line(self, num_syls, last_syl=None, used=None):
		"""
		Generate a line of poetry with num_syls syllables ending with last_syl
		if specified. Return the line as a string, the last syllable, and the
		last word.
		"""
		words = []
		
		# Start with the last word in the line
		if last_syl:
			last_word, l, last_syl = self.get_rhyming_word(num_syls, last_syl, used)
		else:
			last_word, l, last_syl = self.get_random_word(min(3,num_syls))
		num_syls -= l
		words.append(last_word)

		while num_syls > 0:
			word, l, _ = self.get_random_word(num_syls)
			num_syls -= l
			words.append(word)

		words.reverse()
		line = ' '.join(words)
		return (line, last_syl, last_word)

	def generate_stanza(self, pattern, counts):
		"""
		Generate a stanza. pattern should be a string (like "ABAB") that
		describes the rhyme pattern of the poem. Counts should be a list
		of integers with the same length as pattern, where each integer
		denotes the length of the corresponding line in the pattern in
		syllables.
		Returns the stanza as a string.
		"""
		if len(pattern) != len(counts):
			print("Error: Pattern length must match counts length")
			return ""

		rhymeDict = {}
		lines = []
		for pat, count in zip(pattern, counts):
			if pat not in rhymeDict:
				line, last_syl, last_word = self.generate_line(count)
				rhymeDict[pat] = {
					"last_syl": last_syl,
					"last_word": last_word
				}
			else:
				line, _, last_word = self.generate_line(count,
																								rhymeDict[pat]["last_syl"],
																								rhymeDict[pat]["last_word"])
				rhymeDict[pat]["last_word"] = last_word
			lines.append(line)

		return '\n'.join(lines)

	def write_poem(self):
		poem = []
		for i in range(self.stanzas):
			stanza = self.generate_stanza(self.pattern, self.counts)
			poem.append(stanza)
		print('\n'.join(poem))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file_path", nargs="?",
		help="Path to the dictionary relative to this file")
	parser.add_argument("pattern", nargs="?", help="Rhyme pattern")
	parser.add_argument("counts", nargs="*", help="Length of each lines")
	parser.add_argument("stanzas", nargs="?", help="Number of stanzas")
	args = parser.parse_args()

	file_path = args.file_path if args.file_path else "dict/cmudict.json"
	path = os.path.join(os.path.dirname(__file__), file_path)

	pattern = args.pattern if args.pattern else "ABAB"
	counts = args.counts if args.counts else [2,1,2,1]
	stanzas = args.stanzas if args.stanzas else 2

	poet = CloudPoet0(path, pattern, counts, stanzas)
	poet.write_poem()




if __name__ == '__main__':
	main()














