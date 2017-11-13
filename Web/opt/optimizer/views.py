# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import RequestConfig
from forms import NewProject, NewTime
from django.http import HttpResponse, HttpResponseRedirect
from models import Project, Teacher, Time, Constraint, Student, Course, ConstraintType, Message
import xlrd
import data as Data
import threading

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
	pr = Project.objects.get(id=prid)
	times = Time.objects.filter(project=pr)
	# print times
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
	timeid = request.POST['time']
	teacher = Teacher.objects.get(id=tid)
	time = Time.objects.get(id=timeid)
	course = Course.objects.get(id=crid)
	course.teacher = teacher
	course.time = time
	course.save()
	return HttpResponseRedirect('/project/students/'+str(crid)+'/'+str(prid))

# /result/projectid
def result(request, prid):
	import optimizer
	op = optimizer.Optimize(prid)
	op.start()
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
	pr = Project.objects.get(id=prid)
	times = Time.objects.filter(project=pr)
	return render(request, 'course.html', {'times':times, 'course':course, "students":students, 'prid':prid, 'crid':crid, 'teachers':teachers})

def comp_eng(courses):
	cont_time = 0
	in_day_time = 0
	cont_day = 0
	same_time = 0
	for c1 in courses:
		for c2 in courses:
			if c1.id < c2.id:
				if not c1.time or not c2.time:
					continue
				if c1.time == c2.time:
					same_time += Data.students_conflict(c1.id, c2.id)
				elif Data.continues_time_time(c1.time, c2.time):
					cont_time += Data.students_conflict(c1.id, c2.id)
				elif Data.in_day_time(c1.time, c2.time):
					in_day_time += Data.students_conflict(c1.id, c2.id)
				elif Data.continues_day_time(c1.time, c2.time):
					cont_day += Data.students_conflict(c1.id, c2.id)
	return [('continues_time', cont_time), ('in_day',in_day_time), ('continues_day',cont_day), ('same_time', same_time)]

def courses(request, prid):
	pr = Project.objects.get(id=prid)
	courses = Course.objects.filter(project=pr)
	conflicts = comp_eng(courses)
	msgs = Message.objects.filter(project=pr)
	print conflicts
	data = {'courses':courses, 'prid':prid, 'msgs':msgs}
	for key, val in conflicts:
		data[key] = val
	return render(request, 'courses.html', data)

def upload_courses(prid, filename):
	book = xlrd.open_workbook(filename)
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
def course_remove(request, crid, prid):
	Course.objects.get(id=crid).delete()
	return HttpResponseRedirect('/project/course/'+str(prid)+'/')
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


def dl_excel(request, prid):
	proj = Project.objects.get(id=int(prid))
	courses = Course.objects.filter(project=proj)
	import xlsxwriter
	from django.utils.encoding import smart_str
	workbook = xlsxwriter.Workbook('book.xlsx')
	worksheet = workbook.add_worksheet()
	row = 0
	
	for course in courses:
		worksheet.write(row, 0, course.name)
		worksheet.write(row, 1, course.teacher.name)
		worksheet.write(row, 2, course.time.d)
		worksheet.write(row, 3, course.time.m)
		worksheet.write(row, 4, course.time.h)
		row+=1
	workbook.close()
	# import xlrd
	# workbook = xlrd.open_workbook('book.xlsx')
	# print workbook.sheet_names()
	# from django.core.servers.basehttp import FileWrapper
	from wsgiref.util import FileWrapper
	import os, tempfile, zipfile
	filename = 'book.xlsx' # Select your file here.                                
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Length'] = os.path.getsize(filename)
	return response


def upload_excel(request, prid):
	from django.core.files.storage import FileSystemStorage
	import datetime
	if request.method == "POST":
		
		myfile = request.FILES['excel']
		fs = FileSystemStorage()
		filename = 'excel' + str(datetime.datetime.now()) + ".xlsx"
        filename = fs.save(filename, myfile)
        uploaded_file_url = fs.url(filename)
        return upload_courses(prid, filename)


		
