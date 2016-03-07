"""
    A timesheet is represented by a 2D list, with 2 1D list for the headers
"""

import string
import csv
from Classes import Timesheet

def timesheet_from_csv(TIMESHEET_FROM_CSV_FILE):
    timesheet_file = open(TIMESHEET_FROM_CSV_FILE, 'rU')
    timeHeader, L = [], []
    for i, line in enumerate(timesheet_file):
        columns = line.strip().split(',')
        if i == 0: 
            dayHeader = columns
            dayHeader.pop(0) #remove first entry
            dayHeader = filter(None, dayHeader)
            continue

        timeHead = columns.pop(0) #capture the time header
        timeHeader.append(timeHead)
        L.append(columns[:len(dayHeader)])

    return Timesheet(TIMESHEET_FROM_CSV_FILE.strip(".csv"), L, dayHeader, timeHeader)
