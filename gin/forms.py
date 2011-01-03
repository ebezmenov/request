#-*- coding: utf-8 -*-
from django import forms
from hcb.gin.models import Incident, Client, Solution
from django.forms import ModelForm
STATUS_CHOICES = (('1','New'),
    ('2','Close'),
    ('3','В работе'),
    ('4','Решение невозможно'),
    ('5','Отменено'),
)
class FormIncidentEdit(ModelForm):
    class Meta:
       model = Incident
       exclude = ('author','client')

class FormClient(ModelForm):
    class Meta:
        model = Client

class FormSolution(ModelForm):
    class Meta:
        model = Solution
        exclude = ('author', 'incident')