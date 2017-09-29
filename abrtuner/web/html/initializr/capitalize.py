from mod_python import apache

def outputfilter(filter):
  s = filter.read()
  while s:
    filter.write(s.upper())
    s = filter.read()

  if s is None:
    filter.close()

