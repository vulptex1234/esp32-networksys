import boot
import calc

import socket
import time
import _thread
import machine

PORT = 80
listen_socket = None
csv_file = 'node_data.csv'
param_dict = {}