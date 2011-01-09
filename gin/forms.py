#-*- coding: utf-8 -*-
from hcb.gin.models import Incident, Client, Solution, Attachment
from django.forms import ModelForm
from django import forms
STATUS_CHOICES = (('1','New'),
    ('2','Close'),
    ('3','В работе'),
    ('4','Решение невозможно'),
    ('5','Отменено'),
)
class FormIncidentEdit(ModelForm):
#    data_answer_client = forms.DateField(required=False)
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

class FormAttachment(ModelForm):
    class Meta:
        model = Attachment