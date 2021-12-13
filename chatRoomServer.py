import re
import os
import socket as sk

userNameMap = {}
serverPort = 16888
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
serverSocket.bind(("", serverPort))


def main():
    while True:
        try:
            f = open('ChatFile.txt', 'a')
            userName = "Server"
            message, clientAddress = serverSocket.recvfrom(9999)
            message = message.decode()
            storedInfo = clientAddress[0] + ' port: ' + str(clientAddress[1]) + ', ' + message
            print(storedInfo, end='')
            f.write(storedInfo + '\n')
            if userNameMap.get(clientAddress) is None:  # 如果没有注册传来的就是名字
                print('joined')
                userNameMap[clientAddress] = message
                replayMessage = "Welcome " + message
            elif message == userNameMap[clientAddress] + " has left":
                print()
                replayMessage = "Good bye " + userNameMap[clientAddress]
                del userNameMap[clientAddress]
            else:
                print()
                replayMessage = message
            for perUser in userNameMap.keys():
                if replayMessage.find("Welcome") != -1 or userNameMap.get(clientAddress) is None:
                    pass
                else:
                    userName = userNameMap[clientAddress]
                serverSocket.sendto(("[" + userName + "]: " + replayMessage).encode(), perUser)
            f.close()
        except:
            continue


if __name__ == "__main__":
    main() 
