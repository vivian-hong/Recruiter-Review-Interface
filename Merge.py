import csv
import os

def merge(filename, fileList):

	if not os.path.exists("Desktop/Reports"):
	os.makedirs("Desktop/Reports")

	with open('Desktop/Reports/' + filename, 'w') as csvOutput:
		writer = csv.writer(csvOutput) # merged list will end up here
		writer.writerow(['Name', 'Activity', 'Candidate', 'Job', 'Creation time']) 
		for x in range (0, len(fileList)):
			with open (os.path.expanduser(fileList[x]), 'r') as csvInput:
				reader = csv.reader(csvInput)
				if next(reader) != ['Name', 'Activity', 'Candidate', 'Job', 'Creation time']:
					#os.remove(filename)
					return 0
				for row in reader:
					writer.writerow(row)

