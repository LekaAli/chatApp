#! -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SO_REUSEADDR
from socket import SOL_SOCKET
from threading import Thread
import select

# Create your views here.
class ClientThread(Thread):

    def __init__(self,ip,port,client_socket):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.client_socket = client_socket

    def run(self):
        self.client_socket.send('Thank you for connecting to me')

def index(request):
    return render(request,'start_server/start.html')

def boardcast(client,server, SOCKET_LISTS, message):
    for socket in SOCKET_LISTS:
        if socket != client and socket != server:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in SOCKET_LISTS:
                    SOCKET_LISTS.remove(socket)

def startServer(request):
    results = None
    INPUT_SOCKET_LIST = []
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    if request.method == 'POST':
        option = request.POST.get('serveroption')
        if option == 'start':
            try:
                HOST = str(request.POST.get('host'))
                PORT = int(request.POST.get('port'))
                SERVER_ADDR = (HOST,PORT)
                BUFFER_SIZE = 4096
                threads = []
                server_socket.bind(SERVER_ADDR)
                INPUT_SOCKET_LIST.append(server_socket)
                results = 'Server started on address %s port %s' % (HOST, PORT)

                while True:
                    server_socket.listen(2)
                    ready_to_read, ready_to_write, in_error = select.select(INPUT_SOCKET_LIST, [], [], 0)
                    for sock in ready_to_read:
                        if sock == server_socket:
                            (client_socket,(client_addr, client_port)) = server_socket.accept()
                            INPUT_SOCKET_LIST.append(client_socket)
                            boardcast(client_socket, server_socket, INPUT_SOCKET_LIST, "[%s:%s] joined our chat room" % (client_addr,client_port))
                            
                            client_thread = ClientThread(client_addr,client_port,client_socket)
                            client_thread.start()
                            threads.append(client_thread)
                        else:
                            try:
                                data = sock.recv(BUFFER_SIZE)
                                if data:
                                    boardcast(sock,server_socket, INPUT_SOCKET_LIST, data)
                                else:
                                    if sock in INPUT_SOCKET_LIST:
                                        INPUT_SOCKET_LIST.remove(sock)
                                    boardcast(sock, server_socket, INPUT_SOCKET_LIST, "Offline")
                            except Exception as e:
                                boardcast(sock, server_socket, INPUT_SOCKET_LIST, "Offline")
                                continue

                for thread in threads:
                    thread.join()

            except Exception as e:
                results = 'Server not started on address %s port %s' % (HOST,PORT)
            return HttpResponse('<h3>' + results + '</h3>')
        else:
            server_socket.close()
            results = 'Server has shut down.'
    return HttpResponse('<h3>' + results + '</h3>')
