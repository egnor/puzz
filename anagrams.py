by_sorted = {}

def init(wordlist=None):
  if wordlist is None:
    from . import words
    wordlist = words.all

  print("constructing anagram index for %d words..." % (len(wordlist),))
  for i in wordlist:
    s = "".join(sorted(i))
    by_sorted.setdefault(s, []).append(i)


def is_subset_sorted(big, small):
  """Returns true iff small is a subset of big.  Both arguments must
  be sorted sequences of letters.

  >>> is_subset_sorted("abcde", "ace")
  True
  
  >>> is_subset_sorted("abcccde", "acce")
  True
  
  >>> is_subset_sorted("abcccd", "cce")
  False
  
  >>> is_subset_sorted("abcccd", "abcd")
  True
  """

  if len(small) > len(big): return False
  b_iter = iter(big)
  for s in small:
    try:
      b = next(b_iter)
      while b < s:
        b = next(b_iter)
      if s != b:
        return False
    except StopIteration:
      return False
  return True

def sort(w):
  return "".join(sorted(w))

def candidates(letters):
  letters = sort(letters)
  out = []
  for k, v in by_sorted.items():
    if is_subset_sorted(letters, k):
      for i in v:
        out.append((len(i), i))
  out.sort()
  out.reverse()
  return [i[1] for i in out]

if __name__ == "__main__":
  init(())
  import doctest
  doctest.testmod()
else:
  init()
