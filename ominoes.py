import collections

class Omino(collections.namedtuple('Omino',
    ['name', 'size', 'cells', 'symmetries'])):
  """
  Omino instances represent polyominoes (pentominoes, hexominoes, etc).
  The omino is described at a certain arbitrary orientation and position.
  Ominoes are typically retrieved from global values in this module
  (eg. pentominoes), not created directly by the caller.

  Attributes:
    name: Common name of this polyomino (e.g. 'R').
    size: 2-tuple (x_size, y_size) bounding the polyomino cells.
    cells: Set of (x, y) coordinates of cells in the polyomino.
    symmetries: Set of symmetries, out of '|', '-', '+', '/', '\', '@'.
  """

  # TODO: Add doctest examples.

  # TODO: Add ability to transform (reflect, rotate) and track transformations.

  # TODO: Add aliases in addition to primary name, for different schemes?

  def __new__(cls, name, *lines):
    lines = [[not ch.isspace() for ch in line] for line in lines]
    cells = set([
      (x, y)
      for y, line in enumerate(lines)
      for x, cell in enumerate(line)
      if cell])

    xs = max([len(line) for line in lines])
    ys = len(lines)
    sym = set()
    if cells == set([(xs - 1 - x, y) for x, y in cells]): sym.add('|')
    if cells == set([(x, ys - 1 - y) for x, y in cells]): sym.add('-')
    if cells == set([(xs - 1 - x, ys - 1 - y) for x, y in cells]): sym.add('+')
    if cells == set([(y, x) for x, y in cells]): sym.add('\\')
    if cells == set([(ys - 1 - y, xs - 1 - x) for x, y in cells]): sym.add('/')
    if cells == set([(ys - 1 - y, x) for x, y in cells]): sym.add('@')
    return super(cls, Omino).__new__(
        cls, name=name, size=(xs, ys), cells=cells,
        symmetries=sym)

  def __len__(self):
    """Returns the degree of the polyomino (5 for a pentomino, etc)."""
    return len(self.cells)

  def __repr__(self):
    """Returns text identifying the polyomino's degree and name."""
    return '<%d-omino "%s">' % (len(self), self.name)

  def __str__(self):
    """Returns a multiline ASCII art picture of the polyomino."""
    xs, ys = self.size
    return '\n'.join([
        ''.join([' #'[(x, y) in self.cells] for x in range(xs)])
        for y in range(ys)])


monomino = Omino('Monomino', '#')

domino = Omino('Domino', '#', '#')

# Names from: https://en.wikipedia.org/wiki/Tromino
trominoes = [
  Omino('I', '#', '#', '#'),
  Omino('L', '#', '##'),
]

# Names from: https://en.wikipedia.org/wiki/Tetromino
tetrominoes = [
  Omino('I', '#', '#', '#', '#'),
  Omino('L', '#', '#', '##'),
  Omino('O', '##', '##'),
  Omino('T', '###', ' #'),
  Omino('Z', '##', ' ##'),
]

# Names from: https://en.wikipedia.org/wiki/Pentomino
# Using standard names, *not* Conway's notation.
pentominoes = [
  Omino('F', ' ##', '##', ' #'),
  Omino('I', '#', '#', '#', '#', '#'),
  Omino('L', '#', '#', '#', '##'),
  Omino('N', ' #', ' #', '##', '#'),
  Omino('P', '##', '##', '#'),
  Omino('T', '###', ' #', ' #'),
  Omino('U', '# #', '###'),
  Omino('V', '#', '#', '###'),
  Omino('W', '#', '##', ' ##'),
  Omino('Y', ' #', '##', ' #', ' #'),
  Omino('Z', '##', ' #', ' ##'),
]

# Names from: http://www.gamepuzzles.com/sxnames.htm
# Note that their 'Short S' is just a flip of 'Short N' (so not included).
# See also: http://puzzler.sf.net/docs/polyominoes-intro.html#hexominoes
hexominoes = [
  Omino('A', '###', '##', '#'),
  Omino('C', '##', '#', '#', '##'),
  Omino('D', '#', '##', '##', '#'),
  Omino('E', ' ##', '##', ' ##'),
  Omino('High F', ' ##', '##', ' #', ' #'),
  Omino('Low F', ' ##', ' #', '##', ' #'),
  Omino('G', '##', '#', '##', ' #'),
  Omino('H', '#', '###', '# #'),
  Omino('I', '#', '#', '#', '#', '#', '#'),
  Omino('J', '  #', '# #', '###'),
  Omino('K', '##', '###', ' #'),
  Omino('L', '#', '#', '#', '#', '##'),
  Omino('M', ' ##', ' #', '##', '#'),
  Omino('Long N', ' #', '##', '#', '#', '#'),
  Omino('Short N', ' #', '##', '##', '#'),
  Omino('O', '##', '##', '##'),
  Omino('P', '##', '##', '#', '#'),
  Omino('Q', '##', '##', ' ##'),
  Omino('R', '##', '###', '#'),
  Omino('Long S', '#', '#', '##', ' #', ' #'),
  Omino('Tall T', '###', ' #', ' #', ' #'),
  Omino('Short T', '####', ' #', ' #'),
  Omino('U', '# #', '####'),
  Omino('V', '#', '#', '####'),
  Omino('Wa', '#', '##', ' ###'),
  Omino('Wb', '#', '##', ' ##', '  #'),
  Omino('Wc', '#', '##', ' ##', ' #'),
  Omino('X', ' #', '####', ' #'),
  Omino('Italic X', ' #', '##', ' ##', ' #'),
  Omino('High Y', ' #', '##', ' #', ' #', ' #'),
  Omino('Low Y', ' #', ' #', '##', ' #', ' #'),
  Omino('Short Z', '##', ' #', ' ###'),
  Omino('Tall Z', '##', ' #', ' #', ' ##'),
  Omino('High 4', '#', '###', ' #', ' #'),
  Omino('Low 4', '#', '#', '###', ' #'),
]

all = [monomino, domino] + trominoes + tetrominoes + pentominoes + hexominoes

by_size_name = {(len(omino), omino.name): omino for omino in all}
