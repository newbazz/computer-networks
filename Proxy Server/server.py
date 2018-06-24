import os
import time
import SocketServer
import SimpleHTTPServer

PORT = 20000

class HTTPCacheRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
        if self.command != "POST" and self.headers.get('If-Modified-Since', None):
            print "Oh yes"
            filename = self.path.strip("/")
            if os.path.isfile(filename):
                x=time.ctime(os.path.getmtime(filename)) + " GMT"
                print x
                a = time.strptime(x, "%a %b %d %H:%M:%S %Y %Z")
                print "\n\nA\n\n"
                print a
                print "\n\n"+self.headers.get('If-Modified-Since', None)+"\n\n"
                print "\n\n\n"
                b = time.strptime(self.headers.get('If-Modified-Since', None), "%a, %d %b %Y %H:%M:%S %Z")
                print "\n\nB\n\n"
                print b
                if a <= b:
                    print "Here"
                    self.send_response(304)
                    self.end_headers()
                    return None
        else:
            print "Oh no Here!\n\n\n"
        return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

    def end_headers(self):
        filename = self.path.strip("/")
        if filename == "2.binary":
            self.send_header('Cache-control', 'no-cache')
        else:
            self.send_header('Cache-control', 'must-revalidate')
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

s = SocketServer.ThreadingTCPServer(("", PORT), HTTPCacheRequestHandler)
s.allow_reuse_address = True
print "Serving on port", PORT
s.serve_forever()