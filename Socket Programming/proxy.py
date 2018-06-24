import SocketServer
import SimpleHTTPServer
import socket

PORT = 12345
cache_dict = {}
cache_arr = []
cache_len = 3

class HTTPCacheRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
        if self.command != "POST":
            global cache_arr, cache_dict
            filename = self.path.strip("/")
            fnm = filename.split('/')
            # Get filename and port
            act_fnm = ""
            for_port = ""
            for i in fnm:
            	if "localhost" in i:
            		for_port = i;
                if "http" not in i and i and "localhost" not in i:
                    act_fnm += i
                    act_fnm += "/"
            filename = act_fnm.strip("/")
            for_port = for_port.split(':')
            if(len(for_port)==1):
                for_port.append('20000')
            '''
            Get the method, headers and version of the request.
            '''
            method = self.command
            hdrs = str(self.headers)
            hdrs = hdrs.replace('12345',for_port[1])
            ver = self.request_version
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
            	'''
            	Make a HEAD request and
            	check the header.
            	''' 
                ss.connect(("",int(for_port[1])))
                print "Connection Established"
                get_msg = str(method) + " /" + str(filename) + " " + str(ver) + "\r\n" + str(hdrs) + "\r\n"
                head_msg = get_msg.replace('GET','HEAD')
                ss.send(head_msg)
                head_response = ""
                data = 123
                while data:
                    data = ss.recv(1024)
                    head_response += data
            except:
            	print "Not able to establish connection"
            ss.close()
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
            	'''
            	Make a GET request and
            	check the body.
            	'''
                ss.connect(("",int(for_port[1])))
                if filename in cache_arr and "304 Not Modified" in head_response:
                    print "File in cache already upto date"
                elif "404" in head_response:
                	print "404-->Not adding in cache"
                elif "304 Not Modified" not in head_response or filename not in cache_arr:
                    ss.send(get_msg)
                    get_response = ""
                    data = 123
                    while data:
                        data = ss.recv(1024)
                        get_response += data
                    temp_arr = []
                    temp_arr.append(filename)
                    '''
                    Update the cache_arr and cache_dict
                    according to the LRU algorithm.
                    '''
                    for i in range(len(cache_arr)):
                        if(cache_arr[i] != filename):
                            temp_arr.append(cache_arr[i])
                    cache_arr = temp_arr
                    if(len(cache_arr) > 3):
                        popped_file = cache_arr.pop()
                        cache_dict[popped_file] = None
                    cache_dict[filename] = get_response
                self.wfile.write(cache_dict[filename])
            except:
            	print "Not able to connect"
            ss.close()

s = SocketServer.ThreadingTCPServer(("", PORT), HTTPCacheRequestHandler)
s.allow_reuse_address = True
print "Serving on port", PORT
s.serve_forever()