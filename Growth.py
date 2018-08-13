import csv
import os
import pandas as pd
import datetime
import Format

def getGrowth(final, today):

	with open('Desktop/Reports/%s WorkableJuneToDate.csv' %today, 'w') as csvGrowth:
		growth = csv.writer(csvGrowth)
		recruiter = "No One"
		iCount = 0
		sCount = 0
		week = 0
		year = 0

		with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'r') as parsedReport:
			report = csv.reader(parsedReport)
			next(report) # header
			sortedList = sorted(report, key=lambda row: (row[0], row[4])) # sorting by recruiter, time

			first = sortedList[0]
			recruiter = first[0]
			if (first[1] == "Moved to stage Screened"):
				iCount += 1
			else:
				sCount += 1		
			date = first[4].split('-')
			day = date[2].split('T')
			week = datetime.date(int(date[0]), int(date[1]), int(day[0])).isocalendar()[1]
			year = date[0]

			for row in sortedList[1:len(sortedList)]:
				if row[0] == " ":
					calc = str(year) + "-W" + str(week)
					weekdate = str(datetime.datetime.strptime(calc + '-1', "%Y-W%W-%w")).split(" ")[0]

					growth.writerow([recruiter, weekdate, iCount, sCount])
					break
				elif row[0] == recruiter: # checking if recording for same recruiter
					current_date = row[4].split('-')
					current_day = current_date[2].split('T')
					current_week = datetime.date(int(current_date[0]), int(current_date[1]), int(current_day[0])).isocalendar()[1]
					if current_week == week: # checking if recording for same week
						if (row[1] == "Moved to stage Screened"): # interview
							iCount += 1
						if row[1] == "Moved to stage Interview": # send-out
							sCount +=1
					else:
						calc = str(year) + "-W" + str(week)
						weekdate = str(datetime.datetime.strptime(calc + '-1', "%Y-W%W-%w")).split(" ")[0]

						growth.writerow([recruiter, weekdate, iCount, sCount])
						current_date = row[4].split('-')
						current_day = current_date[2].split('T')
						week = datetime.date(int(current_date[0]), int(current_date[1]), int(current_day[0])).isocalendar()[1]
						if (row[1] == "Moved to stage Screened"):
							iCount = 1
							sCount = 0
						else:
							iCount = 0
							sCount = 1
				else:
					calc = str(year) + "-W" + str(week)
					weekdate = str(datetime.datetime.strptime(calc + '-1', "%Y-W%W-%w")).split(" ")[0]

					growth.writerow([recruiter, weekdate, iCount, sCount])
					recruiter = row[0]
					current_date = row[4].split('-')
					current_day = current_date[2].split('T')
					week = datetime.date(int(current_date[0]), int(current_date[1]), int(current_day[0])).isocalendar()[1]
					if (row[1] == "Moved to stage Screened"):
						iCount = 1
						sCount = 0
					else:
						iCount = 0
						sCount = 1	
			parsedReport.close()	
			calc = str(year) + "-W" + str(week)
			weekdate = str(datetime.datetime.strptime(calc + '-1', "%Y-W%W-%w")).split(" ")[0]

			growth.writerow([recruiter, weekdate, iCount, sCount])	
			csvGrowth.close()
			reformatGrowth(final, today)

def reformatGrowth(final, today):

	filename = final.split("/")[len(final.split("/")) - 1]

	with open('Desktop/Reports/%s WorkableJuneToDate.csv' %today, 'r') as csvGrowth:
		reader = csv.reader(csvGrowth)
		sortedList = sorted(reader, key=lambda row: (row[1])) # sorting list
	csvGrowth.close()
	
	weekList = ["Recruiter"]
	for row in sortedList:
		if row[1] != weekList[len(weekList)-1]:
			weekList.append(str(row[1]))
	numRows = len(sortedList) - 1
	header = []
	for i in range (0, len(weekList) - 1):
		header.append(weekList[i])
	header.append(weekList[i+1])
	finalList = [header]
	recruiter = sortedList[0][0]
	finished = False
	lineCounter = 0
	recruiterList = []
	while not finished:
		current  = [recruiter]
		for i in range (1, len(weekList)):
			found = False
			for j in range (0, len(sortedList)):

				if recruiter == sortedList[j][0] and weekList[i] == sortedList[j][1]:

					current.append(sortedList[j][2] + "|" + sortedList[j][3])
					lineCounter += 1
					found = True
					break
			if j == len(sortedList) - 1 and found == False:

				current.append("0|0")
		finalList.append(current)
		recruiterList.append(recruiter)

		for row in sortedList:
			if row[0] not in recruiterList:
				recruiter = row[0]
				break

		if lineCounter == len(sortedList):
			finished = True
	with open('Desktop/Reports/%s WorkableJuneToDate.csv' %today, 'w') as csvGrowth:
		growth = csv.writer(csvGrowth)
		for row in finalList:
			growth.writerow(row) # writing sorted list

		initSplit = filename.split("_")
		secSplit = initSplit[3].split(".")
		fDate = initSplit[2] # "first date" - start date
		sDate = secSplit[0] # "second date" - end date

		reportRange  = "Activity Dates: " + str(fDate) + "-" + str(sDate)
		date = "Date Ran: " + str(today)

		growth.writerow(' ')
		growth.writerow(['WorkableJuneToDate', reportRange, date])
		csvGrowth.close()

		Format.format('Desktop/Reports/' + today + ' WorkableJuneToDate.csv')