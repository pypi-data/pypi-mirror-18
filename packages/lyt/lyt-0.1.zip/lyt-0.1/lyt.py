## #! /usr/bin/python

# Copyright (C) 2016  Adrien Lamarque

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""lyt is a literate programming tool, written in Python, that extracts fenced code blocks from Markdown documents. It is meant to be used as a preprocess tool before a conventional build.
"""
import re
import collections
import click
import sys
import os.path

DEFAULT_EXT = "txt"
matching_extensions = {
	'python': 'py',
	'c++': 'cpp',
	'c': 'c',
	'c#': 'cs',
	'haskell': 'hs',
	'ruby': 'rb',
	'go': 'go',
	'rust': 'rs',
	'racket': 'rkt',
}

DEFAULT_COMMENT_SYMBOL = "#"
comment_symbols = collections.defaultdict(lambda: DEFAULT_COMMENT_SYMBOL, {
	'python': '#',
	'c++': '//',
	'c': '//',
	'c#': '//',
	'haskell': '--',
	'ruby': '#',
	'go': '//',
	'rust': '//',
	'racket': ';',
})

e = click.echo

code_open_re = re.compile(r'^`{3,}(?!.*`)|^~{3,}(?!.*~)', re.MULTILINE) # /^`{3,}(?!.*`)|^~{3,}(?!.*~)/
code_close_re = re.compile(r'^(?:`{3,}|~{3,})(?= *$)', re.MULTILINE) # /^(?:`{3,}|~{3,})(?= *$)/

@click.command()
@click.argument("input_file", type=click.File('r'))
@click.option("--force", is_flag=True)

def lyt(input_file, force):
	"""lyt extracts fenced code blocks from Markdown documents."""
	out = collections.defaultdict(str)
	lines = input_file.read()
	start_pos = 0

	while True:
		open_match = code_open_re.search(lines, start_pos)
		if not open_match:
			break
		start_pos = open_match.end()
		fence_char = lines[open_match.start()]
		infostring_end_idx = lines.find("\n", open_match.end())
		infostring = lines[open_match.end():infostring_end_idx]
		
		if infostring:
			lang = infostring.split()[0]
		else:
			lang = "unknown"
		start_pos = infostring_end_idx

		found = False
		while not found:
			close_match = code_close_re.search(lines, start_pos)
			if not close_match:
				found = True
				out[lang] += lines[start_pos:]
				# Turns out it's valid to have a 'dangling' fenced block quote according to the CommonMark spec
				# e("Mismatched fenced block quotes! Check that your Markdown is valid.")
				# sys.exit(1)

			if lines[close_match.start()] == fence_char:
				found = True
				out[lang] += lines[start_pos+1:close_match.start()]
		start_pos = close_match.end()

	lpy_ext_idx = input_file.name.rfind(".") + 1
	basename = input_file.name[:lpy_ext_idx]

	for (language, source) in out.items():
		language = language.lower()
		if language in matching_extensions:
			ext = matching_extensions[language]
		else:
			if language == "unknown":
				e("WARNING! The following blocks didn't have an infostring specifying the language. They were aggregated together and will be written to a .%s file." % DEFAULT_EXT)
				e(source)
				ext = DEFAULT_EXT
			else:
				e("Couldn't find extension to use for language %s. Using the first three letters: %s" % (language, language[:3]))
				ext = language[:3]

		output_filename = basename + ext

		if os.path.isfile(output_filename) and not force:
			e("WARNING! The file %s already exists. To allow overwriting, re-launch lyt with the --force option." % output_filename)
		else:
			with open(output_filename, "w") as output_file:
				output_file.write(comment_symbols[language] + "")
				output_file.write(source)
				e("Wrote %s." % output_filename)

if __name__ == "__main__":
	lyt()
