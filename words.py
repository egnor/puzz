import os
import re
import sys


class Word(str):
  """
  Word is a subclass of string that normalizes the string used to
  create it (remove all nonletter, nondigit characters and
  lowercase).  Several other properties are attached:

    sources - a list of ["source/filename.txt"] containing the word
    original - the original, un-normalized form
    frequency - numeric frequency, if known
    phonemes - pronunciation, if known; see data/mobypron.readme; [/',] removed

  >>> x = Word("Dr. Awkward")
  >>> x
  'drawkward'

  >>> x.original
  'Dr. Awkward'

  >>> isinstance(x, str)
  True
  """

  remove = re.compile("[^a-z0-9A-Z]+")

  def __new__(cls, original):
    obj = str.__new__(cls, cls.normalize(original))
    obj.__dict__["original"] = original
    obj.__dict__["sources"] = []
    obj.__dict__["frequency"] = 0
    obj.__dict__["phonemes"] = ""
    return obj

  @classmethod
  def normalize(cls, s):
    n = cls.remove.sub("", s.lower())
    if n == s:
      return s
    else:
      return n


def of_length(n):
  """
  Return a generator yielding all words of length 'n' (from the global
  dictionary loaded by this module.
  """
  for w in all:
    if len(w) == n:
      yield w


def with_letters(*lettersets):
  """
  Return a generator yielding all words that can be constructed by
  choosing one letter out of each set in 'lettersets'.
  """

  matcher = re.compile("".join(["[%s]" % "".join(s) for s in lettersets]) + "$")
  return [w for w in all if re.match(matcher, w)]


def remove_substrings(words):
  by_length = [(len(i), i) for i in words]
  by_length.sort()
  out = set()
  for l, w in by_length:
    for i in range(0, l+1):
      for j in range(i+1, l+1):
        out.discard(w[i:j])
    out.add(w)
  return list(out)


all = []
lookup = {}
"""
Dictionaries are loaded into 'all' and 'lookup', which contain the same
Word instances as a list and a dict, respectively.
"""


def add(word_str, source):
  """
  Adds a word to the global dictionary, if not already present.
  Returns the Word object, and appends the given source, either way.
  """
  new_word = Word(word_str)
  old_word = lookup.setdefault(new_word, new_word)
  if old_word is new_word: all.append(new_word)
  old_word.sources.append(source)
  return old_word


def load_text(filename):
  """
  Loads a simple word list containing one word per line.
  Empty lines are skipped, as are lines starting with "#" or ";".
  """
  for line in open(filename):
    line = line.strip()
    if line and line[0] != "#" and line[0] != ";":
      add(line, filename)


def load_mobypron(filename):
  """
  Loads the Moby Pronunciator data set, containing phonemic data.
  """
  for line in open(filename):
    word, pron = line.strip().split(None, 1)
    word = word.replace("_", " ")
    pron = pron.translate(None, "[/',] ")
    add(word, filename).phonemes = pron


def load_nutrimatic(filename):
  """
  Loads a Nutrimatic-format word list with words and frequencies.
  """
  for line in open(filename):
    freq, word = line.split()
    add(word, filename).frequency = int(freq)


def reload_default(data_dir=None):
  """
  Clears the global word set and loads the default set of dictionaries.
  If 'data_dir' is not given, $DICTIONARIES is checked, or by default
  a path relative to the script's source is used.
  """
  if not data_dir:
    data_dir = os.getenv("DICTIONARIES")
    if not data_dir:
      import inspect
      data_dir, _ = os.path.split(inspect.getsourcefile(lambda: None))
      data_dir = os.path.join(data_dir, "data")

  lookup.clear()
  for file, loader in [
      ("american.txt", load_text),
      ("mobypron.txt", load_mobypron),
      ("nutrimatic-100K.txt", load_nutrimatic),
      ("propernames.txt", load_text),
      ("words.txt", load_text),
    ]:
    path = os.path.join(data_dir, file)
    if os.path.exists(path):
      print >>sys.stderr, ">> Loading %s..." % path
      loader(path)

  print >>sys.stderr, ">> Dictionaries loaded."


def get_terminal_width():
  try:
    import curses
    try:
      curses.setupterm()
      return curses.tigetnum("cols")
    except curses.error:
      pass
  except ImportError:
    pass
  return 80


def print_compact_list(words, width=None, out=sys.stdout):
  if width is None:
    width = get_terminal_width()

  maxwidth = max(len(i) for i in words)
  cols = width / (maxwidth+2)
  if cols < 1: cols = 1
  rows = (len(words)+cols-1) / cols
  fmt = "  %%-%ds" % (maxwidth,)
  for i in range(0, rows):
    print >> out, "".join(fmt % j for j in words[i::rows])


if __name__ == "__main__":
  import doctest
  doctest.testmod()
else:
  reload_default()
