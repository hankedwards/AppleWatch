# August 2017 - 
# Simple Python script to parse Apple Health Values out of the export.xml into a pipe delimited txt file
# The basis of this script is from Kristian Desch  I modified the code to pull out the swim data that I wanted
# to analyze.  This script is used to pull the data and create an extracted file which I then analyse via
# a Jupyter notebook file

# I will provide more comments and notes later

import re, sys, os, datetime
from datetime import datetime, timedelta

# Assumes you run the script in same location as the exported data
healthlog = open("export.xml","r")

# Open Parsed results file
healthresults = open("AppleHealthData3.txt","w")

#Create Header row 
healthresults.write("Date|Time|Laps|Distance|Pre_date|avg100\n")

# Init counter
count = 0

#Init Health type value dictionary

valdic = {}
sourcedic = {}

#determine number of lines in export.xml
num_lines = sum(1 for line in open('export.xml'))
print("The total number of lines is ", num_lines) 

FMT = '%Y-%m-%d %H:%M:%S'
totaldist = 0.0
totalmin = 0.0
# set the initial value to the first date in the file.  This prevents extra logic
pre_date = "2017-04-02"


for line in healthlog:
    if re.search(r'<Record type=', line):
        recordtype = re.search(r"<Record type=\"\S+\"",line)
        recordtypeval = recordtype.group()
        # print(recordtype)
        
        # Add record types to value dictionary
        valdic[recordtypeval[38:-1]] = count
        
        #get source of value
        sourceName =re.search(r"sourceName\S\S\S+\s+\S+",line)
        sourceNameval = sourceName.group()
        sourcedic[sourceNameval[12:]]= count
        
       
                
        #Get end date/time of data collection
        datetime2 = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
        datetime2val = datetime2.group()
    
        # Output results to file
        #minssec = 0.0

        if "DistanceSwim" in recordtypeval[38:-1] :
            starttime = re.search(r"startDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
            endtime = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
            tdelta = datetime.strptime(endtime.group()[9:], FMT) - datetime.strptime(starttime.group()[11:], FMT)
            sec_dif = str((datetime.strptime(endtime.group()[9:], FMT) - datetime.strptime(starttime.group()[11:], FMT)))
            # Obtain the total seconds
            delta_in_seconds = str(tdelta.total_seconds())
            healthdata = re.search(r"value\S\S\w+",line)
            healthdataval = healthdata.group()
            hvalue =int(healthdataval[7:9]) 
            totalmin = totalmin + float(delta_in_seconds)
            totaldist = totaldist + hvalue
            # Calculate the totals by day and write out record for the day
            
            if pre_date != datetime2val[9:19]:
                avg100 = f'{((totalmin/(totaldist/100))/60):.2f}'
                laps = int(totaldist/25)
                healthresults.write(str(pre_date + "|" + str(totalmin) + "|" + str(laps) + "|" + str(totaldist) + "|" 
                + pre_date + "|"+ str(avg100) + "\n"))
                totalmin = 0.0
                totaldist = 0.0
                pre_date = datetime2val[9:19]
                count = count +1     
            #if count >= 200:
            #   break

        #print progress hash
        #if count % 100000 == 0:
            #print ('{counts} of {nums}'.format(counts=count, nums=num_lines))
sys.stdout.flush()

#Close files
healthlog.close()
healthresults.close()

#print values parsed
print ("Health Values Captured")
for key in valdic:
	print(key)
	
print("device Sources of Health data")
for key in sourcedic:
	print(key)
                        