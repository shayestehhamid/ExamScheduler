# -*- coding: utf-8 -*-
import xlrd
from models import Project, Teacher, Time, Constraint, Student, Course
import xlrd

# class Chart:

# 	def openFile(self, path):
# 		self.courseToTerm = {}
# 		book = xlrd.open_workbook(path)
# 		sheet = book.sheet_by_index(0)
# 		self.courses = []
# 		for i in xrange(8):
# 			col = sheet.col_values(i)
# 			self.courses.append(col)
# 			for j in col:
# 				self.courseToTerm[j] = i

# 	def courseTerm(self, courseID):
# 		return self.courseToTerm[courseID] if courseID in self.courseToTerm else []

# 	def termCourses(self, term):
# 		return self.courses[term]



# def calculateConflicts(self):
# 	def hasConflict(c1, c2):
# 		res = 0
# 		for i in c1.courseStudents:
# 			if i in c2.courseStudents:
# 				res += 1
# 		return res   
# 	res = [[hasConflict(c,course) for c in self.courses ] for course in self.courses]
# 	return res

# def calculateTR45(self, cost):
# 	return [[self.conflicts[i][j]*cost for j in range(self.coursesNum)] for i in range(self.coursesNum)]

# def calculateTR2(self, minCost, maxCost, timeNum):
	
# 	costPlus = (maxCost-minCost)*1.0/timeNum
# 	tmp = []
# 	for i in range(timeNum):
# 		tmp.append(maxCost-(i*costPlus))

# 	return [tmp for i in xrange(self.coursesNum)]

# def calculateTR6(self):
# 	"""course-place"""
# 	return [ [True for i in range(n_o_places)] for j in self.courses]

# def calculateTR1(self):
# 	"""time-place"""
# 	return [ [True for i in range(n_o_places)] for j in range(n_o_times)]

# def getCourseName(self, index):
# 	return self.coursesNames[index]



def getStudentCourses(st): # courses of a student
	""" st: student ID (String or int) """
	pass

def getCourseIntersections(c1, c2): # number of students in both course
	pass

def addChart(self, path):
	pass

def profConflict(c1, c2): # same prof ?
	""" True in condition of same prof """
	pass

def chartConflict(c1, c2):
	""" True in condition of conflict """
	# if have conflicts in charts!
	pass

def in_day_conflict(c1, c2):
	pass
	# have conflict that has not to be in one day

def continues_day_conflict(c1, c2):
	pass
	# has conflict that cannot be in following days

def continues_time_conflict(c1, c2):
	pass
	# connat be in following time

def same_time_conflict(c1, c2):
	pass
	# cannot be in same time!

def getTime(index):
	pass # printable time!