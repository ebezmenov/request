#-*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import permalink
from datetime import datetime

STATUS_CHOICES = (('1','Новый'),
    ('3','В работе'),
    ('4','Отменено'),
    ('5','Решение невозможно'),
)

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    timestamp = models.DateTimeField()
    class Meta:
        ordering = ('-timestamp',)

class BlogPostAdmin(admin.ModelAdmin):
    """Class for me"""
    list_display = ('title', 'timestamp')

admin.site.register(BlogPost, BlogPostAdmin)

class EmployeeProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    departament = models.CharField(max_length=50)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'departament')
admin.site.register(EmployeeProfile,EmployeeProfileAdmin)

class Client(models.Model):
    first = models.CharField('Имя',max_length=50)
    last = models.CharField("Фамилия" ,max_length=50)
    middle_name =models.CharField('Отчество', max_length=50) 
    inn = models.DecimalField('INN', max_digits=10, decimal_places=0)
    def __unicode__(self):
        return self.first+" "+self.last
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first','last')
admin.site.register(Client, ClientAdmin)

class Incident(models.Model):
    timestamp = models.DateField(auto_now_add = True)
    title = models.CharField(max_length=50)
    client = models.ForeignKey(Client)
    author = models.ForeignKey(User)
    responsibles = models.ManyToManyField(User, related_name='respons')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default='1')
    incoming_number = models.CharField('Входящий номер', max_length=20)
    class Meta:
        permissions = (
        ("can_view_all","могут видеть все"),
        ('can_close_incident','Могут закрывать инциденты')
        )

    def __unicode__(self):
        return self.title
    @permalink
    def get_absolute_url(self):
        return ('incident_detail',[str(self.id)])
    
    def get_list_resp(self):
        return self.responsibles.all()

class FormIncident(ModelForm):
     class Meta:
        model = Incident
        exclude = ('author','client', 'status')


#fgfdg
admin.site.register(Incident)