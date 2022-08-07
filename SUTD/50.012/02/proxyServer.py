# # 50.012 Networks Lab 2 code skeleton
# Based on old code from Kurose & Ross: Computer Networks
# Streamlined, threaded, ported to HTTP/1.1
from socket import *
from thread import *
import sys,os

BUFFER_SIZE = 4096
PROXY_PORT = 8080

def clientthread(tcpCliSock):
    message = tcpCliSock.recv(BUFFER_SIZE)
    print message    
    # Extract the parameters from the given message
    # we need to fill "host": the host name in the request
    # we need to fill "resource": the resource requested on the target system
    # we need to fill "filetouse": an escaped valid path to the cache file. could be hash value as well
    host = None
    resource = None
    import re
    m = re.search(r'GET https*://([^/]*)(.*) HTTP/1.1',message)
    if m:
        print "host from first line: "+m.group(1)
        print "resource from first line: "+m.group(2)
        host=m.group(1)
        resource=m.group(2)
    # Extract Host
    m = re.search(r'Host: ([\S]*)\n',message)
    if m:
        print "host from Host:"+m.group(1)
        host=m.group(1)
    if host==None or resource==None:
        print "ERROR: no host found"
        return
    # Extract Accept
    accept=""
    m = re.search(r'Accept: ([\S]*)\n',message)
    if m:
        print "accept: "+m.group(1)
        accept=m.group(1)

    # lets not do connection-alive
    message=message.replace("Connection: keep-alive","Connection: close")
    # generate our cache file name
    import hashlib
    m = hashlib.md5()
    m.update(host+resource)
    filetouse=m.hexdigest()
    fileExist = False

    print "Host: "+host
    print "Resource: "+resource
    try:
        # Check wether the file exist in the cache
        f = open(filetouse, "r")                      
        outputdata = f.readlines()                        
        fileExist = True
        f.close()
        # send out the cached file content here
        for i in outputdata:
            tcpCliSock.send(i)
        tcpCliSock.close()
        print 'Read from cache'     
	# Error handling for file not found in cache
    except IOError:
        if fileExist == False:
            c = socket(AF_INET, SOCK_STREAM) # Create a new client socket here
            c.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
            os.environ['http_proxy']=''
            
            print 'host is ' + host + " resource is" + resource
            try:
                # Connect to the socket to port 80
                c.connect((host, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile()
                fileobj.write("GET "+ resource + " HTTP/1.1\r\n")
                fileobj.write("Host: "+host+"\r\n")                
                if accept:
                    fileobj.write("Accept: "+accept+"\r\n")
                fileobj.write("Connection: close\r\n")
                fileobj.write("\r\n")
                fileobj.flush()
                # Read the response into buffer
                outputdata = fileobj.readlines()
                fileobj.close()
                c.close()
                # Create a new file in the cache for the requested file. 
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                print "received response, saving in "+filetouse
                tmpFile = open("./" + filetouse,"wb")  
                # save returned data into cache file
                for i in outputdata:
                    tmpFile.write(i)
                tmpFile.close()
                # also send returned data to original client
                for i in outputdata:
                    tcpCliSock.send(i)
                
            except gaierror as e:
                print e
            except:
                print "Illegal request"+str(sys.exc_info()[0])
        else:
            # HTTP response message for file not found
            tcpCliSock.send("404 Not Found\n")
    # Close the client and the server sockets    
    tcpCliSock.close()


    
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('localhost', PROXY_PORT))
tcpSerSock.listen(1)
while 1:
    # Start receiving data from the client
    print 'Ready to serve...'
    tcpCliSock, addr = tcpSerSock.accept()
    print 'Received a connection from:', addr
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(tcpCliSock,))
    #clientthread(tcpCliSock)
    
