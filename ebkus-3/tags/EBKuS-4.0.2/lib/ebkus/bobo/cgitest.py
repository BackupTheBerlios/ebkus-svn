#!/usr/local/bin/python
# coding: latin-1

import sys
from ebapi import *
from templates import *

sys.path.append('../lib')


def cgitest(REQUEST):
    """BOBO PUBLISHED NUR SOLCHE FUNKTIONEN, DIE EINEN DOC STRING HABEN!!!"""
    res = []
    res.append(str(REQUEST))
    res.append('\n\n')
    import string
    return string.join(res)
    
    
    
def main():
    import cgi
    field_storage_form = cgi.FieldStorage()
    form = {}
    for k in field_storage_form.keys():
        form[k] = field_storage_form[k].value
        
    if not form:
        form = {'akid' : DEFAULT_AKTE}
        
    res = test(form)
    print "Content-type: text/plain\n\n" + res
    #  cgi.test()
    ##   print 
    
    ## <HTML>
    ## <HEAD><TITLE> (titel)s </TITLE></HEAD><BODY>
    
    ## <PRE>"""  + res + """ asdf </BODY></HTML> """
    
    
    
if __name__ == '__main__':
    main()
