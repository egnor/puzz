def combine(*pieces):
  """
  Return a generator that yields all possible sequences made by
  selecting one element from each member of 'pieces'.

  >>> list(combine("AB", "CD", "EFG"))
  ['ACE', 'ACF', 'ACG', 'ADE', 'ADF', 'ADG', 'BCE', 'BCF', 'BCG', 'BDE', 'BDF', 'BDG']

  >>> list(combine([1, 2], [3, 4]))
  [[1, 3], [1, 4], [2, 3], [2, 4]]
  """
    
  if not pieces:
    yield ()
  f = pieces[0]
  if len(pieces) == 1:
    for i, _ in enumerate(f):
      yield f[i:i+1]
  else:
    for i, _ in enumerate(f):
      for j in combine(*pieces[1:]):
        yield f[i:i+1] + j


def choose(items, k):
  """
  Return a generator that yields all 'k'-subsets of 'items'.  Elements
  of the yielded subsets are in the same order as in the original
  'items' sequence.

  >>> [i for i in choose("ABC", 2)]
  ['AB', 'AC', 'BC']

  >>> len(list(choose(list(range(10)), 6)))
  210
  """
  
  n = len(items)
  if n < k:
    raise ValueError("can't choose %d of %d items" % (k, n))
  if k == 0:
    yield items[:0]
  elif len(items) == k:
    yield items
  else:
    for i in choose(items[1:], k-1):
      yield items[:1] + i
    for i in choose(items[1:], k):
      yield i

if __name__ == "__main__":
  import doctest
  doctest.testmod()
