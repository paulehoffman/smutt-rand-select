#!/usr/bin/env python3

import hashlib
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

  def __repr__(self):
    return "str:" + self.ss + " hex:" + self.to_hex()

# A candidate
class Candidate(Hexable):
  def __init__(self, in_str):
    Hexable.__init__(self, in_str)

# A _P_ value
class P_value(Hexable):
  def __init__(self, in_str):
    Hexable.__init__(self, in_str)


# Outputs a bracketed string
def puts(out_str):
  print("[" + out_str + "]")

# Takes a prompt string and a type
# Supported types are str and int > 0
# Returns input of correct type
def get_input(prompt_str, type=str):
  while True:
    puts(prompt_str)
    ss = input("-->").strip()
    if type == str:
      return ss
    else: # type == int > 0
      try:
        ii = int(ss)
      except:
        continue
      if ii > 0:
        return ii

# Takes a class
# Returns a list filled with objects of passed class
def fill_list(cls):
  rv = []
  while True:
    prompt = "'A' to add a new " + cls.__name__ + \
      " || 'D' to delete a " + cls.__name__ + \
      " || 'L' to list " + cls.__name__ + "s" + \
      " || 'Q' to quit when finished"
    ss = get_input(prompt)

    if "A" == ss.upper():
      rv.append(cls(get_input("Enter " + cls.__name__)))
    elif "D" == ss.upper():
      puts(str(rv.pop(get_input("Enter index of " + cls.__name__ + " to delete", int)-1)) + " deleted")
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
        print(cls.__name__ + " list is empty")
    else:
      puts("Invalid command")

if not sys.flags.utf8_mode:
  print("Not in UTF-8 mode. Aborting.")
  exit(1)
      
puts("Welcome to the interactive random selection program")

_S_ = get_input("How many candidates are being selected?", int)
puts("Performing selection for " + str(_S_) + " candidate(s)")

puts("Enter candidates")
candidates = fill_list(Candidate)

puts("Enter _P_ values")
p_values = fill_list(P_value)
_D_ = "/" + "/".join([pp.to_hex() for pp in p_values])

puts("_S_:" + str(_S_))
puts("_D_:" + _D_)

output = []
for cc in candidates:
  output.append((hashlib.sha256(cc.to_hex(_D_).encode("utf8")).hexdigest(), str(cc)))

for ii in sorted(output, key=lambda hash: hash[0]):
  puts("hash:" + ii[0] + " candidate:" + ii[1])
