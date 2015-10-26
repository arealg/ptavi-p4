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
        Registramos al cliente en un fichero json
        """
        with open('registered.json', 'w') as file:
            json.dump(self.dicc, file, sort_keys=True, indent=4)

    def registrar_user(self, IP, login, tiempo):
        """
        Añadimos al cliente con un Address y Expires en un diccionario,
        que mas adelante lo añadimos al fihcero json
        """
        lista_info = {}
        lista_info['address'] = IP
        lista_info['expires'] = (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tiempo)))
        self.wfile.write(b"SIP/2.0 200 OK" + b'\r\n\r\n')
        self.dicc[login] = lista_info

    # def json2registered(self):
    #     """
    #
    #     """
    #     try:
    #         fich =  open('registered.json','r')
    #         data = fich.readlines()
    #         fichero = json.loads(data)
    #         fich.close()
    #     except:
    #         pass

    def handle(self):
        """
        Principal método de la clase SIPRegisterHandler, identificamos al
        cliente, leemos lo que nos envía y respondemos. También Registramos
        y borramos a un cliente dependiendo de su tiempo de Expiración
        """
        # self.json2registered()
        tiempo_real = time.time()
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP = self.client_address[0]
        PUERTO = self.client_address[1]
        print("{} {}".format(IP, PUERTO))
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
                    if login in self.dicc:
                        del self.dicc[login]
                        self.wfile.write(b"SIP/2.0 200 OK" + b'\r\n\r\n')
                else:
                    tiempo = tiempo_real + float(lista[3])
                    print('TIEMPO MAS EXPIRE',tiempo)
                    self.registrar_user(IP, login, tiempo)
                    self.register2json()
            # print(self.dicc)
            try:
                for i in self.dicc:
                    print('SALIDO DEL FICH',self.dicc[i]['expires'])
                    exp = time.strptime(self.dicc[i]['expires'], '%Y-%m-%d %H:%M:%S')
                    exp_new = time.mktime(exp)
                    print('SALIDO Y PASADO POR STRP',time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(exp_new)))
                    # print('TIEMPO EXP',time.mktime(exp))
                    # if time.time() >= time.mktime(exp):
                    #      del self.dicc[i]
            except:
                pass
            # print(self.dicc)


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
