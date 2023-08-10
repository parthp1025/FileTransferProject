#!/usr/bin/python

#Parth Patel

from socket import*
import sys
import hashlib
import time
import random
import csv
import datetime


response2 = ''
debug = 0

#detect if there are too much arguments
if (len(sys.argv) < 4):
    print ('Too few arguments, please try again')
    sys.exit()
#detect if there are the correct amount of arguments
if (len(sys.argv) < 6):
    if sys.argv[4] == '-d':
        debug = 1

    # '', signify server is listening locally
    serverName = ''
    serverPort = ''
    #detect if the port is an integer
    try:
        serverPort = int(str(sys.argv[2]))
    except ValueError:
        print 'Incorrect port.'
        sys.exit()

    #exit if port is out of range
    if ((serverPort < 1024) or (serverPort > 65536)):
        print 'Invalid port number, please try again.'
        sys.exit()

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverName, serverPort))
    print "The server is ready to receive"

    while 1:
        #message hold the contents recieved from the client
        #clientAddress contains the ip address of the client
        message = ''
        tries = 0
        retry = 1
        try:
            message, clientAddress = serverSocket.recvfrom(1024)
            if debug:
                print 'Receiving ACK "' +message+ '" from client.'
        #except timeout:
        except timeout:
            while ((retry) and (tries < 3)):
                try:
                    if debug:
                        print 'No response from client after 30 seconds'
                        print 'Resending ACK, retry #', tries
                    message, clientAddress = serverSocket.recvfrom(1024)
                    if debug:
                        print 'Receiving hash "' +message+ '" from client.'
                    retry = 0
                except timeout:
                    print 'No response from client after 15 seconds, moving on to next client'
                    retry = 1
                    tries = tries + 1

            if (tries == 3):
                if debug:
                    print 'No response from client after 15 seconds, moving on to next client'
        print 'ACK received: ' + message
        response = ''
        result = ''
        skip = 0
        #md5 returns a 64 character string
        if (message == 'ACK'):
            if debug:
                print 'Receiving authentication request "' + message +'" from client.'
            #start = time.time()
            #too many tabbing issues here, not supported to be inside "if debug"
            rand = str(random.randint(0,9)*17)+'something'
            challenge = str(hashlib.md5(rand).hexdigest())+str(hashlib.md5(rand+rand).hexdigest())
            #time.sleep(8)
            serverSocket.sendto(challenge, clientAddress)
            if debug:
                print 'Sending challenge string: ' + challenge

            tries = 0
            retry = 1
            serverSocket.settimeout(60)
            #ready = select.select([serverSocket],[],[], 30)
            #if (ready[0]):
            try:
                message, clientAddress = serverSocket.recvfrom(1024)
                if debug:
                    print 'Receiving hash "' +message+ '" from client.'
            #else:
            #except timeout:
            except timeout:
                while ((retry) and (tries < 3)):
#                    #if (not ready[0]):
                    try:
                        if debug:
                            print 'No response from client after 30 seconds'
                            print 'Resending challenge string, retry #', tries
                        #serverSocket.sendto(challenge, clientAddress)
                        message, clientAddress = serverSocket.recvfrom(1024)
                        if debug:
                            print 'Receiving hash "' +message+ '" from client.'
                        retry = 0
                    #else:
                    except timeout:
                        print 'No response from client after 15 seconds, moving on to next client'
                        retry = 1
                        tries = tries + 1

                if (tries == 3):
                    if debug:
                        print 'No response from client after 15 seconds, moving on to next client'
                    skip = 1
#                    continue
            #end = time.time()
            #elapsedTime = end-start
            #if debug:
            #   print "Time elapsed from creation of challenge string to receiving a response: " + str(end - start)

            #received message format: username + '.' + hash
#            try:
            print 'message recieved from client: ' + message
            dot = message.index('.')
            username = message[0:dot]
            hashed = message[dot+1:]
#            except ValueError:
#                print 'Wrong message format'
#                sys.exit()

            checkUser = 0
            pass1=''
            with open(sys.argv[4], 'rb') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if (row[0] == str(username)):
                        pass1 = row[1]
                        checkUser = 1

            #concat user, pass, mystery string for hashing
            result = username + pass1 + challenge
            result = hashlib.md5(result).hexdigest()
            response2 = username
            if result == hashed:
                response = 'Welcome to our service.'
            elif checkUser and (result <> hashed):
                response = 'Correct username, incorrect password.'
            else:
                response = 'User authorization failed.'
        else:
            if not skip:
                response = 'Authentication request from client not received.'
            if debug:
                print 'Authentication request from client not received.'

        #send the message to the client
        if not skip:
            serverSocket.sendto(response, clientAddress)
            if debug:
                print 'Sending response "' + response + '" to client.'

        tries = 0
        retry = 1
        data = 0
        try:
            data, clientAddress = serverSocket.recvfrom(1024)
            if debug:
                print 'Receiving hash "' +message+ '" from client.'
        #except timeout:
        except timeout:
            while ((retry) and (tries < 3)):
                try:
                    if debug:
                        print 'No response from client after 30 seconds'
                        print 'Resending data, retry #', tries
                    data, clientAddress = serverSocket.recvfrom(1024)
                    if debug:
                        print 'Receiving data' +data+ 'from client.'
                    retry = 0
                except timeout:
                    print 'No response from client after 15 seconds, moving on to next client'
                    retry = 1
                    tries = tries + 1

            if (tries == 3):
                if debug:
                    print 'No response from client after 15 seconds, moving on to next client'

        sensorMin = 10
        sensorAvg = 15
        sensorMax = 20
        allAvg = 25
        response2 = response2+' recorded: '+data+' '+(datetime.datetime.now().strftime('%B %d %H:%M:%S'))+' sensorMin: '+ str(sensorMin)+' sensorAvg: '+str(sensorAvg)+' sensorMax: '+str(sensorMax)+' allAvg: '+str(allAvg)
        serverSocket.sendto(response2, clientAddress)
else:
    print 'Missing port number, please try again.'
    sys.exit()




            
            
