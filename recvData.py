from socket import *
from struct import *
from IPython import embed

serverName='192.168.0.163'
serverPort = 9996
clientSocket = socket(AF_INET,SOCK_DGRAM)
message=pack('iii',1,1,0)

clientSocket.sendto(message, (serverName, serverPort))

messageback, ipAddress=clientSocket.recvfrom(1024)
print( 'received')
pktformat='100s100sii100s100s'
n = calcsize(pktformat)
print (n)
print (unpack(pktformat, messageback))

backString = unpack(pktformat, messageback)

carName = backString[0].decode(errors='ignore').replace('\x00', '').split('%')[0]
driverName = backString[1].decode(errors='ignore').replace('\x00', '').split('%')[0]
trackName = backString[4].decode(errors='ignore').replace('\x00', '').split('%')[0]
trackConfig = backString[5].decode(errors='ignore').replace('\x00', '').split('%')[0]

print(carName, driverName, trackName)

message=pack('iii',1,1,1)
clientSocket.sendto(message, (serverName, serverPort))

i=0


while 1:
    pktformat='cifff??????fffiiiifffffiffffffffffffffffff'
    messageback, ipAddress =clientSocket.recvfrom(16384)
    backString = unpack(pktformat, messageback[:152])
    print (backString[:7])

    gear = backString[23]
    speed = backString[3]
    

    i+=1



clientSocket.close()