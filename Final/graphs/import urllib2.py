import urllib

for i in range (0000,10000):
    filename = '%0*d' % (4, i)
    url = 'http://cs1.calstatela.edu/~jtran/graphs/%s' % filename
    urllib.urlretrieve (url, filename)
