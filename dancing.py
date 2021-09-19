"""
Dancing Links is a solver for the "exact cover" problem: given an
incidence matrix (a matrix whose values are all either 0 or 1), find a
subset of the rows such that each column contains exactly one 1 (in
the select rows).  For instance:

         A  B  C  D  E  F  G
     #1        1     1  1
     #2  1        1        1
     #3     1  1        1
     #4  1        1
     #5     1              1
     #6           1  1     1

Rows 1, 4, and 5 are a solution to the problem: together they have a
single one in each column A-G.  (For this matrix that is in fact the
only solution.)

This problem is known to be NP-complete and this implementation
doesn't magically change that, but for many puzzle-sized practical
instances of this problem it is tractable.

The algorithm is simple: select a row, remove all columns covered by
that row and all rows that conflict with the selected row (as well as
the selected row itself), and recurse on the smaller matrix that
results.  If you reach a state where you have no columns left, the
selected rows are a solution.  If you reach a state where you have
columns left but no rows left, you must backtrack.  'Dancing links' is
really just a way of representing the matrix that makes removing rows
and columns and putting them back fast.

To use this code:

1. Create a Matrix object.

2. Add columns.  Each column has a name, which can be any hashable
python object.  To use the "optional columns" feature, the names must
be strings (which is usually what's wanted anyway.)

3. Add rows.  Each row has a name, which can be any python object, and
a list of the column names that are covered by that row.

4. Call Solve(), which returns an iterator over all the solutions.
Each solution is a list of row names that together cover all the
columns.  If you only want a single solution you can discard the
iterator after you've obtained the first value.


The Matrix class supports a couple of features that deviate from the
"exact cover" problem definition but which are useful in practice:
columns can be marked optional, which means they may not be covered at
all (but will not be covered multiple times); and you can set a column
size, which is the number of times a solution must cover that column
(if you want something other than 1, which is the default).
"""

import time
import random

class DLNode(object):
  def __init__(self, name, nodelist):
    self.name = name
    self.size = 0
    nodelist.append(self)

    self.need = 1
    self.have = 0

    self.l = self
    self.r = self
    self.u = self
    self.d = self
    self.c = self

  def iterup(self):
    x = self.u
    while x != self:
      yield x
      x = x.u

  def iterdown(self):
    x = self.d
    while x != self:
      yield x
      x = x.d

  def iterleft(self):
    x = self.l
    while x != self:
      yield x
      x = x.l

  def iterright(self):
    x = self.r
    while x != self:
      yield x
      x = x.r

  @staticmethod
  def cover_column(c):
    c.have += 1
    if c.have < c.need: return

    c.r.l = c.l
    c.l.r = c.r
    for i in c.iterdown():
      for j in i.iterright():
        j.d.u = j.u
        j.u.d = j.d
        j.c.size -= 1

  @staticmethod
  def uncover_column(c):
    if c.have == c.need:
      for i in c.iterup():
        for j in i.iterleft():
          j.c.size += 1
          j.d.u = j
          j.u.d = j
      c.r.l = c
      c.l.r = c
    c.have -= 1


class Matrix(object):
  def __init__(self):
    self.nodes = []
    self.h = DLNode(None, self.nodes)
    self.colindex = {}

  def Discard(self):
    """Python's garbage collection doesn't do great with circular
    reference chains, of which this class creates *many*.  This breaks
    up the circular references so objects can be discarded via
    reference count.  Useful in long-running servers."""
    for n in self.nodes:
      n.l = None
      n.r = None
      n.u = None
      n.d = None
      n.c = None
    self.nodes = None
    self.colindex = None

  def AddColumns(self, colnames):
    """Create columns from the given sequence of column names."""
    h = self.h
    for cname in colnames:
      # create a new column
      c = DLNode(cname, self.nodes)
      c.l = h.l
      c.r = h
      h.l.r = c
      h.l = c

      self.colindex[cname] = c

  def ShuffleColumns(self):
    """Randomize the order of columns in the matrix; this has the
    effect of shuffling the order in which Solve() returns
    solutions.  Doesn't change the number of solutions."""
    for c in self.h.iterright():
      nodes = list(c.iterdown())
      nodes.append(c)
      random.shuffle(nodes)
      offset = nodes[1:]
      offset.append(nodes[0])
      for a, b in zip(nodes, offset):
        a.d = b
        b.u = a

  def MakePrefixOptional(self, prefix):
    """Make all columns whose name begins with 'prefix' optional, so
    they may be covered 0 or 1 times (but not more than 1).  Assumes
    all column names are strings."""
    to_remove = [c for c in self.h.iterright() if c.name.startswith(prefix)]
    for c in to_remove:
      c.r.l = c.l
      c.l.r = c.r
      c.l = c
      c.r = c

  def SetColumnSize(self, cname, need):
    """Set the number of times that this column must be covered (the
    default is 1)."""
    if cname in self.colindex:
      self.colindex[cname].need = need

  def AddRow(self, name, colnames):
    """Add a row to the matrix, which covers the columns named in
    'colnames'."""
    row = []
    h = self.h
    for cname in colnames:
      if cname not in self.colindex:
        # create a new column
        c = DLNode(cname, self.nodes)
        c.l = h.l
        c.r = h
        h.l.r = c
        h.l = c

        self.colindex[cname] = c
      else:
        c = self.colindex[cname]

      c.size += 1
      x = DLNode(name, self.nodes)
      x.c = c
      # add x to the end of the c column
      x.u = c.u
      x.d = c
      c.u.d = x
      c.u = x

      row.append(x)

    # stitch together all the row nodes
    for i, x in enumerate(row):
      x.l = row[(i-1+len(row)) % len(row)]
      x.r = row[(i+1+len(row)) % len(row)]

  def DumpColumns(self):
    """Print the name and size of all columns in the matrix."""
    for c in self.h.iterright():
      print((c.name, c.size))

  def _Recur(self, solution, k):
    if self.h.r == self.h:
      yield solution
      return

    # choose column c
    c = min((i.size, id(i), i) for i in self.h.iterright())[-1]

    c.cover_column(c)

    for r in c.iterdown():
      solution.append(r.name)

      for j in r.iterright():
        j.c.cover_column(j.c)
      for s in self._Recur(solution, k+1):
        yield s
      for j in r.iterleft():
        j.c.uncover_column(j.c)
      solution.pop()

    c.uncover_column(c)

  def Solve(self):
    """Generator object that yields solutions.  Each solution is a
    list of row names."""
    return self._Recur([], 0)


def test():
  A = Matrix()
  A.AddColumns("ABCDEFG")
  A.AddRow("1", "CEF")
  A.AddRow("2", "ADG")
  A.AddRow("3", "BCF")
  A.AddRow("4", "AD")
  A.AddRow("5", "BG")
  A.AddRow("6", "DEG")

  A.DumpColumns()
  A.ShuffleColumns()
  for x in A.Solve():
    print(x)


if __name__ == '__main__':
  test()
