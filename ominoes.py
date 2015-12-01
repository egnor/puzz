import collections


def cells_from_string(text):
  """Given a multiline string, return a dict of {(col, row): character}
  for each non-space, non-newline character."""
  out = {}
  for j, row in enumerate(text.split("\n")):
    for i, k in enumerate(row):
      if k == ' ': continue
      out[(i,j)] = k
  return out


class Omino(collections.namedtuple(
    'Omino', ["name", "cells", "aspects", "symmetries"])):
  """
  Omino instances represent polyominoes (pentominoes, hexominoes, etc).
  The omino is described at a certain arbitrary orientation.
  Ominoes are typically retrieved from global values in this module
  (eg. pentominoes), not created directly by the caller.

  Attributes:
    name: Common name of this polyomino (e.g. 'R').
    cells: Tuple of (x, y) coordinates of cells in the polyomino.
      Cells are always in normalized form: cells are lexiographically
      increasing, with the first cell always (0, 0).
    aspects: A tuple of normalized cell tuples, representing all the
      distinct reflections and rotations of the polyomino.  Will
      contain from 1 to 8 elements, depending on the symmetries of the
      shape.  One of the elements will be identical to 'cells'.
    symmetries: Set of symmetries, out of '|', '-', '+' (180-degree
      rotation), '/', '\', '@' (90-degree rotation).
  """

  @classmethod
  def normalize(cls, h):
    """Given a sequence of cell locations, return them in normalized
    form (lexicographically increasing from (0, 0), which is always
    the first element if the input is nonempty."""
    h = sorted(h)
    rx = h[0][0]
    ry = h[0][1]
    h = [(x-rx, y-ry) for (x, y) in h]
    h = tuple(h)
    return h

  @classmethod
  def flip(cls, h):
    """Reflect a cell tuple across the Y-axis."""
    return cls.normalize([(-i, j) for (i, j) in h])

  @classmethod
  def rotate(cls, h):
    """Rotate a cell tuple 90 degress (clockwise, if the y-axis points up)."""
    return cls.normalize([(-j, i) for (i, j) in h])

  @classmethod
  def extract_ominoes(cls, picture):
    """Given a multiline ASCII art, create polyominoes for each unique
    non-space character.  The character becomes the polyomino's name."""
    d = cells_from_string(picture)
    bn = {}
    for p, k in d.iteritems():
      bn.setdefault(k, []).append(p)
    for name, cells in bn.iteritems():
      Omino(name, cells)

  # List of all Omino objects
  ALL = []
  # Dict of {size: {name: omino_object}}
  BY_SIZE = {}

  _PICTURE_CACHE = {}

  def __new__(cls, name, cells):
    # Generate all 8 possible rotations/reflections.
    h = cls.normalize(cells)
    fh = cls.flip(h)
    rh = cls.rotate(h)
    rfh = cls.rotate(fh)
    rrh = cls.rotate(rh)
    rrfh = cls.rotate(rfh)
    rrrh = cls.rotate(rrh)
    rrrfh = cls.rotate(rrfh)

    # These are all normalized, so making a set will collapse any
    # duplicates.  We sort and convert to a tuple so indexes into the
    # aspects are stable.
    aspects = tuple(sorted(set([h, fh, rh, rfh, rrh, rrfh, rrrh, rrrfh])))

    sym = set()
    if h == fh: sym.add("|")
    if rh == rrrfh: sym.add("-")
    if h == rrh: sym.add("+")
    if h == rrrfh: sym.add("\\")
    if h == rfh: sym.add("/")
    if h == rh: sym.add("@")

    o = super(cls, Omino).__new__(
      cls, name=name, cells=h, aspects=aspects, symmetries=sym)
    cls.ALL.append(o)
    cls.BY_SIZE.setdefault(len(h), {})[name] = o
    return o

  def __len__(self):
    """Returns the degree of the polyomino (5 for a pentomino, etc)."""
    return len(self.cells)

  def __repr__(self):
    return '<%d-omino "%s">' % (len(self), self.name)

  def __hash__(self):
    return hash((self.name, self.cells))

  __str__ = __repr__

  def picture(self, char=None):
    """Return a multiline ASCII art picture of the polyomino."""
    if char is None: char = self.name
    key = (self, char)

    if key not in self._PICTURE_CACHE:
      min_j = min(c[1] for c in self.cells)
      out = []
      for i, j in self.cells:
        j -= min_j
        while len(out) < j+1: out.append([])
        while len(out[j]) < i+1: out[j].append(" ")
        out[j][i] = char
      self._PICTURE_CACHE[key] = "\n".join("".join(row) for row in out)

    return self._PICTURE_CACHE[key]


# 3-omino names from: https://en.wikipedia.org/wiki/Tromino,
# plus the unique "monomino" and "domino".
Omino.extract_ominoes("""
  M  DD  III  L
              LL
""")

# Names from: https://en.wikipedia.org/wiki/Tetromino
Omino.extract_ominoes("""
  IIII  OO
        OO
  L  Z
  L  ZZ  TTT
  LL  Z   T
""")

# Names from: https://en.wikipedia.org/wiki/Pentomino
# Using standard names, *not* Conway's notation.
Omino.extract_ominoes("""
       I
   FF  I  L  N
  FF   I  L  N   PP  TTT
   F   I  L  NN  PP   T
       I  LL  N  P    T
                   Y
 UU  V   W    X   YY ZZ
 U   V   WW  XXX   Y  Z
 UU  VVV  WW  X    Y  ZZ
""")

# From: http://puzzler.sourceforge.net/docs/polyominoes-intro.html#hexominoes
# Names were converted to a single character, if they weren't already:
#
#   High F = "F"  Low F = "f"
#   Long N = "N"  Short N = "n"
#   Tall T = "T"  Short T = "t"
#   Wa = "a"  Wb = "b"  Wc = "c"
#   Italic X = "x"
#   High Y = "Y"  Low Y = "y"
#   Tall Z = "Z"  Short Z = "z"
#   High 4 = "$"  Low 4 = "4"
#
# 'Short S' is omitted as it is a reflected 'Short N'.
Omino.extract_ominoes("""
                                     I
AAA  CC  D    EE   FF  ff   GG  H    I
AA   C   DD  EE   FF   f    G   HHH  I   J
A    C   DD   EE   F  ff    GG  H H  I J J
     CC  D         F   f     G       I JJJ
                                     I
     L       N   n
KK   L   MM NN  nn  OO  PP  QQ
KKK  L   M  N   nn  OO  PP  QQ
 K   L  MM  N   n   OO  P    QQ
     LL M   N           P

RR   S  TTT  tttt  U U   V
RRR  S   T    t    UUUU  V
R    SS  T    t          VVVV
      S  T
      S                    Y   y
  a                       YY   y
  a   bb   c   X     x     Y  yy
 aa  bb   ccc XXXX  xxxx   Y   y
aa  bb   cc    X      x    Y   y

     ZZ   $    4
zz    Z   $$$  4
 z    Z    $   444
 zzz  ZZ   $    4

""")


# Verify some expected facts about the number of free and fixed 5- and
# 6-ominoes.
assert len(Omino.BY_SIZE[6]) == 35
assert sum(len(o.aspects) for o in Omino.BY_SIZE[6].itervalues()) == 216
assert len(Omino.BY_SIZE[5]) == 12
assert sum(len(o.aspects) for o in Omino.BY_SIZE[5].itervalues()) == 63

__all__ = ("Omino", "cells_from_string")
