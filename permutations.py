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
  ['ZP', 'PZ']
  """

  if len(items) <= 1:
    yield items
    return
  for i in range(len(items)):
    for l in all(items[:i] + items[i+1:]):
      yield items[i:i+1] + l


def unique(items):
  """
  Return a generator which yields unique permutations of a sequence
  (even if the input has duplicates).

  >>> [p for p in unique((1,2,1))]
  [(1, 2, 1), (1, 1, 2), (2, 1, 1)]

  >>> set(unique("BANANA")) == set(all("BANANA"))
  True

  >>> len([p for p in unique("BANANA")]) * 12 == len([p for p in all("BANANA")])
  True
  """

  if len(items) <= 1:
    yield items
    return
  used = set()
  for i in range(len(items)):
    if items[i] not in used:
      for l in unique(items[:i] + items[i+1:]):
        yield items[i:i+1] + l
      used.add(items[i])


def get(items, n):
  """
  Return the n-th permutation of a sequence.
  Equivalent to list(all(items))[n], but much faster.

  >>> get([1,2,3], 0)
  [1, 2, 3]

  >>> get([1,2,3], 1)
  [1, 3, 2]

  >>> [get("HELLO", i) for i in range(count(5))] == list(all("HELLO"))
  True
  """

  if not items: return items[:0]
  c = count(len(items) - 1)
  i = n / c
  return items[i:i+1] + get(items[:i] + items[i+1:], n % c)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
