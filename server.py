#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    lista = []


    def register2json(self):
        with open('registered.json', 'w') as file:
            json.dump(self.lista, file, sort_keys=True, indent=4)

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        ip = self.client_address[0]
        puerto = self.client_address[1]
        print("{} {}".format(ip, puerto))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            linea = line.decode('utf-8')
            lista = linea.split()
            if 'REGISTER' in lista:
                login = lista[1].split(':')[1]
                if '0' in lista:
                    self.wfile.write(b"SIP/2.0 200 OK" + b'\r\n\r\n')
                else:
                    self.dicc['address'] = ip
                    self.dicc['expires'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))+ ' ' + lista[3]
                    self.wfile.write(b"SIP/2.0 200 OK" + b'\n')
                    lista_user = [login,self.dicc]
                    self.lista.append(lista_user)
        self.register2json()



if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
