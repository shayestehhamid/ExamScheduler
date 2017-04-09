from pulp import *
import data
data = data.Data("Book1.xlsx")

problem = LpProblem('Project', LpMinimize)

n_o_places = 10
n_o_time = 10




########################
# TV2
# course * course
var_in_day_binary = [[] _ for i in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
	for j in xrange(data.coursesNum):
		name = ",".join(["TV2cc", str(i), str(j)])
		var = LpVariable(name, 0, 1, LpInteger)
		var_in_day_binary[i].append(var)
# TV3
# course * course
var_continues = [[] _ for i in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
	for j in xrange(data.coursesNum):
		name = ",".join(["TV3cc", str(i), str(j)])
		var = LpVariable(name, 0, 1, LpInteger)
		var_continues[i].append(var)
# TV4
#course * time * places
var_cr_time_places = [[[] for j in xrange(n_o_places)] for _ in xrange(data.coursesNum)]
for i in xrange(data.coursesNum):
	for j in xrange(n_o_places):
		for k in xrange(n_o_time):
			name = ','.join(["TV4cpt", str(i), str(j), str(k)]) # course, place, time
			var = LpVariable(name, 0, 1, LpInteger)
			var_cr_time_places[i][j].append(var)
###########################

# const 2
# check for intersections!

for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:
			
			for time in xrange(n_o_time):
				const = []
				for place in xrange(n_o_places):
					const.append(var_cr_time_places[c1][place][time])
					const.append(var_cr_time_places[c2][place][time])
				problem += lpSum(const) <= 1

# const 3
# constrains for AA table, being after each other!
for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:			
			for time in xrange(n_o_time):
				const = []
				for place in xrange(n_o_places):
					const.append(var_cr_time_places[c1][place][time])
					const.append(var_cr_time_places[c2][place][time])
				problem += lpSum(const) <= 2*var_continues[c1][c2]

# const 4
# constrains for AD table, being in one day
for c1 in xrange(data.coursesNum):
	for c2 in xrange(data.coursesNum):
		if data.conflicts[c1][c2]:			
			for time in xrange(n_o_time):
				const = []
				for place in xrange(n_o_places):
					const.append(var_cr_time_places[c1][place][time])
					const.append(var_cr_time_places[c2][place][time])
				problem += lpSum(const) <= 2*var_in_day_binary[c1][c2]

# const 5
# sigma on time, sigma on places, for a specific course = 1, get sure time and room has been assigned
for course in xrange(data.coursesNum):
	const = []
	for time in xrange(n_o_time):
		for place in xrange(n_o_places):
			const.append(var_cr_time_places[course][place][time])
	problem += lpSum(const) = 1

# const 6
# get sure the place is free in the time
# not exists for now!!!
# love our department!

# const 7
# in a place, a time, only one exam is held ( or less )
for time in xrange(n_o_time):
	for place in xrange(n_o_places):
		const = []
		for course in xrange(data.coursesNum):
			const.append(var_cr_time_places[course][place][time])
		problem += lpSum(const) <= 1


############################
#objective!
for course in xrange(data.coursesNum):
	for course in xrange(data.coursesNum):
		problem += var_in_day_binary[course][course]*data.TR4[course][course]
		problem += var_continues[course][course]*data.TR5[course][course]
# zarb in_day ba element moshabeh
# zarb continues ba element moshabeh
# zarb coursetime, dar hanizeie time

########################



problem.solve()

