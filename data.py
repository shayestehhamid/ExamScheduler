import xlrd

n_o_times = 36
n_o_places = 20

class Course:
	def __init__(self, courseID, courseProf, courseStudents):
		self.courseID = courseID
		self.courseProf = courseProf
		self.courseStudents = courseStudents

class Place:
	def __init__(self, placeID, capacity):
		self.placeID = placeID
		capacity = capacity

class Data:

	def open_file(self, path):
		book = xlrd.open_workbook(path)
		self.coursesNum = book.nsheets
		self.coursesNames = book.sheet_names()
		
		for i in range(self.coursesNum):
			thisSheet = book.sheet_by_index(i)		
			#print thisSheet.col_values(0)
			cs = thisSheet.col_values(0)
			self.courses.append(Course(i, "", cs))
			for st in cs:
				try:
					self.students[int(st)].append(i)
				except:
					self.students[int(st)] = [i]
		# print self.students

	def calculateConflicts(self):
		def hasConflict(c1, c2):
			res = 0
			for i in c1.courseStudents:
				if i in c2.courseStudents:
					res += 1
			return res   
		res = [[ hasConflict(c,course) for c in self.courses ] for course in self.courses]
		return res

	def calculateTR45(self, cost):
		return [[self.conflicts[i][j]*cost for j in range(self.coursesNum)] for i in range(self.coursesNum)]

	def calculateTR2(self, minCost, maxCost, timeNum):
		
		costPlus = (maxCost-minCost)*1.0/timeNum
		tmp = []
		for i in range(timeNum):
			tmp.append(maxCost-(i*costPlus))

		return [tmp for i in xrange(self.coursesNum)]

	def calculateTR6(self):
		"""course-place"""
		return [ [True for i in range(n_o_places)] for j in self.courses]

	def calculateTR1(self):
		"""time-place"""
		return [ [True for i in range(n_o_places)] for j in range(n_o_times)]

	def getCourseName(self, index):
		return self.coursesNames[index]

	def getTime(self, index):
		return str(index/4 + 13), str((index%4)*3 + 8)

	def getStudentCourses(self, st):
		""" st: student ID (String or int) """
		return self.students[int(st)]

	def getCourseIntersections(self, c1, c2):
		return self.courses[c1].intersection(self.courses[c1])

	def __init__(self, path):
		self.students = {}
		self.courses = []
		self.open_file(path)
		self.conflicts = self.calculateConflicts()
		self.TR4 = self.calculateTR45(100*1000)
		self.TR5 = self.calculateTR45(5000*1000)
		# print 'start4', self.TR4[0], 'end'
		# print 'start5', self.TR5[0], 'end'
		self.TR2 = self.calculateTR2(7*1000, 10*1000, n_o_times)
		self.places = []
		self.TR1 = self.calculateTR1()
		self.TR6 = self.calculateTR6()
		self.n_o_times = 40

#a = Data("Book1.xlsx")
