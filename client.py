#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import time

# Cliente UDP simple.

if len(sys.argv) != 6:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Dirección IP del servidor.

SERVER = sys.argv[1]
PORT = int(sys.argv[2])

# Contenido que vamos a enviar
LINE = " ".join(sys.argv[3:])
linea = LINE.split()
LINE = linea[0].upper() + ' ' + 'sip:' + linea[1] + ' ' + 'SIP/2.0' + '\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

EXPIRES = linea[2]

print(LINE + 'Expires: ' + EXPIRES + '\r\n\r\n')
LINE = LINE + 'Expires: ' + EXPIRES
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n\r\n')
data = my_socket.recv(1024)

print(data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
