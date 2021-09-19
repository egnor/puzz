"""
A solver for rectangular black-and-white nonograms.

Takes too long on very large grids but seems to be okay for up to
40x40 or so.
"""

# many techniques taken from http://www.comp.lancs.ac.uk/~ss/nonogram/

import sys
import re

# bunny
#ROWS = "2 4,2 1,1,4 1,1,1,1 1,1,1,1 1,1,1,1 1,1,1,1 1,1,1,1 1,2,2,1 1,3,1 2,1 1,1,1,2 2,1,1,1 1,2 1,2,1"
#COLS = "3 3 10 2 2 8,2 2 1,2,1 2,1 7 2 2 10 3 2"

# wot
#ROWS = "7,4,6 5,1,1,5 4,1,4 3,3,3 2,1,2 1,5,1 2,2 2,2 1,1,1,1 5,1,1,5 1,1,1,1,1,1,1,1,1,1 1,1,1,5,5,1,1,1 1,1,1,1,1,1,1,1,1,1 1,1,1,2,2,1,1,1 3 1,1,1,1,3 1,1,1,3,3,1 1,1,1,2,2,1,2 1,5,2,2,1,1 2,1,1,3,2,1,2"
#COLS = "6,3,2 5,1,1,1 4,4 3,1,1,4 2,4,2 1,1,1,4 1,3,2 1,4 5 2,1,2 4,2,1,3,4 1,1,1,2,1,1 1,3,1,4 2,1,2,2 2,1,3 2,1,1 5,5 1,1,1 3 1,1,1,1 2,4,1,1,1 3,1,1,3 4,4 5,1,1,1 6,3,2"

# UT no more
#ROWS="2,2,6,18 2,2,6,11 2,2,2,6 18,3 2,2,2,12,2 2,2,2,3,4,1 6,2,3,7,3 5,2,3,7,3,2 2,8,5,2 3,1,9,6,1 1,2,9,6 7,2,2,9,7,1 11,2,2,9,8,2 13,1,9,7,2 15,1,3,9,8,3 3,5,3,2,3,8,7,3 3,3,3,1,4,8,8,4 4,1,1,4,1,3,7,7,4 7,7,1,8,7,5 5,5,1,2,3,7,6 4,4,1,2,4,4,6 11,1,2,11,6 1,1,1,1,1,1,1,2,16,2 2,1,1,1,2,1,2,2,13,1 10,1,2,2,11,2 9,2,1,9,6,2 1,5,1,1,12,1,3 2,1,1,16,4 3,2,1,18,4 4,2,17,3 5,1,12,3,1 7,2,3,9,2,1 10,2,5,5,1,2 14,3,6,1,3 18,2,9,3"
#COLS = "5,9 7,8 1,13,7 1,3,5,3,6 1,4,5,2,5 7,5,4,4,4 8,8,2,3,4 1,2,6,1,4,3 1,2,8,2,3,3 8,5,4,4,3 8,4,5,2,2 1,3,5,3,2 2,1,12,2 2,1,7,2 8,5,1 8,1 2,1,11,1 2,1,4,4,1 1,2,2,6,2 1,3,4,8,3 2,1,4,2,2 3,2,3,3,1,2 1,2,1,4,5,1 2,2,6,3,5,1,2 1,8,3,6,2,1 2,9,3,6,2 1,10,2,5,2 1,2,12,3,6,2 1,1,14,3,6,3 1,1,14,3,6,2 1,1,11,3,6,2 1,1,9,2,4,6,2 1,1,7,4,3,6,1 1,1,5,7,3,7,1 2,1,4,9,3,6,1 2,1,10,4,6,1 2,1,14,4,6,1 2,2,13,3,7 2,2,11,1,3,4 3,1,9,3,4,1,1 3,2,7,4,2,3,1 3,1,4,7,1,5,2 4,2,9,5,1 5,2,11,6,2 6,2,9,6,3"

# warship
#ROWS = "2 2 2 2 12 2 2 2 2 2 2 2 2 2 2 2 14 14 1,2 1,2 1,2 1,2 11,2 1,2 1,2 1,2 1,2 1,5 1,5 1,5 1,5 1,5 1,5 1,24 32 26 26 26 3,8,7,2 3,7,6,2 3,7,6,2 3,7,6,2 3,8,7,2 26 34 34 34 34 34 24 5,3,5 3,5,3,5 2,2,24 1,1,24 2,29 5,24,2 3,26,2 41,3 43,2 42,3 41,2 41,2 4,2,2,2,2,5 42 42 42 64 86 83 65 75 71 60,10 6,53,10 6,25,24,10 19,17,3,44 30,12,40 12,19,22 9,24,16 4,20,8,11 5,24,6,2,3 38,6,2,6 45,8,8 52,3 51,1 51,2 50,1 50,1 50,1 34,9,2 31,6,7,7,1 29,10,6,3,5,1 27,8,5,5,3,1 25,5,5,4,10,5,2 23,3,11,2,3,3,5,1 20,3,16,2,8,11,1 18,2,8,4,1,9,3,7,2 15,4,8,5,4,12,5,9,1 11,5,7,8,2,14,5,11,1 7,7,6,13,9,15,15"
#COLS = "2 4 8 2,13 2,17 2,18 2,19 2,19 2,19 1,2,19 2,2,19 2,2,19 2,2,19 2,2,19 2,2,19 2,2,18 2,26,1 2,9,17,1 2,10,17,1 2,10,16,2 2,9,17,2 2,9,17,2 2,3,3,16,3 13,16,2 13,15,1 12,16,2,1 12,15,2,1 12,15,1,2 11,15,2,3 11,15,1,3 11,14,2,4 1,3,20,14,1,3 1,1,2,23,13,1,4 1,1,1,21,14,2,4 1,1,5,2,22,13,3,3,1 1,1,5,4,5,13,13,2,3,1 1,1,5,2,5,13,12,2,3,1 31,1,6,13,12,3,3,2 1,15,1,6,13,12,3,2,2 1,29,13,12,3,2,3 1,5,32,13,3,2,3 1,42,13,2,3,3 1,29,12,13,2,3,3 29,12,14,1,3,3 2,17,10,12,4,8,3,2 1,2,17,10,12,3,8,4,1 1,2,17,10,12,3,2,9,4,1 1,2,17,23,3,2,10,3 1,2,6,8,22,3,2,11,3 1,2,11,19,11,4,2,11,3 38,19,11,4,2,13,1 38,19,11,25 1,2,11,7,10,12,1,1,3 1,2,12,8,10,12,1,1,5 1,2,17,23,1,1,7 1,2,17,24,1,1,7 1,2,17,10,13,1,1,8 2,17,10,13,1,1,3,5 29,13,4,3,4 29,14,2,4,4 5,19,14,1,2,4 29,14,1,1,3 44,2,2,2 5,20,2,3,1 5,5,14,2,2,2 5,5,15,3,2,1 5,5,15,3,3,1 5,5,15,6,1 5,15,3,3 21,3,3 21,3,3 22,2,2 2,17,2,2 2,2,13,3,1 1,2,13,2,1 2,2,13,2,1 2,1,6,5,4 1,2,14,4 1,14,4 14,2 14,2 14,3 14,2 14,2 15,2 15,2 15,2 5,2,1,1 2,1,2,1,1 2,1,2,1,1 2,1,2,1,1 2,1,2,2,1 2,1,2,2,1 1,2,1,1 1,2,1,1 2,1,4 2,1,4 2,2,5 2,2,5 3"

# howdy-ho
#ROWS="25 1,1 1,3,1 1,6,1 1,8,1 1,9,1 1,3,6,1 1,3,4,1 1,1,4,2,1 1,2,2,2,2,1 2,2,1,1,2,1 2,1,1,1,1,1,1 1,3,4,1,1,4 1,2,2,4,1,2 1,2,1,2,3,1,1 1,8,2,2,1 1,6,3,1 1,9,1 1,7,1 1,7,1 1,5,1 1,4,1 1,5,1 1,6,1 1,7,1 1,7,1 1,7,1 1,7,1 1,7,1 1,5,1 1,5,1 1,3,1 1,2,1 1,1 25"
#COLS="35 1,2,1 1,1,1,1 1,2,1,1 1,4,1 1,2,1 1,2,5,1 1,1,5,9,1 1,1,1,2,18,1 1,2,24,1 1,4,1,17,1 1,3,1,4,16,1 1,2,1,1,6,6,1 1,4,2,5,3,1 1,4,1,2,1,1 1,6,3,2,1 1,9,1,1 1,8,2,1 1,5,2,1 1,1,1 1,2,1 1,1,1,1 1,1,2,1 1,2,1 35"

# artist
#ROWS="2 2 2 2 2 2 4 4 6 4,1 5 4 4 4 4 4 4 5 6 3,2 3,2 3,2 3,2 3,2 3,2 6 6 7 4,2 4,2 4,2,5 4,2,8 7,9 7,11 7,11 7,13 5,1,1,5,5 5,1,2,7,5 5,2,2,7,6 5,2,2,2,13 5,2,5,12 5,2,3,1,13 5,2,4,17 5,2,2,2,15 5,1,2,3,14 5,1,5,1,12 5,1,5,1,12 5,1,5,16 5,1,5,2,13 5,2,5,2,14 5,2,5,4,15 5,2,6,6,1,16 5,1,11,1,1,1,14,1 5,1,9,2,2,7,6,1 5,1,9,7,7,9 5,1,16,8,8,1 5,1,14,8,8,1 5,1,21,8,1 5,1,20,9,1 5,2,5,8,8,1 5,3,8,8,1 5,3,7,5,2 5,3,6,5,2 3,1,3,4,3,7,1,4,2 12,3,4,5,3,2 12,2,3,5,2 12,1,7,6,2 12,4,2,4,9,2 3,1,1,2,2,3,13,2 5,1,3,2,17,2 5,21,19,2 5,19,20,2 5,4,22,2 5,33,2 5,11,20,2 5,12,27 5,12,28 5,11,29 5,9,30 5,8,30 5,9,30 5,8,7,3,5 5,8,7,5,5 5,8,6,6,5 5,8,4,7,5 5,8,3,9,5 5,1,8,2,11,5 5,1,8,2,12,5 5,1,8,2,13,5 5,1,8,2,15,5 5,1,8,2,2,5 5,5,9,2,21 5,1,1,8,2,2,16 5,1,3,8,2,2,14 5,1,3,8,2,2,12 5,1,3,7,2,2,12 5,5,7,2,2,2,8 14,5,2,2,8 31,7,2,2,4,4 31,8,6,4,4"
#COLS="2 2 2 2 2 2 2 2 2 2 2 3 3 4,82 100 100 13,38,4,31 1,18,68 3,19,4,3 17,4,3 14,4,9 1,11,4,1,4 2,9,1,7 2,8,6,7 2,8,9 5,2 7,2 4,2,2 1,6,2 1,6,1,2 6,2,2 5,2 5,2 5,2 5,2,2 5,2,6 5,2,8 5,2,11 5,2,15 5,2,19,1 6,25,2 7,28,2 7,2,27,2 2,5,1,9,20 2,1,5,3,2,5,17 6,9,2,2,2,4,5,15 3,6,2,7,1,4,3,7,12 12,2,6,2,3,2,8,7 12,2,6,1,4,1,10 14,2,1,5,1,2,1,14 14,2,6,2,1,1,28 8,6,2,8,1,1,2,29 6,10,2,2,3,11,1 15,1,11,3,3,30 33,2,31 31,2,21,1,1 34,12,8,1 4,26,12,8,1 25,13,7,2 20,2,13,6,2 11,7,2,13,5,3 13,1,1,13,5,3 17,1,14,4,4 18,14,4,6 17,1,15,3,6,1 16,16,2,5,2 34,1,5,3 2,27,1,9 30,8 10,9,23 5,7,25 25 25 39 26,2"

#ROWS = [[int(j) for j in i.split(",")] for i in ROWS.split()]
#COLS = [[int(j) for j in i.split(",")] for i in COLS.split()]

ON = "#"
OFF = "+"
UNKNOWN = "-"

# raising this value makes the exhaustive search of a single line take
# longer, but might reduce the amount of guessing.  
CUTOFF = 500

class NoSolution(ValueError):
  pass

class UselessGuess(ValueError):
  pass

def read_nonogram_file(f):
  print("reading nonogram input from %s..." % (f,), file=sys.stderr)
  if isinstance(f, str):
    f = open(f)
  state = 0
  rows = []
  cols = []
  curr = rows
  for line in f:
    line = line.strip()
    if not line:
      if state == 1:
        state = 2
        curr = cols
      elif state == 3:
        print("read %d rows and %d columns" % (len(rows), len(cols)))
        return rows, cols
    else:
      state = (state/2)*2 + 1
      curr.append([int(i) for i in re.split(r"[ ,-]+", line)])

  print("read %d rows and %d columns" % (len(rows), len(cols)), file=sys.stderr)
  return rows, cols
          

class Line(object):
  def __init__(self, name, values, size, parent=None, index=None, state=None, verbose=False):
    self.verbose = verbose
    self.name = name
    self.parent = parent
    self.index = index
    
    self.values = tuple(values)
    if len(self.values) == 1 and self.values[0] == 0:
      self.values = ()
    self.size = size
    if state:
      self.s = state
      assert size == len(self.s)
    else:
      self.s = UNKNOWN * size
    self.done = False
    self.stack = []

    temp = [size+1]
    for i in reversed(values):
      temp.append(temp[-1] - (i+1))
    self.maxstart = list(reversed(temp[1:]))
    self.minstart = [0]
    for i in values[:-1]:
      self.minstart.append(self.minstart[-1] + (i+1))

  def push(self):
    self.stack.append((self.s, self.done))

  def pop(self):
    self.s, self.done = self.stack.pop()

  def solve(self):
    if self.done:
      return 0

    size = self.size
    
    if not self.values:
      self.s = OFF * size
      if self.parent:
        for i in range(self.size):
          self.parent.update(self.index, i, OFF)
      self.done = True
      return size

    possible = set([i for i in range(size) if self.s[i] == UNKNOWN])
    if not possible:
      self.done = True
      return 0
    start_possible_size = len(possible)
    if self.verbose:
      print("possible set: ", possible)
      print(" start state: ", self.s)
    values = None
    count = 0
    for s in self.find_solutions():
      count += 1
      if count > CUTOFF:
        #print "giving up on", self.s, self.values
        return 0
      
      if self.verbose:
        print(s)
      if not values:
        values = dict((i, s[i]) for i in possible)
      else:
        remove = set()
        for p in possible:
          if s[p] != values[p]:
            remove.add(p)
        possible.difference_update(remove)
        if not possible: break

    if values is None:
      raise NoSolution("no solutions starting with " + self.s)

    if self.verbose:
      print("forced positions:", ["%d=%s" % (i, values[i]) for i in possible])
    s = list(self.s)
    for i in possible:
      if self.parent:
        self.parent.update(self.index, i, values[i])
      s[i] = values[i]
    self.s = "".join(s)

    if start_possible_size == len(possible):
      self.done = True

    return len(possible)

  def set(self, pos, value):
    self.s = self.s[:pos] + value + self.s[pos+1:]
 
  def __str__(self):
    return self.s

  def find_solutions(self):
    return self.place_block(0, 0, self.s);

  def place_block(self, b, p, s):
    if b >= len(self.values):
      if not ON in s[p:]:
        yield s.replace(UNKNOWN, OFF)
      return

    v = self.values[b]
    for i in range(max(self.minstart[b], p), self.maxstart[b]+1):
      #print "trying block", b, "at", i
      if i > 0 and s[i-1] == ON:
        #print "skipped ON at %d" % (i-1,)
        break
      for k in range(i, i+v):
        if s[k] == OFF:
          #print "  blocked by OFF at", k
          break
      else:
        if i+v >= self.size:
          new_s = s[:i] + (ON*v)
          for j in self.place_block(b+1, i+v+1, new_s):
            yield j
        elif s[i+v] != ON:
          new_s = s[:i] + (ON*v) + OFF + s[i+v+1:]
          for j in self.place_block(b+1, i+v+1, new_s):
            yield j

class Nonogram(object):
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.height = len(rows)
    self.width = len(cols)

  def solve(self):
    self.R = [Line("row %d" % (i,), r, self.width, self, i)
              for (i, r) in enumerate(self.rows)]
    self.C = [Line("col %d" % (i,), c, self.height, self, -1-i)
              for (i, c) in enumerate(self.cols)]

    R = self.R[:]
    C = self.C[:]
    R.reverse()
    C.reverse()
    self.A = []
    while R or C:
      if R: self.A.append(R.pop())
      if C: self.A.append(C.pop())

    self.recurse([])

  def select_guess_location(self):
    locs = []
    for y, r in enumerate(self.R):
      for x, k in enumerate(r.s):
        if k == UNKNOWN:
          score = 0
          if x > 0 and r.s[x-1] == ON:
            score += 10
          if x < r.size-1 and r.s[x+1] == ON:
            score += 10
          locs.append((score, x, y))
    locs.sort(reverse=True)
    return [i[1:] for i in locs]

  def recurse(self, guesses, init=None):
    first = True
    while True:
      if not self.find_forced(init) and first:
        raise UselessGuess()

      first = False

      for i in self.A:
        if not i.done:
          break
      else:
        return

      #self.dump()
      #raw_input()

      locs = self.select_guess_location()
      #print len(locs), "unknowns left"
      for x, y in locs:
        #print "guessing at", x, y
        r = self.R[y]
        c = self.C[x]

        for i in self.A:
          i.push()

        r.set(x, ON)
        c.set(y, ON)
        try:
          return self.recurse(guesses+["%d,%d:ON" % (x,y)],
                              init=[r,c])
        except NoSolution:
          for i in self.A:
            i.pop()
          r.set(x, OFF)
          c.set(y, OFF)
          break
        except UselessGuess:
          #print "useless"
          for i in self.A:
            i.pop()
          r.set(x, UNKNOWN)
          c.set(y, UNKNOWN)

  def find_forced(self, init=None):
    if not init:
      q = self.q = self.A[:]
    else:
      q = self.q = init
    queued = self.queued = set(q)

    updated = 0
    while q:
      l = q.pop(0)
      queued.remove(l)
      if not l.done:
        updated += l.solve()

    return updated

  def update(self, index, pos, v):
    if index >= 0:
      #print "row %d update pos %d = %s" % (index, pos, v)
      other = self.C[pos]
    else:
      index = -1-index
      #print "col %d update pos %d = %s" % (index, pos, v)
      other = self.R[pos]

    other.set(index, v)
    if other not in self.queued:
      self.queued.add(other)
      self.q.append(other)

  def dump(self):
    for r in self.R:
      print(r, "  ", ",".join([str(i) for i in r.values]))

  def show(self, off=OFF, on=ON, unknown=UNKNOWN):
    print()
    m = {OFF: off, ON: on, UNKNOWN: unknown}
    for r in self.R:
      rp = "".join(m[i] for i in r.s)
      print("   ", rp, "  ", " ".join(str(i) for i in r.values))
    print()
      

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("""
    Usage: %s <inputfile>

 inputfile contains rows top-to-bottom, a blank line, then columns
 left-to-right.  Values in a line can be separated by spaces, commas,
 or hyphens.
 """)
    sys.exit(2)
 
  f = sys.argv[1]
  rows, cols = read_nonogram_file(sys.argv[1])
  n = Nonogram(rows, cols)
  n.solve()
  n.show('  ', '##')
  
