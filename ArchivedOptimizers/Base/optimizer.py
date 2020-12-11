from pulp import *
import data
import matplotlib.pyplot as plt

data = data.Data("Book1.xlsx")

removed_course = -1

# for c1 in xrange(data.coursesNum):
# 	data.conflicts[c1][removed_course] = 0
# 	data.conflicts[removed_course][c1] = 0

problem = LpProblem('Project', LpMinimize)

n_o_places = 20
n_o_time = 72


import time

start_time = time.time()
########################



# TV2
# course * course
var_in_day_binary = [[] for _ in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
	for j in xrange(data.coursesNum):
		name = ",".join(["TV2cc", str(i), str(j)])
		var = LpVariable(name, 0, 1, LpInteger)
		var_in_day_binary[i].append(var)

# TV3
# course * course


var_continues = [[] for i in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
	for j in xrange(data.coursesNum):
		name = ",".join(["TV3cc", str(i), str(j)])
		var = LpVariable(name, 0, 1, LpInteger)
		var_continues[i].append(var)


# TV4
#course * time * places
var_cr_time = [[] for _ in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
		for k in xrange(n_o_time):
			name = ','.join(["TV4cpt", str(i), str(k)]) # course, place, time
			var = LpVariable(name, 0, 1, LpInteger)
			var_cr_time[i].append(var)
###########################

# const 2
# check for intersections!

for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:
			if c1 == c2:
				continue
			for time in xrange(n_o_time):
				const = []
				
				const.append(var_cr_time[c1][time])
				const.append(var_cr_time[c2][time])
				problem += lpSum(const) <= 1

#another new const
#

times_serial_day = []
for time1 in xrange(n_o_time):
	for time2 in xrange(n_o_time):
		if abs(time1/4 - time2/4) == 1:
			times_serial_day.append((time1, time2))


for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:			
			for t1, t2 in times_serial_day:
				const = []
			
				const.append(var_cr_time[c1][t1])
				const.append(var_cr_time[c2][t2])
				problem += lpSum(const) <= 1 + var_continues[c1][c2]



# const 3
# constrains for AA table, being after each other!
times_serial = []
for time1 in xrange(n_o_time):
	for time2 in xrange(n_o_time):
		if time1/4 == time2/4 and abs(time1 - time2) == 1:
			times_serial.append((time1, time2))


for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:			
			for t1, t2 in times_serial:
				const = []
			
				const.append(var_cr_time[c1][t1])
				const.append(var_cr_time[c2][t2])
				problem += lpSum(const) <= 1 

# const 4
# constrains for AD table, being in one day
times_day = []
for time1 in xrange(n_o_time):
	for time2 in xrange(n_o_time):
		if time1/4 == time2/4 and abs(time1 - time2) > 1:
			times_day.append((time1, time2))

for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:			
			for t1, t2 in times_day:
				const = []
				
				const.append(var_cr_time[c1][t1])
				const.append(var_cr_time[c2][t2])
				problem += lpSum(const) <= var_in_day_binary[c1][c2] + 1

# no two course of same semester are in same day!
for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if c1 == c2:
			continue
		if c1 == removed_course or c2 == removed_course:
			continue
		if data.chartConflict(c1, c2):
			for t1 in xrange(n_o_time):
				for t2 in xrange(n_o_time):
					if t1/4 == t2/4:
						problem += var_cr_time[c1][t1] + var_cr_time[c2][t2] <= 1


# prof conflict

for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if c1 != c2:
			if c1 == removed_course or c2 == removed_course:
				continue
			if data.profConflict(c1, c2):
				for time in xrange(n_o_time):
					problem += var_cr_time[c1][time] + var_cr_time[c2][time] <= 1


# const 5
# sigma on time, sigma on places, for a specific course = 1, get sure time and room has been assigned
for course in xrange(data.coursesNum):
	const = []
	for time in xrange(n_o_time):	
		const.append(var_cr_time[course][time])
	problem += lpSum(const) == 1





# const 6
# get sure the place is free in the time
# not exists for now!!!
# love our department!

#get sure there is a place assign!
# get sure they do not have intersection one place, need an permission variable,.

# const 7
# in a place, a time, only one exam is held ( or less )


# solve this by permission!

#
# const = []
# for c1 in xrange(data.coursesNum):
# 	for c2 in xrange(data.coursesNum):
# 		if c1 < c2:
# 			const.append(var_in_day_binary[c1][c2]*data.conflicts[c1][c2])
# problem += lpSum(const) < 50

############################
#objective!
for course1 in xrange(data.coursesNum):
	for course2 in xrange(data.coursesNum):
		if course1 != course2:
			problem += var_in_day_binary[course1][course2]*data.TR4[course1][course2]
			problem += var_continues[course1][course2]*data.TR5[course1][course2]
			
# zarb in_day ba element moshabeh
# zarb continues ba element moshabeh
for course in xrange(data.coursesNum):
	for time in xrange(n_o_time):
			problem += var_cr_time[course][time]*data.TR2[course][time]
# zarb coursetime, dar hanizeie time

########################


print "problem created!"
status = problem.solve()
print LpStatus[status]
print "problem solved! part1"


import xlsxwriter
workbook = xlsxwriter.Workbook('res1.xlsx')
worksheet = workbook.add_worksheet()


result= []

# problem.writeLP("problem.lp")
row = 0
for course in xrange(data.coursesNum):
	for time in xrange(n_o_time):
		if value(var_cr_time[course][time]) == 1:
			worksheet.write(row, 0, data.getCourseName(course))
			worksheet.write(row, 1, data.getTime(time)[0])
			worksheet.write(row, 2, data.getTime(time)[1])
			reversed = 21 - int(data.getTime(time)[0]) + 13
			worksheet.write(row, 3, str(reversed))
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
				
			if abs(t1/4 - t2/4) == 1:
				# print index1, index2
				two_serial_day += data.conflicts[index1][index2]



print n_days_conf, "day conf"
# print n_serial_conf, "serial conf"
print two_serial_day, "two serial days!"
print n_o_time, "times"



# import networkx as nx
# G = nx.Graph()


# for i in xrange(data.coursesNum):
# 	G.add_node(i)


# for index1 in xrange(data.coursesNum):
# 	for index2 in xrange(data.coursesNum):
# 		if index1 < index2 and data.conflicts[index1][index2]:
# 			G.add_edge(index1, index2, weight=data.conflicts[index1][index2])



# pos = nx.circular_layout(G)
# nx.draw_networkx(G, pos)

# labels = {}
# for i in xrange(data.coursesNum):
# 	labels[i] = str(G.degree(i))+","+data.getCourseName(i)

# nx.draw_networkx_labels(G, pos, labels)

# plt.figure(1, figsize=(1000, 1000))
# plt.axis('off')
# plt.savefig("weighted_graph.png") # save as png
# plt.show() # displa




# import xlrd

# book = xlrd.open_workbook('Book3.xlsx')
# sheet = book.sheet_by_index(0)

# course = sheet.col_values(0)
# course = [int(x) for x in course]
# times = sheet.col_values(2)
# for index in xrange(len(times)):
# 	t1, t2 = times[index].split('-')
	

# 	times[index] = int(t1)*4 + int(t2)

# result1 = zip(course, times)

# n_days_conf = 0
# n_serial_conf = 0
# two_serial_day = 0

# for index1 in xrange(len(result1)):
# 	for index2 in xrange(len(result1)):
# 		if index1 < index2:
# 			c1, t1 = result1[index1]
# 			c2, t2 = result1[index2]
# 			if t1/4 == t2/4 and abs(t1-t2)==1:
# 				n_serial_conf += data.conflicts[c1][c2]
# 				continue
# 			if t1/4 == t2/4:
# 				n_days_conf += data.conflicts[c1][c2]
# 			if abs(t1/4 - t2/4) == 1:
# 				# print index1, index2
# 				two_serial_day += data.conflicts[index1][index2]

# print "male ouna bashe"
# print n_serial_conf
# print n_days_conf
# print two_serial_day

# import time
# finish_time = time.time()
# print "time: ", finish_time - start_time