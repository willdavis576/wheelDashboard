import socket
from socket import *
from struct import *

serverName='192.168.0.163'
serverPort = 20777
clientSocket = socket(AF_INET,SOCK_DGRAM)


messageback=clientSocket.recvfrom(1024)
print( 'received')
pktformat='100s100sii100s100s'
n = calcsize(pktformat)
print (n)
print (unpack(pktformat, messageback))

backString = unpack(pktformat, messageback)
        
