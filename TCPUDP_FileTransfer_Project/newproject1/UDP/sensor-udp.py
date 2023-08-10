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
addrRegEx = re.compile('([0-9]{1,3})[\.]([0-9]{1,3})[\.]([0-9]{1,3})[\.]([0-9]{1,3})[:]([0-9]{1,5})')
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
    if (sys.argv[3] == '-p'):
        try:
            serverPort = int(str(sys.argv[4]))
            print ('port: ' + str(serverPort))
        except ValueError:
            print ('Incorrect port.')
            sys.exit()

        # check if the port number is valid
        if ((serverPort < 1024) or (serverPort > 65536)):
            print ('Invalid port number, please try again.')
            sys.exit()

    if (sys.argv[1] == '-s'):
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

# -------- udp section -----------

    tries = 0
    #create a socket for UDP
    clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
    print 'created'
    if hostNameDetect:
        try:
            if debug:
                print 'Hostname: ' + serverName
            serverName = socket.gethostbyname(serverName)
            if debug:
                print 'Host name converted to IP address: ' + serverName
        except socket.gaierror, err:
            print 'Cant resolve hostname' + serverName + ''

    #send the message to the server
    clientSocket.settimeout(15)
    
    print 'Sending authentication request to server <' + serverName + '> <' + str(serverPort) + '>'
    clientSocket.sendto('ACK', (serverName, serverPort))
    print 'sent ACK'
    
    
    tries = 0
    retry = 1
    try:
        #result will contain message from server
        #serverAddress will contain server ip addres
        result, serverAddress = clientSocket.recvfrom(1024)
        #print 'Receiving mystery string: ', result
        if debug:
            print 'Receiving mystery string: ', result
    except socket.timeout:
        while ((retry) and (tries < 3)):
            try:
                if debug:
                    print 'Failed to receive anything within 5 seconds'
                    print 'Retry receiving authentication message, try #', tries
                result, serverAddress = clientSocket.recvfrom(1024)
                tries = tries + 1;
                if debug:
                    print 'Receiving hash "' +message+ '" from client.'
                retry = 0
            except socket.timeout:
                retry = 1
                tries = tries + 1

        if (tries == 3):
            if debug:
                print 'No response from client after 15 seconds, closing connection.'
            clientSocket.close()
            sys.exit()


    tries = 0
    retry = 1
    #concat user, pass, mystery string for hashing
    message = sys.argv[6] + sys.argv[8] + result 
    #format: username + username length + hashed value
    message = sys.argv[6] + '.' + hashlib.md5(message).hexdigest()  

    if debug:
        print 'Sending username.hash: ', message
    clientSocket.sendto(message, (serverName, serverPort))

    tries = 0;  
    try:
        result, serverAddress = clientSocket.recvfrom(1024)
        if debug:
            print 'Receiving response from server.'
        
    except socket.timeout:
        while ((retry) and (tries < 3)):
            try:
                if debug:
                    print 'Failed to receive anything within 5 seconds'
                    print 'Retry receiving message from server, try #', tries
                result, serverAddress = clientSocket.recvfrom(1024)
                tries = tries + 1;
                if debug:
                    print 'Receiving response.'
                retry = 0
            except socket.timeout:
                retry = 1
                tries = tries + 1

        if (tries == 3):
            if debug:
                print 'No response from client after 15 seconds, closing connection.'
            clientSocket.close()
            sys.exit()

    print 'From server:', result

    clientSocket.sendto(sys.argv[10], (serverName, serverPort))

    result2 = 0
    tries = 0
    retry = 1
    try:
        result2, clientAddress = clientSocket.recvfrom(1024)
        if debug:
            print 'Receiving hash "' +message+ '" from client.'
    #except timeout:
    except timeout:
        while ((retry) and (tries < 3)):
            try:
                if debug:
                    print 'No response from client after 30 seconds'
                    print 'Resending data, retry #', tries
                result2, clientAddress = serverSocket.recvfrom(1024)
                if debug:
                    print 'Receiving data ' +result2+ ' from client.'
                retry = 0
            except timeout:
                print 'No response from client after 15 seconds, moving on to next client'
                retry = 1
                tries = tries + 1

        if (tries == 3):
            if debug:
                print 'No response from client after 15 seconds, moving on to next client'

    print 'From server: ', result2

    #close socket connection so that we dont crash the server
    clientSocket.close()

else:
    print 'Incorrect arguments, please try again.'
    sys.exit()

