__author__ = 'dleece'

import random, string

def genString(intarg):
    # Each view needs an authoritiative zone to resolve the cname. Although the view could be reused per view
    # generating random makes it very difficult for anyone to guess the name and potentially probe for zone contents.
    randstring = ''.join(random.choice(string.ascii_lowercase) for _ in range(intarg))
    return  randstring