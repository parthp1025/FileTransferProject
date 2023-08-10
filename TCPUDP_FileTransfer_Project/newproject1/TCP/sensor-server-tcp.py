

#!/usr/bin/python

#Parth Patel

from socket import*
import sys
import hashlib
import csv
import random
import datetime



response2 = ''
debug = 0

#detect if there are too much arguments
for i in range(len(sys.argv)):
    print (sys.argv[i])
if (len(sys.argv) < 4):
    print ('Too few arguments, please try again')
    sys.exit()
#detect if there are the correct amount of arguments
if (len(sys.argv) < 6):
    if sys.argv[4] == '-d':
        debug = 0


    serverName = ''
    serverPort = ''

        #detect if the port is an integer
    try:
        serverPort = int(str(sys.argv[2]))
    except ValueError:
        print ('Incorrect port.')
        sys.exit()

    #determine if port number is in the valid range 
    if ((serverPort < 1024) or (serverPort > 65536)):
        print ('Invalid port number, please try again.')
        sys.exit()

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(1)
    print ('The server is ready to receive')

    while 1:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024)
        response = ''
        result = ''
        
        #md5 returns a 32 character string
        if (message == 'ACK'):
            if debug:
                print ('Receiving authentication request ' + message +' from client.')
#---------------------------------------------------------------------------------------> need to be changed to a unique string
            ##challenge = str(hashlib.md5(('I need to get this')).hexdigest()) + str(hashlib.md5(('homework done')).hexdigest())
            ran = str(random.randint(0,9)*17)+'something'
            challenge = str(hashlib.md5(ran).hexdigest()) + str(hashlib.md5(ran+ran).hexdigest())
            connectionSocket.send(challenge)
            if debug:
                print ('Sending challenge string: ', challenge)

            message = connectionSocket.recv(1024)
            if debug:
                print ('Receiving hash ' +message+ ' from client.')

            #received message format: username + '.' + hash
            dot = message.index('.')
            username = message[0:dot]
            hashed = message[dot+1:]
            
            checkUser = 0
#            for i in list1:
#                #determine if the username exist
#                if i[0] == username:
#                    checkUser = 1
#                    result = i[0] + i[1] + challenge
#                    result = hashlib.md5(result).hexdigest()


            #------------------------SENSORID-----------
            pass1=''
            with open(sys.argv[4], 'rb') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if (row[0] == str(username)):
			checkUser = 1;
                        pass1 = row[1]
                                                       
            #concat user, pass, mystery string for hashing
            result = username + pass1 + challenge
            result = hashlib.md5(result).hexdigest()   

            response2 = username

#----------------------------------------------------------------BELOW IS WHERE WE SEND THE RESPONSE BACK TO CLIENT            
            if result == hashed:
                response = 'Welcome to our service.'
            elif checkUser and (result != hashed):
                response = 'Correct username, incorrect password.'
            else:
                response = 'User authorization failed.'
        else:
            response = 'Authentication request from client not received.'
            if debug:
                print ('Authentication request from client not received.')
        
        #send the message to the client
        connectionSocket.send(response)
        if debug:
            print ('Sending response ' + response + ' to client.')

        data = connectionSocket.recv(1024)
        sensorMin = 10
        sensorAvg = 15
        sensorMax = 20
        allAvg = 25
        response2 = response2+' recorded: '+data+' '+(datetime.datetime.now().strftime('%B %d %H:%M:%S'))+' sensorMin: '+ str(sensorMin)+' sensorAvg: '+str(sensorAvg)+' sensorMax: '+str(sensorMax)+' allAvg: '+str(allAvg)
        connectionSocket.send(response2)

        connectionSocket.close()

else:
    print ('Missing port number, please try again.')
    print (len(sys.argv))
    print (sys.argv[0]) 
    print (sys.argv[1])
    #print (sys.argv[2])
    #print (sys.argv[3])
    #print (sys.argv[4])
    #print (sys.argv[5])
    sys.exit()
