import socket
from f1_2020_telemetry.packets import unpack_udp_packet

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))

#s = socket.socket()
#s.connect(("192.168.0.163", 20777))

oldFlag = ""
flag = 0
counter = 0
printString = ""
toSend = ""
sent = ""

while True:
    flag = 0
    udp_packet = udp_socket.recv(2048)
    # print(udp_packet)

    if udp_packet[5:6].decode() == '\x07':
        packet = unpack_udp_packet(udp_packet)
        # flag = packet.carStatusData[21].vehicleFiaFlags #vietnam
        # 19 for austrailia

        for i in packet.carStatusData:
            if i.vehicleFiaFlags > flag:
                flag = i.vehicleFiaFlags
        
        print(flag)

        # conc = ""
        # for i,j in enumerate(packet.carStatusData):
        #     # if j.vehicleFiaFlags != 0:
        #     conc = conc + str(j.vehicleFiaFl  ags) + "_" + str(i) + " "
        # print(conc)

        if flag != oldFlag:
            print("Current Flag", flag)
            oldFlag = flag

        if flag == 3:
            toSend = "255,100,0\r"
        if flag == 2:
            toSend = "0,0,255\r"
        if flag == 1 or flag == 0:
            toSend = "0,255,0\r"

        if toSend != sent:
            s.send(toSend.encode())
            print("sent", toSend)
            sent = toSend
