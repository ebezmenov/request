#-*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import permalink

STATUS_CHOICES = (('1','Новый'),
    ('3','В работе'),
    ('4','Отменено'),
    ('5','Решение невозможно'),
)
REGION_UKRAINE = ((1,'Киевская'),
                  (2,'Днепропетровская')
                  )

CATEGORY = ((0,'Кадровые вопросы'),
            (1,'Жалобы на качество работы подразделения'))
class EmployeeProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    departament = models.CharField(max_length=50)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'departament')
admin.site.register(EmployeeProfile,EmployeeProfileAdmin)

class FormAppeal(models.Model):
    name = models.CharField('Форма обращения', max_length=20)
    def __unicode__(self):
        return "%s" % self.name
admin.site.register(FormAppeal)

class Category(models.Model):
    subcatagory = models.CharField('Подкатегория',max_length=100, blank = True)
    def __unicode__(self):
        return '%s' % self.subcatagory

admin.site.register(Category)

class Client(models.Model):
    first = models.CharField('Имя',max_length=50)
    last = models.CharField("Фамилия" ,max_length=50)
    middle_name =models.CharField('Отчество', max_length=50) 
    inn = models.DecimalField('ИНН', max_digits=10, decimal_places=0, blank= True, null=True)
    agreement = models.CharField('Договор', max_length=30, blank=True)
    region = models.IntegerField('Область', choices = REGION_UKRAINE, default='1')
    city = models.CharField('Город', max_length=30, blank=True)
    adres = models.CharField('Адрес', max_length=50, blank=True)
    postal_code = models.IntegerField('Индекс', blank = True, null=False, default = 0)
    def __unicode__(self):
        return self.first+" "+self.last
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first','last')
admin.site.register(Client, ClientAdmin)

class Incident(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    title = models.CharField('Обращение',max_length=50)
    client = models.ForeignKey(Client)
    author = models.ForeignKey(User)
    responsibles = models.ManyToManyField(User, related_name='respons')
    status = models.CharField('Статус', max_length=1,choices=STATUS_CHOICES, default='1')
    incoming_number = models.CharField('Входящий номер', max_length=20)
    form_appeal = models.ForeignKey(FormAppeal, blank = True)
    data_answer_client = models.DateField('Дата ответа клиенту', blank = True, null=True)
    category = models.ForeignKey(Category, blank = True, null=True)
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

class Solution(models.Model):
#Class Solution 
    author = models.ForeignKey(User)
    incident = models.ForeignKey(Incident)
    timestamp = models.DateTimeField(auto_now_add = True)
    text = models.CharField('Решение',max_length=150)
    
    def __unicode__(self):
        return str(self.author) + self.text
    
class Attachment(models.Model):
    slug = models.CharField('Описание', max_length=80)
    file_document = models.FileField(upload_to='upload_doc/')
    incident = models.ForeignKey(Incident)
    
    def __unicode__(self):
        return '%s' % self.slug

    
admin.site.register(Attachment)
admin.site.register(Incident)
admin.site.register(Solution)