from proxy import HTTPProxy

p = HTTPProxy()

for i in xrange(10):
    print p.fetch("http://42.96.136.170:3000")
