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

class Chart:

	def openFile(self, path):
		self.courseToTerm = {}
		book = xlrd.open_workbook(path)
		sheet = book.sheet_by_index(0)
		self.courses = []
		for i in xrange(8):
			col = sheet.col_values(i)
			self.courses.append(col)
			for j in col:
				self.courseToTerm[j] = i

	def courseTerm(self, courseID):
		return self.courseToTerm[courseID] if courseID in self.courseToTerm else []

	def termCourses(self, term):
		return self.courses[term]

	def __init__(self, path):
		self.openFile(path)
		

class Data:

	def openFile(self, path):
		book = xlrd.open_workbook(path)
		self.coursesNum = book.nsheets
		self.coursesNames = book.sheet_names()
		
		for i in range(self.coursesNum):
			thisSheet = book.sheet_by_index(i)		
			#print thisSheet.col_values(0)
			cs = thisSheet.col_values(0)
			self.courses.append(Course(i, int(thisSheet.col_values(1)[0]), cs))
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
		return str(index/4 + 13), str(index%4*3 + 8)

	def getStudentCourses(self, st):
		""" st: student ID (String or int) """
		return self.students[int(st)]

	def getCourseIntersections(self, c1, c2):
		return set(self.courses[c1].courseStudents).intersection(set(self.courses[c2].courseStudents))

	def addChart(self, path):
		self.charts.append(Chart(path))

	def profConflict(self, c1, c2):
		""" True in condition of same prof """
		return self.courses[c1].courseProf == self.courses[c2].courseProf

	def chartConflict(self, c1, c2):
		""" True in condition of conflict """
		for chart in self.charts:
			if c1 in chart.courseToTerm and c2 in chart.courseToTerm and chart.courseToTerm[c1] == chart.courseToTerm[c2]:
				return True
		return False

	def __init__(self, path):
		self.students = {}
		self.courses = []
		self.charts = []
		self.openFile(path)
		self.conflicts = self.calculateConflicts()
		self.TR4 = self.calculateTR45(1000*1000*1000*1000)
		self.TR5 = self.calculateTR45(1000*1000)
		# print 'start4', self.TR4[0], 'end'
		# print 'start5', self.TR5[0], 'end'
		self.TR2 = self.calculateTR2(7*1000, 10*1000, n_o_times)
		self.places = []
		self.TR1 = self.calculateTR1()
		self.TR6 = self.calculateTR6()
		self.addChart("chartNarm.xlsx")
		self.addChart("chartSakht.xlsx")

data = Data("Book1.xlsx")

# mm = 10
# mx = 0
# ss = 0
# for x in a.students:
# 	mm = min(mm, len(a.students[x]))
# 	mx = max(mx, len(a.students[x]))
# 	ss += len(a.students[x])

# print mm, mx, ss, ss/float(len(a.students))


import xlrd

book = xlrd.open_workbook('res1Final.xlsx')
sheet = book.sheet_by_index(0)

course = sheet.col_values(1)
course = [int(x) for x in course]
times = sheet.col_values(2)
days = sheet.col_values(3)
slot_time = []
for i in xrange(len(times)):
	t = int((int(times[i])-8)/3) + int(int(days[i])-13)*4
	slot_time.append(t)

	
result1 = zip(course, slot_time)
n_days_conf = 0
n_serial_conf = 0
two_serial_day = 0

any_conf = 0

for index1 in xrange(len(result1)):
	for index2 in xrange(len(result1)):
		if index1 < index2:
			c1, t1 = result1[index1]
			c2, t2 = result1[index2]
			# print c1, type(c2), t1, type(t2)
			if t1 == t2:
				any_conf += data.conflicts[c1][c2]
			if t1/4 == t2/4 and abs(t1-t2)==1:
				n_serial_conf += data.conflicts[c1][c2]
			if t1/4 == t2/4:
				n_days_conf += data.conflicts[c1][c2]
			if abs(t1/4 - t2/4) == 1:
				# print index1, index2
				two_serial_day += data.conflicts[index1][index2]

print any_conf, "conflict,!"
print n_serial_conf , "time serial"
print n_days_conf, "in day"
print two_serial_day, "two day serial"
print data.getCourseIntersections(12, 8)
print data.conflicts[20][24]
print data.getCourseIntersections(0, 7)