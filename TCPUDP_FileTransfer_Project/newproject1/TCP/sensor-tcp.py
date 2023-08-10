

#!/usr/bin/python

#Parth Patel

from socket import*
import socket
import sys
import re
import hashlib
import csv


serverPort = ''
serverName = ''
debug = 0
hostNameDetect = 0
dot1 = 0
dot2 = 0
dot3 = 0

#regular expression for error checking
addrRegEx = re.compile('([0-9]{1,3})[.]([0-9]{1,3})[.]([0-9]{1,3})[.]([0-9]{1,3})[:]([0-9]{1,5})')
ipRegEx = re.compile('([0-9]{1,3})[\.]([0-9]{1,3})[\.]([0-9]{1,3})[\.]([0-9]{1,3})')
hostRegEx = re.compile('((\.?(\w+))+(.com|.org|.edu))|(localhost)[:]([0-9]{1,3})')
hostRegEx2 = re.compile('((\.?(\w+))+(.com|.org|.edu))|(localhost)')

#determine if the argument format is correct
if ((len(sys.argv) == 11) or (len(sys.argv) == 12)):
    if (len(sys.argv) == 12):
        if (sys.argv[11] == '-d'):
            debug = 1
            print ('debug on')
   

    #convert port into an int
    if  (sys.argv[3] == '-p'):
        try:
            serverPort = int(str(sys.argv[4]))
            print ('port: ' + str(serverPort))
        except ValueError:
            print ('Incorrect port.')
            sys.exit()

        #cond = 0
    
        # check if the port number is valid
        if ((serverPort < 1024) or (serverPort > 65536)):
            print ('Invalid port number, please try again.')
            sys.exit()

#---------------------------------------------> need to fix regex
    ##elif (ipRegEx.match(sys.argv[1]) or hostRegEx2.match(sys.argv[1])):
    if  (sys.argv[1] == '-s'):
        serverName = sys.argv[2]                
        if (not hostRegEx2.match(sys.argv[2])):
            try:
                dot1 = serverName.index('.')
                dot2 = serverName.index('.', dot1+1)
                dot3 = serverName.index('.', dot2+1)
            except ValueError:
                print ('Invalid ip address, please try again.')
                sys.exit()

            #check each set of number if they are a byte or less
            if ((int(serverName[0:dot1]) > 255) 
                or (int(serverName[dot1+1:dot2]) > 255) 
                or (int(serverName[dot2+1:dot3]) > 255) 
                or (int(serverName[dot3+1:]) > 255)):
                print ('Invalid ip address, please try again.')
                sys.exit()
        else:
            hostNameDetect = 1
    print ('serverName: '+serverName)
    # if port number is not given, assign this as the port
    #serverPort = 52345
    #print ('Port number not present, using default port # 52345')
        
    ##else:
      ##  print ('The ip and/or port number is invalid, please try again.')
        ##sys.exit()
             
    print ('host name found?')
    print (hostNameDetect)
# ------------- tcp -----------------

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    if hostNameDetect:
        try:
            if debug:
                print ('Hostname: ' + serverName)
            serverName = socket.gethostbyname(serverName)
            if debug:
                print ('Host name converted to IP address: ' + serverName)
        except (socket.gaierror, err):
            print ('Cant resolve hostname' + serverName + '')
    
    print ('socket creation passed')    
    clientSocket.connect((serverName, serverPort))
    if debug:
        print ('Sending authentication request to server <' + serverName + '> <') + str(serverPort) + '>'
    clientSocket.send('ACK')
    
    random = clientSocket.recv(1024)
    if debug:
        print ('Receiving mystery string: ', random)

    #concat user, pass, mystery string for hashing
    message = (sys.argv[6] + sys.argv[8] + random)
    #format: username + username length + hashed value
    message = sys.argv[6] + '.' + hashlib.md5(message).hexdigest()  

    if debug:
        print ('Sending username.hash: ', message)
    clientSocket.send(message)
    if debug:
        print ('Receiving response from server.')
    result = clientSocket.recv(1024)
    print ('From server: ', result)

    clientSocket.send(sys.argv[10])    

    result2 = clientSocket.recv(1024)
    print ('Sensor: ', result2)
    clientSocket.close()

else:
    print ('Incorrect arguments, please try again.')
    sys.exit()

