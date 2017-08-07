# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
import select
import sys
from .models import ChatUsers

LIST_SOCKET = []

@login_required
def home(request):
    return render(request,'html/home.html')

def sendMessage(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        sock_port = int(request.POST.get('client_socket_port'))
        ready_to_read, ready_to_write, in_error = select.select(LIST_SOCKET, LIST_SOCKET, [], 0)
        for sock in ready_to_write:
            ip_addr, port = sock.getsockname()
            if sock_port == port and message:
                sock.send(message)
                chatuser = ChatUsers.objects.create(sender=str(request.user),comments=message.strip())
                chatuser.save()
    return render(request,'html/home.html')

def requestConnection(request):
    if request.method == 'POST':
        ipaddress = request.POST.get('ipaddress')
        portnumber = int(request.POST.get('port'))
        userchat = ChatUsers.objects.all()
        HOST = ipaddress
        PORT = portnumber
        BUFFER_SIZE = 4096
        SERVER_ADDR = (HOST,PORT)
        try:
            client_socket = socket(AF_INET,SOCK_STREAM)
            client_socket.connect(SERVER_ADDR)
            LIST_SOCKET.append(client_socket)
            data = client_socket.recv(BUFFER_SIZE)
            ip_addr,port = client_socket.getsockname()
            return render(request, 
                'html/connected.html', 
                {'username':request.user,'socket_port': port,'chats': userchat})
        except Exception as e:
            return HttpResponse('<h3>Connection to the server failed...</h3>')
