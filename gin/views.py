#-*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from hcb.gin.models import BlogPost, Incident, FormIncident
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def user_is_staff(user):
    return user.is_staff

def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template('archive.html')
    c = Context({'posts': posts})
    return HttpResponse(t.render(c))
def index(request):
    #incidents = Incident.objects.all()
    incidents = Incident.objects.filter(author = request.user)
    return render_to_response("index.html", {'incidents': incidents}, context_instance=RequestContext(request))
@user_passes_test(user_is_staff)
def add_incident(request):
    """Создает новый инцидент"""
    pass
def list_incident(request):
    pass
@user_passes_test(user_is_staff)
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    form = FormIncident(instance=incident)
    return render_to_response("detail.html", {'incident':incident, 'form':form },context_instance=RequestContext(request))