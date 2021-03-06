#-*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from hcb.gin.models import Incident
from hcb.gin.forms import FormIncidentEdit, FormClient, FormSolution
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
# Create your views here.

def user_is_staff(user):
    return user.is_staff

def user_can_closed(user):
    return user.has_perm('gin.can_close_incident')

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
#TODO Create new
def new_incident(request):
    if request.method == 'POST':
        form=FormIncidentEdit(request.POST)
        form_client = FormClient(request.POST)
        if form_client.is_valid():
            client = form_client.save()
            if form.is_valid():
                new_incident = form.save(commit=False)
                new_incident.author = request.user
                new_incident.client = client
                new_incident.save()
                form.save_m2m()
                return HttpResponseRedirect(reverse('list_inc'))
    else:
        form = FormIncidentEdit(initial={'title':'название темы'})
        form_client = FormClient()
    #form.author = request.user
    return render_to_response("new_inc.html", {'form':form, 'form_client':form_client }, context_instance=RequestContext(request))

def list_incident(request):
    pass

def incident_detail_view(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    form = FormIncidentEdit(instance=incident)
    sol = incident.solution_set.all()
    return render_to_response("view_detail.html", {'incident':incident, 'form':form, 'sol': sol },context_instance=RequestContext(request))


def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    sol = incident.solution_set.all()
    if request.method == 'POST':
        form = FormIncidentEdit(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return render_to_response("view_detail.html", {'incident':incident, 'form':form, 'sol': sol },context_instance=RequestContext(request))
    else:
        form = FormIncidentEdit(instance=incident)
    return render_to_response("detail.html", {'incident':incident, 'form':form },context_instance=RequestContext(request))

@user_passes_test(user_can_closed)
def incident_closed(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    incident.status = '2' # ставим статус закрытия инцидента
    incident.save()
    return HttpResponseRedirect(reverse('incident_detail', args=[incident.id]))

def add_solution(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id )
    if request.method == 'POST':
        # FIXME:  Make a form 
        print 'sss'
        solution_form = FormSolution(request.POST)
        if solution_form.is_valid():
            solution = solution_form.save(commit=False)
            solution.author = request.user
            solution.incident = incident
            print solution.author
            print solution.id
            solution.save()
            return HttpResponseRedirect(reverse('incident_detail', args=[incident.id]))
    else:
        solution = FormSolution()
    return render_to_response("detail.html", {'incident':incident, 'sol':solution },context_instance=RequestContext(request))