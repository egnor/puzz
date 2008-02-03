def all(str):
  for i in range(len(str)):
    yield str[0:i] + str[i] + str[i+1:]
