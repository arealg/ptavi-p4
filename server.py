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
    SIP Register Handler
    """
    dicc = {}

    def register2json(self):
        """
        Se registra al cliente en un fichero json.
        """
        with open('registered.json', 'w') as file:
            json.dump(self.dicc, file, sort_keys=True, indent=4)

    def registrar_cliente(self, IP, login, tiempo):
        """
        Se añade al cliente con un Address y Expires en un diccionario.
        """
        lista_info = {}
        lista_info['address'] = IP
        lista_info['expires'] = (time.strftime('%Y-%m-%d %H:%M:%S +0100',
                                 time.localtime(tiempo)))
        self.wfile.write(b"SIP/2.0 200 OK" + b'\r\n\r\n')
        self.dicc[login] = lista_info

    def tiempo_exp(self):
        lista_user = []
        for login in self.dicc:
            exp = time.strptime(self.dicc[login]['expires'],
                                '%Y-%m-%d %H:%M:%S +0100')
            if time.time() >= time.mktime(exp):
                lista_user.append(login)
        for login in lista_user:
                del self.dicc[login]

    def json2registered(self):
        """
        Se mira si hay un fichero registered.json.
        """
        try:
            with open('registered.json', 'r') as fich:
                fichero = json.loads(fich.read())
                self.dicc = fichero
        except:
            pass

    def handle(self):
        """
        Se identifica al cliente y se registra en un diccionario.
        """
        self.json2registered()
        IP = self.client_address[0]
        PUERTO = self.client_address[1]
        print("{} {}".format(IP, PUERTO))
        while 1:
            line = self.rfile.read()
            if not line:
                break
            linea = line.decode('utf-8')
            lista = linea.split()
            expires = lista[4]
            if 'REGISTER' in lista:
                login = lista[1].split(':')[1]
                self.tiempo_exp()
                if expires == '0':
                    if login in self.dicc:
                        del self.dicc[login]
                        self.wfile.write(b"SIP/2.0 200 OK" + b'\r\n\r\n')
                else:
                    tiempo = time.time() + float(lista[4])
                    self.registrar_cliente(IP, login, tiempo)
            self.register2json()

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
