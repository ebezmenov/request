#-*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from hcb.gin.models import BlogPost, Incident, FormIncident
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
# Create your views here.

def user_is_staff(user):
    return user.is_staff

def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template('archive.html')
    c = Context({'posts': posts})
    return HttpResponse(t.render(c))

@login_required
def index(request):
    #all_incidents = Incident.objects.all()
    incidents = Incident.objects.filter(Q(responsibles = request.user)|Q(author = request.user)).distinct()
    if not request.user.is_staff:
        incidents = incidents.filter(author = request.user)
    if request.user.has_perm('gin.can_view_all'):
        incidents = Incident.objects.all()
    return render_to_response("index.html", {'incidents': incidents}, context_instance=RequestContext(request))

@user_passes_test(user_is_staff)
def add_incident(request):
    """Создает новый инцидент"""
    pass

def new_incident(request):
    if request.method == 'POST':
        form=FormIncident(request.POST)
        if form.is_valid():
            new_incident = form.save(commit=False)
            new_incident.author = request.user
            new_incident.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('list_inc'))
    else:
        form = FormIncident(initial={'title':'название темы'})
    #form.author = request.user
    return render_to_response("new_inc.html", {'form':form}, context_instance=RequestContext(request))

def list_incident(request):
    pass
@user_passes_test(user_is_staff)
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    form = FormIncident(instance=incident)
    return render_to_response("detail.html", {'incident':incident, 'form':form },context_instance=RequestContext(request))