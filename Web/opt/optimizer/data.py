# -*- coding: utf-8 -*-
import xlrd
from models import Project, Teacher, Time, Constraint, Student, Course
import xlrd


in_continues_day = 100
in_day_cost = 100000

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

def set_course_time(crid, time):
	course = Course.objects.get(id=crid)
	# time = Time.objects.get(id=tid)
	course.time = time
	course.save()

def times(prid):
	pr = Project.objects.get(id=prid)
	return Time.objects.filter(project=pr)

def times_num(prid):
	pr  = Project.objects.get(id=prid)
	times = Time.objects.filter(project=pr)
	return len(times)

# are times in one day
def in_day_time(time1, time2):
	# time1 = Time.objects.get(id=t1)
	# time2 = Time.objects.get(id=t2)
	if time1.d == time2.d and time1.m == time2.m:
		return True
	return False

msizes = {1:31, 2:31, 3:31, 4:31, 5:31, 6:31, 7:30, 8:30, 9:30, 10:30, 11:30, 12:30}

# are time in continues day
def continues_day_time(time1, time2):
	# time1 = Time.objects.get(id=t1)
	# time2 = Time.objects.get(id=t2)
	if time1.m == time2.m:
		if abs(time1.d - time2.d) == 1:
			return True
	# not in same month
	if abs(time1.m - time2.m) == 1:
		# 1 bozorgtare, 2 kochiktare!
		time1, time2 = time1, time2 if time1.m - time2.m == 1 else time2, time1
		if time1.d == 1 and time2.d == msizes[time2.m]:
			return True
	return False

# are time in continues time, next hour!
def continues_time_time(time1, time2):
	if in_day_time(time1, time2):
		# time1 = Time.objects.get(id=t1)
		# time2 = Time.objects.get(id=t2)
		if abs(time1.h - time2.h) == 3:
			return True
	return False

def courses_num(prid):
	pr = Project.objects.get(id=prid)
	cr = Course.objects.filter(project=pr)
	return len(cr)


def courses(prid):
	pr = Project.objects.get(id=prid)
	return Course.objects.filter(project=pr)

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

def students_conflict(c1, c2):
	course1 = Course.objects.get(id=c1)
	course2 = Course.objects.get(id=c2)
	return len(set(course1.students.all()).intersection(course2.students.all()))
		
def in_day_conflict(c1, c2):
	pass
	# have conflict that has not to be in one day

def continues_day_conflict(c1, c2):
	pass
	# has conflict that cannot be in following days

def continues_time_conflict(c1, c2):
	pass
	# connat be in following time

def has_same_time_conflict(c1, c2):
	course1 = Course.objects.get(id=c1)
	course2 = Course.objects.get(id=c2)
	
	if course1.teacher and course2.teacher and course1.teacher.id == course2.teacher.id:
		return True
	if set(course1.students.all()).intersection(course2.students.all()):
		return True
	# check in database to see if there is any conflict!
	return False
	
	# cannot be in same time!

def getTime(index):
	pass # printable time!