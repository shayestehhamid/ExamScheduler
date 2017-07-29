# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


global months
months = {1:'فروردین', 2:'اردیبهشت', 3:'خرداد', 4:'تیر', 5:'مرداد', 6:'شهریور', 7:'مهر', 8:'آبان', 9:'آذر', 10:'دی', 11:'بهمن', 12:'اسفند'}


# constraint to keep them safe!
# not in same days
# not in following days
class ConstraintType(models.Model):
	typec = models.CharField(primary_key=True, max_length=50)
	description = models.CharField(max_length=50)

class Constraint(models.Model):
	typec = models.ForeignKey(ConstraintType)
	c1 = models.ForeignKey('Course', related_name='course1')
	c2 = models.ForeignKey('Course', related_name='course2')
	project = models.ForeignKey('Project')

class Student(models.Model):
	stdnom = models.CharField(primary_key=True, max_length=60)
	def __repr__(self):
		print self.stdnom
class Teacher(models.Model):
	name = models.CharField(max_length=60)


class Course(models.Model):
	name = models.CharField(max_length=40)
	students = models.ManyToManyField(Student)
	time = models.ForeignKey('Time', null=True)
	teacher = models.ForeignKey(Teacher, null=True)
	project = models.ForeignKey('Project', null=True)

class Project(models.Model):
	name = models.CharField(max_length=50)


class Time(models.Model):
	d = models.IntegerField(default=1)
	m = models.IntegerField(default=1)

	h = models.IntegerField(default=8)
	weekday = models.CharField(max_length=20)
	project = models.ForeignKey(Project)

	def __str__(self):
		return " " + str(self.d) + '-'+str(self.m)+' '+str(self.h)

	def calcmonth(self):
            global months
            return months[self.m]
	month = property(calcmonth)
