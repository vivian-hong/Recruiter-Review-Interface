import csv
import os
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import datetime
import Format

def getSummary(final, today):

	filename = final.split("/")[len(final.split("/")) - 1]
	with open('Desktop/Reports/%s WorkableSummary.csv' %today, 'w') as csvSummary:
		summary = csv.writer(csvSummary)

		recruiter = "No One"
		iCount = 0
		sCount = 0
		bdays = calcBdays(filename)

		# creating categories
		summary.writerow(['Name', 'Number of Interviews', 'Number of Send-outs', 'Interview Average', 'Send-out Average', 'Number of Business Days'])
		
		with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'r') as parsedReport:
			report = csv.reader(parsedReport)
			first = next(report) # first line
			# first recruiter
			recruiter = first[0]
			if (first[1] == "Moved to stage Screened"):
				iCount += 1
			else:
				sCount += 1
			for row in report:
				if row[0] == " ":
					summary.writerow([recruiter, iCount, sCount, round(iCount/float(bdays), 1), round(sCount/float(bdays), 1), bdays])
					break
				elif row[0] == recruiter: # checking if recording for same recruiter
					if (row[1] == "Moved to stage Screened"): # interview
						iCount += 1
					if row[1] == "Moved to stage Interview": # send-out
						sCount +=1
				else: 
					# creating summary for one recruiter
					summary.writerow([recruiter, iCount, sCount, round(iCount/float(bdays), 1), round(sCount/float(bdays), 1), bdays])
					# starting new recruiter 
					recruiter = row[0]
					if row[1] == ("Moved to stage Screened"):
						iCount = 1
						sCount = 0
					if row[1] == "Moved to stage Interview":
						sCount =1
						iCount = 0
			parsedReport.close()

			summary.writerow([recruiter, iCount, sCount, round(iCount/float(bdays), 1), round(sCount/float(bdays), 1), bdays])
			initSplit = filename.split("_")
			secSplit = initSplit[3].split(".")
			fDate = initSplit[2] # "first date" - start date
			sDate = secSplit[0] # "second date" - end date

			reportRange  = "Activity Dates: " + str(fDate) + "-" + str(sDate)
			date = "Date Ran: " + str(today)

			summary.writerow(' ')
			summary.writerow(['Summary', reportRange, date])
		csvSummary.close()
		
		Format.format('Desktop/Reports/' + today + ' WorkableSummary.csv')

def calcBdays(filename):

	initSplit = filename.split("_")
	secSplit = initSplit[3].split(".")
	fDate = initSplit[2] # "first date" - start date
	sDate = secSplit[0] # "second date" - end date
	us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
	return pd.DatetimeIndex(start=fDate,end=sDate, freq=us_bd).shape[0]
