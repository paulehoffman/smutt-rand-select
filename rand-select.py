#!/usr/bin/env python3

'''
Companion program to "A Verifiable and Reproducible Random Candidate Selection Process"
See FUTUREURLGOESHERE for more information
'''

##### Will need and ICANN-approved license

import hashlib
import locale
import select
import sys

# Hexable strings
class Hexable():
  def __init__(self, in_str):
    self.ss = in_str

  def to_utf8(self, suffix=""):
    return (self.ss + suffix).encode("utf8")
    
  def to_hex(self, suffix=""):
    return "".join([hex(cc)[2:] for cc in self.to_utf8(suffix)])

  def __str__(self):
    return self.ss

# Prints a bracketed string
def puts(out_str):
  print("[" + out_str + "]")

# Takes a string prompt
# Returns input of correct type
def get_input(prompt_str):
  puts(prompt_str)
  return input("-->").strip()

# Takes a string name
# Returns a list of Hexables
def fill_list(name):
  rv = []
  while True:
    prompt = "'A' to add a new " + name + \
      " || 'D' to delete a " + name + \
      " || 'L' to list " + name + "s" + \
      " || 'Q' to quit when finished"
    ss = get_input(prompt)

    if ss.upper() == "A":
      rv.append(Hexable(get_input("Enter " + name)))
    elif ss.upper() == "D":
      puts(str(rv.pop(get_input("Enter index of " + name + " to delete", int)-1)) + " deleted")
    elif ss.upper() == "L":
      if len(rv) == 0:
        continue
      else:
        for ii in range(len(rv)):
          puts(str(ii+1) + ": " + str(rv[ii]))
    elif ss.upper() == "Q":
      if len(rv) > 0:
        return rv
      else:
        print(name + " list is empty")
    else:
      puts("Invalid command")

# Handles STDIN
def handle_stdin():
  candidates = []
  p_values = []
  top_done = False

  for line in sys.__stdin__:
    if len(line.strip()) == 0:
      top_done = True
      continue
    if top_done:
      p_values.append(Hexable(line.strip()))
    else:
      candidates.append(Hexable(line.strip()))
  return candidates, p_values


# Main program start here

if locale.getlocale()[1].upper() != 'UTF-8':
  sys.exit("Locale not UTF-8")

if not sys.flags.utf8_mode:
  sys.exit("Not in UTF-8 mode. Aborting.")

# Check if we're being piped data
if select.select([sys.stdin, ], [], [], 0.0)[0]:
  if not sys.__stdin__.encoding == 'utf-8':
    sys.exit("STDIN not UTF-8")
  else:
    candidates, p_values = handle_stdin()
else:
   puts("Candidates")
   candidates = fill_list("candidate")

   puts("_P_ values")
   p_values = fill_list("_P_ value")

if not len(candidates):
  sys.exit("No candidates. Aborting.")

puts("Candidates")
for cc in candidates:
   puts("candidate:" + str(cc) + " hex:" + cc.to_hex())

if not len(p_values):
  sys.exit(0)

puts("_P_ Values")
for pv in p_values:
   puts(str(pv))

_D_ = "/".join([str(pv) for pv in p_values])
puts("_D_ = " + _D_)

output = []
for cc in candidates:
  output.append((hashlib.sha256(cc.to_hex("/" + _D_).encode("utf8")).hexdigest(), str(cc)))

for ii in sorted(output, key=lambda hash: hash[0]):
  puts("hash:" + ii[0] + " candidate:" + ii[1])
