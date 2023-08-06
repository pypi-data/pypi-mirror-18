#!/usr/bin/env python

# noweb.py
# By Jonathan Aquino (jonathan.aquino@gmail.com)
# And is now forked by DragonTortoise (DragonTortoise888@gmail.com)
#
# This program extracts code from a literate programming document in
# "noweb" format.  It was generated from noweb.ny.markdown, itself a
# literate programming document.
#
# For more information, including the original source code and
# documentation, see https://goo.gl/fPgdxH (full url: http://jonaquino.
# blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html)
# and https://goo.gl/WHjKAd (full url: https://github.com/dragontortoise
# /noweb.py).

import sys, re

filename = sys.argv[-1]
outputChunkName = sys.argv[-2][2:]

# Here we read input files into list of chunks.
file = open(filename)
chunkName = None
chunks = {}
OPEN = "<<"
CLOSE = ">>"
for line in file:
  match = re.match(OPEN + "([^>]+)" + CLOSE + "=", line)
  if match:
    chunkName = match.group(1)
    # If chunkName exists in chunks, then we'll just add to the existing
    # chunk.
    if not chunkName in chunks:
      chunks[chunkName] = []
  else:
    match = re.match("@", line)
    if match:
      chunkName = None
    elif chunkName:
      chunks[chunkName].append(line)

# Here we define JonathanAquino's simplest recursive function.
def expand(chunkName, indent):
  chunkLines = chunks[chunkName]
  expandedChunkLines = []
  for line in chunkLines:
    # Check if the line is another chunk or not.
    match = re.match("(\s*)" + OPEN + "([^>]+)" + CLOSE + "\s*$", \
      line)
    if match:
      # Expand the chunk and add the result which are multiple lines of
      # codes to expandedChunkLines.
      expandedChunkLines.extend(expand(match.group(2), indent + \
        match.group(1)))
    else:
      # Add a single line of code.
      expandedChunkLines.append(indent + line)
  return expandedChunkLines

# Outputting the user selected chunk by calling the recursive function
# expand() above.
for line in expand(outputChunkName, ""):
  print(line, end="")
