# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import RequestConfig
from forms import NewProject, NewTime
from django.http import HttpResponse, HttpResponseRedirect
from models import Project, Teacher, Time
# Create your views here.
# /projects
# list of projects
# and create a new project here
def projects(request): # done
	if request.method == "POST":
		lform = NewProject(request.POST)
		if lform.is_valid():
			name = lform.cleaned_data['name']
			proj = Project()
			proj.name = name
			
			proj.save()
			
	projects = Project.objects.all()
	
	return render(request, 'projects.html', {'newproject':NewProject(), 'projects':projects})

# remove project, go to projects
# /removeproject/id

def project_remove(request):
	pass

# /project/time/projectid
# add a new time 
# list of times
def times(request, prid):
	if request.method == "POST":
		lform = NewTime(request.POST)
		if lform.is_valid():
			d = lform.cleaned_data['d']
			m = lform.cleaned_data['m']
			y = lform.cleaned_data['y']
			h = lform.cleaned_data['h']
			weekday = lform.cleaned_data['weekday']
			time = Time()
			time.d = d
			time.m = m
			time.y = y
			time.h = h
			time.weekday = weekday
			time.project = Project.objects.get(id=int(prid))
			time.save()
			

	return render(request, 'time.html', {'days':range(1, 32)})


# /removetime/projectid/timeid
# go to times page
def time_remove(request):
	pass

# /teachers/
# possible to add a new teacher 
# list of teachers
def teachers(request):
	if request.method == "POST":
		lform = NewProject(request.POST)
		if lform.is_valid():
			name = lform.cleaned_data['name']
			tr = Teacher()
			tr.name = name
			
			tr.save()
			
	teachers = Teacher.objects.all()
	
	return render(request, 'teachers.html', {'newproject':NewProject(), 'teachers':teachers})

# /removeteacher/id
def teacher_remove(request):
	pass


# /result/projectid
def result(request):
	pass


# save the changes
# reload the result page
# /save/projectid
def save(request):
	pass