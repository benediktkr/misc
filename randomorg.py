import urllib2

def quota(ip):
    '''
    Returns the remaining quota for the given ip
    '''

    r = 'http://www.random.org/quota/?ip=%s&format=plain' % ip
    return int(urllib2.urlopen(r).read())

def random_int(emailaddr, num=1, base=10, min=0, max=100):
    '''
    Returns a lit of random numbers from the random.org API. Plays
    nice and follows their guidelines. Random.org returns HTTP503 on
    all errors.

    See http://www.random.org/clients/http/
    '''
    rorg = urllib2.build_opener()
    rorg.adheader = [('User-agent', emailaddr)]

    r = 'http://www.random.org/integers/?num=%d&min=%d&max=%d&col=1&base=%d&format=plain&rnd=new' % (num, min, max, base)
    
    n = [int(m.rstrip()) for m in rorg.open(r).readlines()]
        
    return n

if __name__ == '__main__':
    '''
    Example use.
    '''
    email = 'person@example.com'
    ipaddr = '0.0.0.0'
    try:
        print random_int(email, num=10)
    except urllib2.HTTPError as e:
        print e.code # Will be 503
    print 'Your quota: %s' % quota(ipaddr)
