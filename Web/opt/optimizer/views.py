# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import RequestConfig
from forms import NewProject, NewTime
from django.http import HttpResponse, HttpResponseRedirect
from models import Project, Teacher, Time, Constraint, Student, Course, ConstraintType
import xlrd
import data as Data


global months
months = {1:'فروردین', 2:'اردیبهشت', 3:'خرداد', 4:'تیر', 5:'مرداد', 6:'شهریور', 7:'مهر', 8:'آبان', 9:'آذر', 10:'دی', 11:'بهمن', 12:'اسفند'}
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

def project_remove(request, prid):
	Project.objects.filter(id=prid).delete()
	return HttpResponseRedirect('/projects')

# /project/time/projectid
# add a new time 
# list of times
def times(request, prid):
	global months
	if request.method == "POST":
		lform = request.POST
		d = lform['days']
		m = lform['months']
		h = lform['hour']
		weekday = lform['weekday']
		print d, m, h, weekday, 'printing!'
		time = Time()
		time.d = d
		time.m = m
		time.h = h
		time.weekday = weekday
		time.project = Project.objects.get(id=int(prid))
		time.save()
			
	times = Time.objects.all()
	print times
	return render(request, 'time.html', {'days':range(1, 32), 'times':times, 'prid':prid})


# /removetime/projectid/timeid
# go to times page
def time_remove(request, tid, prid):
	t = Time.objects.filter(id=tid)
	t.delete()
	return times(request, prid)

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
def teacher_remove(request, tid):
	Teacher.objects.filter(id=tid).delete()
	return HttpResponseRedirect('/teachers')

def set_teacher(request, crid, prid):
	tid =  request.POST['teacher']
	teacher = Teacher.objects.get(id=tid)
	course = Course.objects.get(id=crid)
	course.teacher = teacher
	course.save()
	return HttpResponseRedirect('/project/students/'+str(crid)+'/'+str(prid))

# /result/projectid
def result(request, prid):
	import optimizer
	optimizer.optimize(prid)
	return HttpResponseRedirect('/projects/prid/')


# save the changes
# reload the result page
# /save/projectid
def save(request):
	pass


def course(request, crid, prid):
	students = Course.objects.get(id=crid).students.all()
	teachers = Teacher.objects.all()
	course = Course.objects.get(id=crid)
	return render(request, 'course.html', {'course':course, "students":students, 'prid':prid, 'crid':crid, 'teachers':teachers})

def comp_eng(courses):
	cont_time = 0
	in_day_time = 0
	cont_day = 0
	for c1 in courses:
		for c2 in courses:
			if c1.id < c2.id:
				if not c1.time or not c2.time:
					return {}
				if Data.continues_time_time(c1.time, c2.time):
					cont_time += Data.students_conflict(c1.id, c2.id)
				elif Data.in_day_time(c1.time, c2.time):
					in_day_time += Data.students_conflict(c1.id, c2.id)
				elif Data.continues_day_time(c1.time, c2.time):
					cont_day += Data.students_conflict(c1.id, c2.id)
	return {'continues_time':cont_time, 'in_day':in_day_time, 'continues_day':cont_day}

def courses(request, prid):
	pr = Project.objects.get(id=prid)
	courses = Course.objects.filter(project=pr)
	conflicts = comp_eng(courses)
	print conflicts
	return render(request, 'courses.html', {'courses':courses, 'prid':prid, 'conflicts':conflicts})

def upload_courses(request, prid):
	book = xlrd.open_workbook('Book1.xlsx')
	coursesNum = book.nsheets
	coursesNames = book.sheet_names()
	
	for i in range(coursesNum):
		thisSheet = book.sheet_by_index(i)		
		#print thisSheet.col_values(0)
		cs = thisSheet.col_values(0)
		course_name = coursesNames[i]
		course = Course(name=course_name)
		course.save()
		pr = Project.objects.get(id=prid)
		print pr.name
		course.project = pr
		course.save()

		for st in cs:
			
			st = Student(stdnom=str(int(st)))
			st.save()
		
			course.students.add(st)
			course.save()
	return projects(request)
	# get and insert courses!
	# professors will be added seperatly
	# time will be added in solution finding!
	# computation engine we have
	# optimization engine!
def course_remove(request, crid):
	Course.objects.get(id=crid).delete()
	return HttpResponseRedirect('/projects')
def constraint(request, prid):
	if request.method == "POST":
		lform = request.POST
		c1 = lform['c1']
		c2 = lform['c2']
		tt = lform['type']
		ct = Constraint()
		ct.typec = ConstraintType.objects.get(typec=tt)
		ct.project = Project.objects.get(id=prid)
		ct.c1 = Course.objects.get(id=c1)
		ct.c2 = Course.objects.get(id=c2)
		ct.save()
	
	pr = Project.objects.get(id=prid)
	consts = Constraint.objects.filter(project=pr)
	courses = Course.objects.filter(project=pr)
	constt = ConstraintType.objects.all()
	return render(request, 'const.html', {'consts':consts, 'prid':prid, 'courses':courses, 'ctype':constt})

def const_remove(request, ctid, prid):
	const = Constraint.objects.get(id=ctid)
	const.delete()
	return HttpResponseRedirect('/project/const/'+str(prid)+'/')

def inter(request, c1, c2):
	ct = ConstraintType(typec='inday')
	ct2 = ConstraintType(typec='contday')
	ct.description = "در یک روز بودن"
	ct2.description = "در دو روز متوالی بودن"
	ct.save()
	ct2.save()
