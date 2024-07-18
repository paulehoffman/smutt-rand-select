#!/usr/bin/env python3

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

# Outputs a bracketed string
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

    if "A" == ss.upper():
      rv.append(Hexable(get_input("Enter " + name)))
    elif "D" == ss.upper():
      puts(str(rv.pop(get_input("Enter index of " + name + " to delete", int)-1)) + " deleted")
    elif "L" == ss.upper():
      if len(rv) == 0:
        continue
      else:
        for ii in range(len(rv)):
          puts(str(ii+1) + ": " + str(rv[ii]))
    elif "Q" == ss.upper():
      if len(rv) > 0:
        return rv
      else:
        print(name + " list is empty")
    else:
      puts("Invalid command")

# BEGIN EXECUTION
if locale.getlocale()[1].upper() != 'UTF-8':
  print("Locale not UTF-8")
  exit(1)

if not sys.flags.utf8_mode:
  print("Not in UTF-8 mode. Aborting.")
  exit(1)

# Check if we're being piped data
if select.select([sys.stdin, ], [], [], 0.0)[0]:
  if not sys.__stdin__.encoding == 'utf-8':
    print("STDIN not UTF-8")
    exit(1)
  else:
    candidates = []
    p_values = []
    first_loaded = False

    for line in sys.__stdin__:
      if len(line.strip()) == 0:
        first_loaded = True
        continue
      if first_loaded:
        p_values.append(Hexable(line.strip()))
      else:
        candidates.append(Hexable(line.strip()))

else:
   puts("Candidates")
   candidates = fill_list("candidate")

   puts("_P_ values")
   p_values = fill_list("_P_ value")

puts("Candidates")
for cc in candidates:
   puts(str(cc))

puts("_P_ Values")
for pv in p_values:
   puts(str(pv))

_D_ = "/" + "/".join([pp.to_hex() for pp in p_values])
puts("_D_:" + _D_)

output = []
for cc in candidates:
  output.append((hashlib.sha256(cc.to_hex(_D_).encode("utf8")).hexdigest(), str(cc)))

for ii in sorted(output, key=lambda hash: hash[0]):
  puts("hash:" + ii[0] + " candidate:" + ii[1])
