import csv
import os
import pandas as pd
import Format

def getData(filename):
	if not os.path.exists("Desktop/Reports"):
		os.makedirs("Desktop/Reports")
	with open (os.path.expanduser(filename), 'r') as csvInput:
		report = csv.reader(csvInput) # for reading in activity report
		today = str(pd.datetime.today().date())
		if next(report) == ['Name', 'Activity', 'Candidate', 'Job', 'Creation time']:
			data = list(report)
			with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'w') as csvOutput:
				outfile = csv.writer(csvOutput)
				trackInterviews(data, outfile)
				trackSendouts(data, outfile)
				csvOutput.close()
		sortOut(today)
		return today

# writes each interviewed candidate into parsed_report.csv
def trackInterviews(report, outfile):	

	for row in report:
		for field in row:
			if (field == "Moved to stage Screened"):
				# REMOVE BEFORE MAKING OPEN SOURCE
				if row[0] == "Antonio Sevilla Dieguez":
					row[0] = "Matt Vahle"
				elif row[0] == "Louis-David Mangin":
					row[0] = "Philip Astuto"
				#UP TO HERE
				outfile.writerow(row)

# writes each send-out candidate into parsed_report.csv
def trackSendouts(report, outfile):

	for row in report:
		for field in row:
			if field == "Moved to stage Interview":
				# REMOVE BEFORE MAKING OPEN SOURCE
				if row[0] == "Antonio Sevilla Dieguez":
					row[0] = "Matt Vahle"
				elif row[0] == "Louis-David Mangin":
					row[0] = "Philip Astuto"
				#UP TO HERE
				outfile.writerow(row)

def sortOut(today):

	with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'r') as csvOut:
		reader = csv.reader(csvOut)
		sortedList = sorted(reader, key=lambda row: (row[0], row[3], row[4])) # sorting list
	csvOut.close()
	with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'w') as csvOutput:
		outfile = csv.writer(csvOutput)
		for row in sortedList:
			outfile.writerow(row) # writing sorted list
	csvOut.close()


def overviewFooter(today, final):

	filename = final.split("/")[len(final.split("/")) - 1]

	with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'r') as csvOut:
		reader = csv.reader(csvOut)
		read = sorted(reader, key=lambda row: (row[0], row[3], row[4])) # sorting list
	csvOut.close()

	with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'w') as csvOutput:
		outfile = csv.writer(csvOutput)
		outfile.writerow(['Name', 'Activity', 'Candidate', 'Job', 'Creation time']) # writing categories
		for row in read:
			outfile.writerow(row) # writing sorted list
		initSplit = filename.split("_")
		secSplit = initSplit[3].split(".")
		fDate = initSplit[2] # "first date" - start date
		sDate = secSplit[0] # "second date" - end date

		reportRange  = "Activity Dates: " + str(fDate) + "-" + str(sDate)
		date = "Date Ran: " + str(today)

		outfile.writerow(' ')
		outfile.writerow(['Overview', reportRange, date])
		
	Format.format('Desktop/Reports/' + today + ' WorkableOverview.csv')
