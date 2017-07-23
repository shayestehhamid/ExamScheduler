# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import RequestConfig

from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
# /projects
# list of projects
# and create a new project here
def projects(request):
	if request.method == "POST":
		lform = NewProject(request.POST)
		if lform.is_valid():
			actant = lform.cleaned_data['accountant']
			cart_number = lform.cleaned_data['cart_number']
			account_number = lform.cleaned_data['account_number']
			account_type = lform.cleaned_data['account_type']
			ac = Account()
			ac.accountant = actant
			ac.cart_number = cart_number
			ac.account_number = account_number
			ac.account_type = account_type
			ac.save()

	return render(request, 'projects.html')

# remove project, go to projects
# /removeproject/id
def project_remove(request):
	pass

# /project/time/projectid
# add a new time 
# list of times
def times(request):
	pass

# /removetime/projectid/timeid
# go to times page
def time_remove(request):
	pass

# /teachers/
# possible to add a new teacher 
# list of teachers
def teachers(request):
	pass

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