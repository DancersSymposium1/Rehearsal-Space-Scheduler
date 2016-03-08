import sys
import os

# download "Timesheet" & "Rehearsal-Space-Scheduler" repos into same directory
sys.path.append(os.path.abspath("../Timesheet"))
from timesheet_from_csv import *
from Classes import *

TIMESHEET_FOLDER = "timesheets/"

def free_times(T): # returns all of the times free in the timesheet
    freeTimes = []
    for time in T.timeHeader:
        for day in T.dayHeader:
            if T.checkAvail(day, time): freeTimes.append((day, time))
    return freeTimes
            
def run():
    ts = dict() # dictionary of timesheets
    for filename in os.listdir(TIMESHEET_FOLDER.strip("/")):
        T = timesheet_from_csv(TIMESHEET_FOLDER + filename)
        print free_times(T)
        ts[T.name] = T
    
run()
