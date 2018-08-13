import csv
import os
import pandas as pd
import Format

def getJobProg(final, today):
	filename = final.split("/")[len(final.split("/")) - 1]

	with open('Desktop/Reports/%s WorkableJobProgress.csv' %today, 'w') as csvJobProgress:
		jobProgress = csv.writer(csvJobProgress)

		recruiter = "No One"
		job = "None"
		iCount = 0
		sCount = 0

		jobProgress.writerow(['Recruiter', 'Job', 'Number of Interviews', 'Number of Send-outs'])
		with open('Desktop/Reports/%s WorkableOverview.csv' %today, 'r') as parsedReport:
			report = csv.reader(parsedReport)
			first = next(report) # first line
			recruiter = first[0]
			job = first[3]
			if (first[1] == "Moved to stage Screened"):
				iCount += 1
			else:
				sCount += 1		
			for row in report:
				if row[0] == " ":
					jobProgress.writerow([recruiter, job, iCount, sCount])
					break
				elif row[0] == recruiter: # checking if recording for same recruiter
					if row[3] == job: # checking if recording for same job
						if (row[1] == "Moved to stage Screened"): # interview
							iCount += 1
						if row[1] == "Moved to stage Interview": # send-out
							sCount +=1
					else:
						jobProgress.writerow([recruiter, job, iCount, sCount])
						job = row[3]
						if (row[1] == "Moved to stage Screened"):
							iCount = 1
							sCount = 0
						else:
							iCount = 0
							sCount = 1
				else:
					jobProgress.writerow([recruiter, job, iCount, sCount])
					recruiter = row[0]
					job = row[3]
					if (row[1] == "Moved to stage Screened"):
						iCount = 1
						sCount = 0
					else:
						iCount = 0
						sCount = 1

			parsedReport.close()
			jobProgress.writerow([recruiter, job, iCount, sCount])
			initSplit = filename.split("_")
			secSplit = initSplit[3].split(".")
			fDate = initSplit[2] # "first date" - start date
			sDate = secSplit[0] # "second date" - end date

			reportRange  = "Activity Dates: " + str(fDate) + "-" + str(sDate)
			date = "Date Ran: " + str(today)

			jobProgress.writerow(' ')
			jobProgress.writerow(['Job Progress', reportRange, date])	
			csvJobProgress.close()	
			
			Format.format('Desktop/Reports/' + today + ' WorkableJobProgress.csv')
