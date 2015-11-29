import sys
import pprint

DIRS_4 = ((1,0), (-1,0), (0,1), (0,-1))
DIRS_8 = DIRS_4 + ((1,1), (1,-1), (-1,1), (-1,-1))

HIGHLIGHT_ON = "\x1b[1;7m"
HIGHLIGHT_OFF = "\x1b[0m"

def read_lettergrid_file(f):
  if isinstance(f, str):
    f = open(f)
  grid = []
  maxlen = 0
  for line in f:
    line = line.rstrip()
    if not line: continue
    grid.append(line)
    maxlen = max(maxlen, len(line))
  for i, row in enumerate(grid):
    grid[i] = row + " " * (maxlen-len(row))
  return tuple(grid)
  

class Done(Exception):
  def __init__(self, path):
    self.path = path

class GeneralizedWordSearch(object):
  def __init__(self, grid, dirs, changedir, reuse):
    self.grid = grid
    self.dirs = dirs
    self.changedir = changedir
    self.reuse = reuse

    self.height = len(grid)
    self.width = len(grid[0])

    self.index = None

  def build_index(self, prefixlen=3):
    self.index = {}
    self.index_length = prefixlen
    
    for j, row in enumerate(self.grid):
      for i, k in enumerate(row):
        for d in self.dirs:
          ni, nj = i + d[0], j + d[1]
          if not (0 <= ni < self.width) or not (0 <= nj < self.height): continue
          self.index_recur(k + self.grid[nj][ni],
                           [(i, j), d, (ni, nj)], set(((i,j), (ni, nj))), prefixlen)

  def index_recur(self, prefix, path, used, prefixlen):
    self.index.setdefault(prefix, []).append(tuple(path))
    if len(prefix) >= prefixlen:
      return

    if self.changedir:
      dirs = self.dirs
    else:
      dirs = (path[-2],)

    i, j = path[-1]
    for d in dirs:
      ni, nj = i + d[0], j + d[1]
      if not (0 <= ni < self.width) or not (0 <= nj < self.height): continue
      if self.reuse == False and (ni, nj) in used: continue
      path.append(d)
      path.append((ni,nj))
      used.add((ni,nj))
      self.index_recur(prefix + self.grid[nj][ni], path, used, prefixlen)
      used.remove((ni,nj))
      path.pop()
      path.pop()

  def find(self, what=None):
    if what is None:
      import words
      what = words.all
    elif isinstance(what, str):
      return self.find_one(what)

    result = {}
    for w in what:
      p = self.find_one(w)
      if p:
        result[w] = p
    return result
  

  def find_one(self, word):
    if self.index is None:
      self.build_index()

    if len(word) <= self.index_length:
      return self.index.get(word, (None,))[0]

    prefix = word[:self.index_length]
    paths = self.index.get(prefix, ())
    try:
      for p in paths:
        used = set(p[::2])
        self.find_recur(prefix, list(p), used, word)
    except Done, e:
      return e.path

    return None

  def find_recur(self, prefix, path, used, word):
    if prefix == word:
      raise Done(path)

    if self.changedir:
      dirs = self.dirs
    else:
      dirs = (path[-2],)
      
    next = word[len(prefix)]
    i, j = path[-1]
    for d in dirs:
      ni, nj = i + d[0], j + d[1]
      if not (0 <= ni < self.width) or not (0 <= nj < self.height): continue
      if self.grid[nj][ni] != next: continue
      if self.reuse == False and (ni, nj) in used: continue
      path.append(d)
      path.append((ni,nj))
      used.add((ni,nj))
      self.find_recur(prefix + next, path, used, word)
      used.remove((ni,nj))
      path.pop()
      path.pop()

  def show(self, highlight=None):
    if not highlight:
      print
      print "  " + "\n  ".join(self.grid)
      print
    else:
      print 
      for j, row in enumerate(self.grid):
        out = []
        for i, k in enumerate(row):
          if (i,j) in highlight:
            out.append(HIGHLIGHT_ON + k + HIGHLIGHT_OFF)
          else:
            out.append(k)
        print "  " + "".join(out)
      print
      

class WordSearch(GeneralizedWordSearch):
  def __init__(self, grid, dirs=DIRS_8):
    GeneralizedWordSearch.__init__(self, grid, dirs, False, True)

class Boggle(GeneralizedWordSearch):
  def __init__(self, grid, dirs=DIRS_8):
    GeneralizedWordSearch.__init__(self, grid, dirs, True, False)

    
if __name__ == '__main__':
  if len(sys.argv) < 2:
    print """
    Usage: %s <inputfile>

 inputfile contains a letter grid.  All blank lines are ignored.
 Letters should be in the same case as the dictionary (the standard
 puzz dictionaries are lowercase).
 """
    sys.exit(2)

  import words

  grid = read_lettergrid_file(sys.argv[1])
  if "boggle" in sys.argv[0]:
    w = Boggle(grid)
  else:
    w = WordSearch(grid)
  print 
  print "  searching grid for %d words..." % (len(words.all),)
  all = w.find(words.all)
  all = all.keys()
  all.sort()
  print "  %d words from dictionary found" % (len(all),)
  reduced = words.remove_substrings(all)
  reduced.sort()
  print "  (%d words after removing substrings)" % (len(reduced),)
  print
  print "  interactive mode:  enter '?' for help"
  print

  while True:
    try:
      i = raw_input("> ").strip()
    except EOFError:
      break
    if not i: break
    if i == "?":
      print """
      ?  print this help message
      *  print all dictionary words found
      /  print all dictionary words found (suppress substrings)
      &  print grid
      """
      continue
    if i == "*":
      x = [i for i in all if len(i)>6]
      words.print_compact_list(x)
      print len(x)
      print
      continue
    if i == "/":
      x = [i for i in reduced if len(i)>6]
      words.print_compact_list(x)
      print len(x)
      print
      continue
    if i == "&":
      w.show()
      continue
    
    p = w.find(i)
    if not p:
      print "\n  not found\n"
    else:
      w.show(highlight=p[::2])
