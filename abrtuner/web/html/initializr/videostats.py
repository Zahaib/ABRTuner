from mod_python import apache

def inputfilter(filter):
  s = filter.read()
  stats = ""
  while s:
    #filter.write(s.upper())
    stats = stats + str(s)
    s = filter.read()
  outfile = open("/home/zahaib/stats.txt", "w")
  outfile.write("%s" % str(stats))
  outfile.close()

  if s is None:
    filter.close()
