import xlrd

book = xlrd.open_workbook('Book3.xlsx')
sheet = book.sheet_by_index(0)

course = sheet.col_values(0)
course = [int(x) for x in course]
times = sheet.col_values(2)
for index in xrange(len(times)):
	t1, t2 = times[index].split('-')
	print int(t1), int(t2)

	times[index] = int(t1)*3 + int(t2)

result1 = zip(course, times)
