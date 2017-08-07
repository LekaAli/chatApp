# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ChatUsers(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=100)
    comments = models.CharField(max_length=200)
