#!/usr/local/bin/python
# coding: latin-1

#     Copyright
#
#       Copyright 1996 Digital Creations, L.C., 910 Princess Anne
#       Street, Suite 300, Fredericksburg, Virginia 22401 U.S.A. All
#       rights reserved.  Copyright in this software is owned by DCLC,
#       unless otherwise indicated. Permission to use, copy and
#       distribute this software is hereby granted, provided that the
#       above copyright notice appear in all copies and that both that
#       copyright notice and this permission notice appear. Note that
#       any product, process or technology described in this software
#       may be the subject of other Intellectual Property rights
#       reserved by Digital Creations, L.C. and are not licensed
#       hereunder.
#
#     Trademarks
#
#       Digital Creations & DCLC, are trademarks of Digital Creations, L.C..
#       All other trademarks are owned by their respective companies.
#
#     No Warranty
#
#       The software is provided "as is" without warranty of any kind,
#       either express or implied, including, but not limited to, the
#       implied warranties of merchantability, fitness for a particular
#       purpose, or non-infringement. This software could include
#       technical inaccuracies or typographical errors. Changes are
#       periodically made to the software; these changes will be
#       incorporated in new editions of the software. DCLC may make
#       improvements and/or changes in this software at any time
#       without notice.
#
#     Limitation Of Liability
#
#       In no event will DCLC be liable for direct, indirect, special,
#       incidental, economic, cover, or consequential damages arising
#       out of the use of or inability to use this software even if
#       advised of the possibility of such damages. Some states do not
#       allow the exclusion or limitation of implied warranties or
#       limitation of liability for incidental or consequential
#       damages, so the above limitation or exclusion may not apply to
#       you.
#
#
# Revision 1.2  1998/05/10 15:03:12  atms
# Juergs Aenderungen
#
# Revision 1.6  1997/01/20 13:58:22  brian
# The publisher component of pcgi now transparently supports threads if they are
# available on the target platform, doing all I/O in separate threads if possible.
# This should let the publisher achieve higher performance in some cases, since
# the application only actually blocks for the duration of the python application
# call rather than blocking until a pcgi-wrapper has finished reading the results
# of a call.
#
# Revision 1.1  1996/12/12 17:12:43  brian
# Added a new version of pcgi_publisher to the CVS project that detects whether threads are available, and if so handles connection IO in a separate thread. Preliminary testing shows it to be quite stable, but lacking the time to do more testing at the moment I decided it would be safer to add the new version as threaded_pcgi_publisher.py for now.
#

import sys, os, socket
from string import atoi, find, joinfields, splitfields, join
from ebkus.config import config
import time
import logging

try:    from cStringIO import StringIO
except: from StringIO import StringIO


publish = None
mustdie = 0


def exit(n):
    logging.critical("Fataler Fehler", exc_info=True)
    logging.shutdown()
    sys.exit(n)

def handle_request(modname, conn):
    global mustdie
    sbuffer=[]
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        sbuffer.append(data)
    buffer = joinfields(sbuffer, '')
    if buffer.startswith('XX6859236XX'):
        if buffer.startswith('XX6859236XXquit'):
            logging.info("Shutdown durch stop.py")
            logging.shutdown()
            sys.exit(0)
        elif buffer.startswith('XX6859236XXstatus'):
            conn.send('Ok')
            conn.close()
            return
    # Parse our pcgi protocol
    elen        = atoi(buffer[:9])
    environment = buffer[9:(elen + 9)]
    input       = buffer[(elen + 18):]
    # Rebuild the env and stdin
    env = {}
    ev = splitfields(environment, '\000')
    for x in ev:
        ox = find(x, '=')
        if x[(ox+1):] and (x[(ox+1):] != ': '):
            env[x[0:ox]] = x[(ox+1):]
    sin, sout, serr = StringIO(input), StringIO(), StringIO()
    envstr = '\n'.join(["%s=%s" % (e[0],e[1]) for e in env.items()])
    logging.info("BEGIN REQUEST (REQUEST_URI: %s)", env['REQUEST_URI'])
    logging.debug("Environment:\n%s>>>>\n%s\n<<<<%s", '-'*50, envstr, '-'*50)
    if input:
        logging.debug("Input:\n%s>>>>\n%s\n<<<<%s", '-'*50, input, '-'*50)
    clock = time.time
    t1=clock()
    # publish ist globale Variable, die unten in main() gesetzt wird:
    # publish = ebkus.bobo.cgi_module_publisher.publish_module
    try:
        publish(modname, stdin=sin, stdout=sout, stderr=serr, environ=env)
    except:
        mustdie=1
    t2=clock()
    ms = (1000*(t2-t1))
    output, error = sout.getvalue(), serr.getvalue()
    conn.send('%9d%s%9d%s' % (len(output), output, len(error), error))
    conn.close()
    i = output.find('Status: ') + 8
    status = output[i:i+3]
    logging.debug("Output:\n%s>>>>\n%s\n<<<<%s", '-'*50, output, '-'*50)
    if error:
        logging.debug("Error:\n%s>>>>\n%s\n<<<<%s", '-'*50, error, '-'*50)
    logging.info("END REQUEST (Status: %s, %2.2f ms)", status, ms)
    if mustdie:
        exit(1)
        

# Server main loop        
def main(module_name):
  # Should know enough now to import the publisher...
    global publish
    import ebkus.bobo.cgi_module_publisher
    import ebkus.app.EBKuS
    publish = ebkus.bobo.cgi_module_publisher.publish_module
    # Create a listening socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((config.HOST, int(config.PORT)))
        sock.listen(5)
    except socket.error, e:
        t = sys.exc_info()[0]
        logging.exception("Socketfehler: %s %s", t, e)
        exit(1)
    #logging.info("Publishing module: %s", module_name)
    host, port = sock.getsockname()
    logging.info('Warte auf Anfragen: EBKuS - %s  (host: %s port: %s)',
                 config.INSTANCE_NAME, host, port)
    request_count = 0
    while 1:
        try:
            connection, addr = sock.accept()
            logging.debug("Connection accepted (addr: %s)", addr)
            handle_request(module_name, connection)
            request_count += 1
            if request_count % 100 == 0:
                ebkus.app.EBKuS.clean_up()
        except socket.error, args:
            if mustdie:
                exit(1)
        except KeyboardInterrupt:
            logging.info("Shutdown mit Str-C")
            sys.exit(0)
        except SystemExit, v:
            # kann aus handle_request() kommen
            v = v[0]
            if v == 0:
                sys.exit(0)
            else:
                exit(v)
        except:
            # Fatal
            exit(1)
            
            
            
            
            
            
            
