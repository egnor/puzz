"""
Generation and inspection of the ways a sequence of items can be permuted.

TODO: Make these faster.
"""


def count(items):
  """
  Return the number of permutations of items (a count, or a sequence).

  >>> count(5)
  120

  >>> count([1,2,3,4,5])
  120

  >>> count("HELLO")
  120
  """

  if type(items) is not int:
    return count(len(items))
  elif items <= 0:
    return 1
  else:
    return items * count(items - 1)  # TODO: something better for big numbers?


def all(items):
  """
  Return a generator which yields permuted lists of the contents of a sequence.

  >>> [p for p in all([1,2,3])]
  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

  >>> [p for p in all("ZP")]
  [['Z', 'P'], ['P', 'Z']]
  """

  if not items:
    yield []
    return
  for i in range(len(items)):
    for l in all(items[:i] + items[i+1:]):
      yield [items[i]] + l


def list(items):
  """
  Convenience function to return a list of the permutations of a sequence:
  list(x) is the same as [p for p in all(x)].

  >>> list([1,2,3])
  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
  """
  return [p for p in all(items)]


def get(items, n):
  """
  Return the n-th permutation of a sequence.
  Equivalent to list(items)[n], but much faster.

  >>> get([1,2,3], 0)
  [1, 2, 3]

  >>> get([1,2,3], 1)
  [1, 3, 2]

  >>> [get("HELLO", i) for i in range(count(5))] == list("HELLO")
  True
  """

  if not items: return []
  c = count(len(items) - 1)
  i = n / c
  return [items[i]] + get(items[:i] + items[i+1:], n % c)


# TODO: Unique permutations (not swapping duplicates)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
