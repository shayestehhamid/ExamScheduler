import xlrd

class Course:
	"""docstring for Course"""
	def __init__(self, courseID, courseProf, courseStudents):
		self.courseID = courseID
		self.courseProf = courseProf
		self.courseStudents = courseStudents


class Data:

	def open_file(self, path):
		"""
		Open and read an Excel file
		"""
		book = xlrd.open_workbook(path)
		self.coursesNum = book.nsheets
		for i in range(self.coursesNum):
			thisSheet = book.sheet_by_index(i)		
			#print thisSheet.col_values(0)
			self.courses.append(Course(i, "", thisSheet.col_values(0)))

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

	def calculateTR2(self, minCost, maxCost):
		costPlus = (maxCost-minCost)*1.0/self.coursesNum
		def helper():
			return True
		#a = [maxCost-c for c]
		return [[]]

	def __init__(self, path):
		self.courses = []
		self.open_file(path)
		self.conflicts = self.calculateConflicts()
		self.TR4 = self.calculateTR45(100*1000)
		self.TR5 = self.calculateTR45(1000*1000)
		self.TR2 = self.calculateTR2(10*1000)




a = Data("Book1.xlsx")
print a.conflicts[5][4]
print a.TR4[5][4]
print a.TR5[5][4]


