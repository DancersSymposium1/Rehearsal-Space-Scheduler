import sys
import os

# download "Timesheet" & "Rehearsal-Space-Scheduler" repos into same directory
sys.path.append(os.path.abspath("../Timesheet"))
from timesheet_from_csv import *
from Classes import *

TIMESHEET_FOLDER = "timesheets/"

def run():
    ts = dict() # dictionary of timesheets
    for filename in os.listdir(TIMESHEET_FOLDER.strip("/")):
        T = timesheet_from_csv(TIMESHEET_FOLDER + filename)
        ts[T.name] = T

    
run()
