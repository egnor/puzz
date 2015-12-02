"""Solves a pentomino packing problem using dancing links."""

# This is mostly meant as sample code for doing omino packing.

import dancing
from ominoes import *

def show_table(table, os):
  out = []

  for (i, j), k in table.iteritems():
    while len(out) < j+1: out.append([])
    while len(out[j]) < i+1: out[j].append(' ')
    out[j][i] = k

  for o, a, i, j in os:
    cells = o.aspects[a]
    for ci, cj in cells:
      out[j+cj][i+ci] = o.name

  for row in out:
    print "".join(row)


# A classic pentomino problem:  select any pentomino.  Remove it from
# the set of 12.  Use 9 of the remaining pentominoes to make the shape
# of the chosen pentomino, but 3x as tall and wide.
#
# In this case we've chosen the F pentomino.
SHAPE = """
   ......
   ......
   ......
......
......
......
   ...
   ...
   ...
"""

# We can use all the pentominoes except the F itself.
ELIGIBLE = [o for o in Omino.BY_SIZE[5].itervalues() if o.name != 'F']

table = cells_from_string(SHAPE)

D = dancing.Matrix()
D.AddColumns(["c%d,%d" % ij for ij in table])
D.AddColumns(["p%s" % o.name for o in ELIGIBLE])
# Because we don't require using every pentomino (and in fact we
# can't; we have 11 and need exactly 9), we make the pentomino columns
# optional.
D.MakePrefixOptional("p")

# Now construct a row for each legal placement of each pentomino.
for o in ELIGIBLE:
  for a, cells in enumerate(o.aspects):
    for i, j in table:
      # Consider placing 'cells' with its origin at (i, j).
      cols = ["p"+o.name]
      for (ci, cj) in cells:
        pij = (ci+i, cj+j)
        if pij not in table:
          # This placement extends outside the goal shape.
          break
        cols.append("c%d,%d" % pij)
      else:
        # All cells fall inside the shape.
        D.AddRow((o, a, i, j), cols)

        # Display the goal shape with this single pentomino positioned
        # inside it.
        #show_table(table, ((o, a, i, j),))

solutions = 0
for x in D.Solve():
  show_table(table, x)
  solutions += 1
print
print "%d solutions found." % (solutions,)
