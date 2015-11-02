#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import time


if len(sys.argv) != 6:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')


SERVER = sys.argv[1]
PORT = int(sys.argv[2])

LINE = " ".join(sys.argv[3:])
linea = LINE.split()
LINE = linea[0].upper() + ' ' + 'sip:' + linea[1] + ' ' + 'SIP/2.0' + '\r\n'

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

EXPIRES = linea[2]

print(LINE + 'Expires: ' + EXPIRES + '\r\n\r\n')
LINE = LINE + 'Expires: ' + EXPIRES
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n\r\n')
data = my_socket.recv(1024)

print(data.decode('utf-8'))
print("Socket finalizado.")

my_socket.close()
