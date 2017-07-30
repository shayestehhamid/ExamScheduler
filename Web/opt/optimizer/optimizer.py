from pulp import *
import data as Data
import matplotlib.pyplot as plt


removed_course = -1


import time



start_time = time.time()
########################
def optimize(projectid):

	problem = LpProblem('Project', LpMinimize)
	courses = Data.courses(projectid)
	dict_courses = {}
	for i in xrange(Data.courses_num(projectid)):
		dict_courses[i] = courses[i].id


	# TV2
	# course * course
	# variables to allowed to courses be in same day
	var_in_day_binary = [[] for _ in xrange(Data.courses_num(projectid))]
	for i in xrange(Data.courses_num(projectid)):
		for j in xrange(Data.courses_num(projectid)):
			name = ",".join(["TV2cc", str(i), str(j)])
			var = LpVariable(name, 0, 1, LpInteger)
			var_in_day_binary[i].append(var)

	# TV3
	# course * course

	# variables to allowed to courses be in continues days.
	var_continues = [[] for i in xrange(Data.courses_num(projectid))]
	for i in xrange(Data.courses_num(projectid)):
		for j in xrange(Data.courses_num(projectid)):
			name = ",".join(["TV3cc", str(i), str(j)])
			var = LpVariable(name, 0, 1, LpInteger)
			var_continues[i].append(var)


	# if a course is taken in a time 1, rest if 0
	# TV4
	#course * time
	var_cr_time = [[] for _ in xrange(Data.courses_num(projectid))]
	for i in xrange(Data.courses_num(projectid)):
			for k in xrange(Data.times_num(projectid)):
				name = ','.join(["TV4cpt", str(i), str(k)]) # course, place, time
				var = LpVariable(name, 0, 1, LpInteger)
				var_cr_time[i].append(var)
	###########################

	# const 1
	# check for intersections!
	# if two courses has confilct (any reason) 
	# including professors!
	for c1 in xrange(Data.courses_num(projectid)):
		for c2 in xrange(Data.courses_num(projectid)):	
			if c1 == c2 or c1 > c2:
				continue
			if Data.has_same_time_conflict(dict_courses[c1], dict_courses[c2]):  
				for time in xrange(Data.times_num(projectid)):
					const = []
					
					const.append(var_cr_time[c1][time])
					const.append(var_cr_time[c2][time])
					problem += lpSum(const) <= 1

	print "73", Data.courses_num(projectid)
	times = Data.times(projectid)
	dict_times = {} # give index and get id!
	for i in xrange(len(times)):
		dict_times[i] = times[i]

	cn_times = []

	for t1 in xrange(Data.times_num(projectid)):
					for t2 in xrange(Data.times_num(projectid)):
						# print c1, c2, t1, t2, 'in 94'
						if Data.continues_day_time(dict_times[t1], dict_times[t2]):
							cn_times.append((t1, t2))
		

	# being in two neighbor days! # emroz va farda
	for c1 in xrange(Data.courses_num(projectid)):
		for c2 in xrange(Data.courses_num(projectid)):
			if Data.students_conflict(dict_courses[c1] ,dict_courses[c2]) and c1 < c2:			
				for t1, t2 in cn_times:
					# print c1, c2, t1, t2, 'in 94'
					if Data.continues_day_time(dict_times[t1], dict_times[t2]):
						const = []
					
						const.append(var_cr_time[c1][t1])
						const.append(var_cr_time[c2][t2])
						problem += lpSum(const) <= (1 + var_continues[c1][c2])


	print "94", Data.courses_num(projectid)

	# next hour!

	cont_times = []
	for t1 in xrange(Data.times_num(projectid)):
					for t2 in xrange(Data.times_num(projectid)):
						if Data.continues_time_time(dict_times[t1], dict_times[t2]):
							cont_times.append((t1, t2))

	# constrains for AA table, being after each other!
	for c1 in xrange(Data.courses_num(projectid)):
		for c2 in xrange(Data.courses_num(projectid)):
			if Data.students_conflict(dict_courses[c1] ,dict_courses[c2]) and c1 < c2:			
				for t1, t2 in cont_times:
					const = []
				
					const.append(var_cr_time[c1][t1])
					const.append(var_cr_time[c2][t2])
					problem += lpSum(const) <= 1 

	# const 4
	print "112", Data.courses_num(projectid)

	in_day_time_list = []
	for t1 in xrange(Data.times_num(projectid)):
					for t2 in xrange(Data.times_num(projectid)):
						if not Data.continues_time_time(dict_times[t1], dict_times[t2]) \
								and Data.in_day_time(dict_times[t1], dict_times[t2]):
							in_day_time_list.append((t1, t2))

	# same day, not following time
	# constrains for AD table, being in one day
	for c1 in xrange(Data.courses_num(projectid)):
		for c2 in xrange(Data.courses_num(projectid)):
			if Data.students_conflict(dict_courses[c1] ,dict_courses[c2]):			
				for t1, t2 in in_day_time_list:
					const = []
					
					const.append(var_cr_time[c1][t1])
					const.append(var_cr_time[c2][t2])
					problem += lpSum(const) <= (1 + var_in_day_binary[c1][c2])

	print "129", Data.courses_num(projectid)
	# no two course of same semester are in same day!
	# will be handle by conflicts in database!

	
	# const 5
	# time is surely assigned for course

	for course in xrange(Data.courses_num(projectid)):
		const = []
		for time in xrange(Data.times_num(projectid)):	
			const.append(var_cr_time[course][time])
		problem += lpSum(const) == 1


	print "144", Data.courses_num(projectid)
	print "objectivE!"

	############################
	#objective!
	lst = []
	lst2 = []
	for course1 in xrange(Data.courses_num(projectid)):
		for course2 in xrange(Data.courses_num(projectid)):
			if course1 < course2:
				lst.append(var_in_day_binary[course1][course2]*
						Data.students_conflict(dict_courses[course1], dict_courses[course2])*
						Data.in_day_cost)			
	 			lst2.append(var_continues[course1][course2]*
	 					Data.students_conflict(dict_courses[course1], dict_courses[course2])*
						Data.in_continues_day)

	problem += lpSum(lst)
	# print "l;ksdfa"
	# print problem.objective
	problem.writeLP("problem.lp")
	status = problem.solve()	
	print LpStatus[status]
	print "problem solved!"
	for course in xrange(Data.courses_num(projectid)):
		for time in xrange(Data.times_num(projectid)):
			if value(var_cr_time[course][time]) == 1:
				Data.set_course_time(dict_courses[course], dict_times[time])				

'''
import xlsxwriter
workbook = xlsxwriter.Workbook('res1.xlsx')
worksheet = workbook.add_worksheet()


result= []


row = 0
for course in xrange(data.coursesNum):
	for time in xrange(n_o_time):
		if value(var_cr_time[course][time]) == 1:
			worksheet.write(row, 0, data.getCourseName(course))
			worksheet.write(row, 1, data.getTime(time)[0])
			worksheet.write(row, 2, data.getTime(time)[1])
			
			worksheet.write(row, 4, str(data.charts[0].courseTerm(course)))
			worksheet.write(row, 5, str(data.charts[1].courseTerm(course)))
			result.append((course, time))
			row += 1


workbook.close()

n_days_conf = 0
n_serial_conf = 0
two_serial_day = 0

for index1 in xrange(len(result)):
	for index2 in xrange(len(result)):
		if index1 < index2:
			c1, t1 = result[index1]
			c2, t2 = result[index2]

			if t1/4 == t2/4 and abs(t1-t2)==1:
				n_serial_conf += data.conflicts[c1][c2]
				
			elif t1/4 == t2/4:
				n_days_conf += data.conflicts[c1][c2]
				# print data.getCourseName(c1), data.getCourseName(c2), data.conflicts[c1][c2]
				
			if abs(t1/4 - t2/4) == 1:
				# print index1, index2
				two_serial_day += data.conflicts[index1][index2]


print "male ma bashe"
print n_days_conf, "in one day conf"
print two_serial_day, "two serial days!"
print n_o_time, " number of times"



# import time
# finish_time = time.time()


# print "time: ", finish_time - start_time
# zarb in_day ba element moshabeh
# zarb continues ba element moshabeh
# vase inke bere akhara hamash!
# for course in xrange(data.coursesNum):

# 	for time in xrange(n_o_time):
# 			problem += var_cr_time[course][time]*data.TR2[course][time]
# zarb coursetime, dar hanizeie time

'''
