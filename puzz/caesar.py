"""
Caesar shift (alphabetic rotation).
"""

def shift(s, n):
  """
  Caesar-shift a string by n (0 = no-op, 3 = classic Caesar, 13 = rot-13).
  Non-alphabetic characters are ignored.  Case is preserved.

  >>> shift("Hello World!", 1)
  'Ifmmp Xpsme!'

  >>> shift("irk", 13)
  'vex'

  >>> shift("IBM 9000", 25)
  'HAL 9000'
  """

  if not s:
    return s
  elif len(s) > 1:
    return "".join([shift(c, n) for c in s])
  elif not s.isalpha():
    return s
  elif s.isupper():
    return chr(65 + (ord(s) - 65 + n) % 26)
  else:
    return chr(97 + (ord(s) - 97 + n) % 26)


def all(s):
  """
  Return a list of all 26 Caesar-shifts of some text (including the original).

  >>> all("Vex")
  ['Vex', 'Wfy', 'Xgz', 'Yha', 'Zib', 'Ajc', 'Bkd', 'Cle', 'Dmf', 'Eng', 'Foh', 'Gpi', 'Hqj', 'Irk', 'Jsl', 'Ktm', 'Lun', 'Mvo', 'Nwp', 'Oxq', 'Pyr', 'Qzs', 'Rat', 'Sbu', 'Tcv', 'Udw']
  """

  return [shift(s, i) for i in range(26)]


if __name__ == "__main__":
  import doctest
  doctest.testmod()
