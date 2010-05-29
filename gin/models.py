from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

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
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first','last')
admin.site.register(Client, ClientAdmin)

class Incident(models.Model):
    timestamp = models.DateField()
    title = models.CharField(max_length=50)
    client = models.ForeignKey(Client)
    author = models.ForeignKey(User)
    responsibles = models.ManyToManyField(User, related_name='respons')


admin.site.register(Incident)