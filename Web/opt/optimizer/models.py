from __future__ import unicode_literals

from django.db import models

class Student(models.Model):
	stdnom = models.CharField(primary_key=True, max_length=60)

class Teacher(models.Model):
	name = models.CharField(max_length=60)

class Time(models.Model):
	d = models.IntegerField(default=1)
	m = models.IntegerField(default=1)
	y = models.IntegerField(default=2017)
	h = models.IntegerField(default=8)
	weekday = models.CharField(max_length=20)

class Course(models.Model):
	name = models.CharField(max_length=40)
	students = models.ManyToManyField(Student)
	time = models.ForeignKey(Time)
	teacher = models.ForeignKey(Teacher)

class Project(models.Model):
	courses = models.ManyToManyField(Course)

