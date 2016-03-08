import sys
import os

# download "Timesheet" & "Rehearsal-Space-Scheduler" repos into same directory
sys.path.append(os.path.abspath("../Timesheet"))
from timesheet_from_csv import *
from Classes import *

TIMESHEET_FOLDER = "timesheets/"
day_order = { "Sunday" : 0, "Sun" : 0, "Su" : 0, "Sn" : 0,
              "Sun." : 0, "Su." : 0, "Sn." : 0,
              "Monday" : 1, "Mon" : 1, "Mo" : 1, "M" : 1,
              "Mon." : 1, "Mo." : 1, "M." : 1,
              "Tuesday" : 2, "Tues" : 2, "Tue" : 2, "Tu" : 2, "T" : 2,
              "Tues." : 2, "Tue." : 2, "Tu." : 2, "T." : 2,
              "Wednesday" : 3, "Wed" : 3, "We" : 3, "W" : 3,
              "Wed." : 3, "We." : 3, "W." : 3,
              "Thursday" : 4, "Thurs" : 4, "Thur" : 4, "Thu" : 4, "Th" : 4, "H" : 4,
              "Thurs." : 4, "Thur." : 4, "Thu." : 4, "Th." : 4, "H." : 4,
              "Friday" : 5, "Fri" : 5, "Fr" : 5, "F" : 5,
              "Fri." : 5, "Fr." : 5, "F." : 5,
              "Saturday" : 6, "Sat" : 6, "Sa" : 6,
              "Sat." : 6, "Sa." : 6 }

def dayHeader_add(ts, T):
    ts_dH_set = set(ts["dayHeader"])
    for day in T.dayHeader: ts_dH_set.add(day)
    ts_dH_list = []
    for i in xrange(len(ts_dH_set)): ts_dH_list.append(ts_dH_set.pop())
    ts["dayHeader"] = sorted(ts_dH_list, key=day_order.get)
    return ts

def timeHeader_redefine(ts, T):
    if len(ts["timeHeader_info"]) > 0: # check to redefine timeHeader boundaries
        if ts["timeHeader_info"][0] > T.startingTime:
            ts["timeHeader_info"][0] = T.startingTime
            ts["timeHeader_info"][3] = len(T.timeHeader)
        if ts["timeHeader_info"][1] != T.timeIncrement:
            print "timeIncrement has changed for %s, please proceed with caution" % T.name
            ts["timeHeader_info"][3] < len(T.timeHeader)
        if ts["timeHeader_info"][2] < T.endingTime:
            ts["timeHeader_info"][2] = T.endingTime
            ts["timeHeader_info"][3] < len(T.timeHeader)
            
    else:
        ts["timeHeader_info"] = [T.startingTime, T.timeIncrement, T.endingTime, len(T.timeHeader)]

    list_time = []
    start_time = ts["timeHeader_info"][0]
    incr_time = ts["timeHeader_info"][1]
    end_time = ts["timeHeader_info"][2]
    len_time = ts["timeHeader_info"][3]
    for i_time in xrange(len_time):
        list_time.append(str(start_time))
        start_time += incr_time
    ts["timeHeader"] = list_time
    return ts

def create_dict_of_timesheets(timesheet_folder):
    ts = dict() # dictionary of timesheets
    ts["dayHeader"], ts["timeHeader"], ts["timeHeader_info"] = [], [], []
    for filename in os.listdir(timesheet_folder.strip("/")):
        T = timesheet_from_csv(timesheet_folder + filename)
        ts[T.name] = T
        ts = dayHeader_add(ts, T)
        ts = timeHeader_redefine(ts, T)
    return ts

def free_times(T): # returns all of the times free in the timesheet
    freeTimes = []
    for day in T.dayHeader:
        for time in T.timeHeader:
            if T.checkAvail(day, time): freeTimes.append((day, time))
    return freeTimes

def build_L(freeTime, ts):
    L = [["x" for i in xrange(len(ts["dayHeader"]))] for j in xrange(len(ts["timeHeader"]))]
#    for i in xrange(len(L)): 
#        print L[i]
#    print freeTime
    count = 0
    for fT in freeTime:
        (day, time) = fT
#        print type(day), type(time), type(fT)
#        print ts["dayHeader"], ts["timeHeader"]
        day_index, time_index = ts["dayHeader"].index(day), ts["timeHeader"].index(time)
#        print day_index, day, time_index, time, type(L)
#        for i in xrange(len(L)): print i, L[i], type(L[i])
#        print
        L[time_index][day_index] = ""
#        print  
#        for i in xrange(len(L)): print i, L[i], type(L[i])
    return L

def run():
    ts = create_dict_of_timesheets(TIMESHEET_FOLDER)
    freeTime = []
    for name in ts:
        if type(ts[name]) is Timesheet:
            tsTime = free_times(ts[name]) #@TODO: Implement slack variable
            if len(freeTime) > 0:
                freeTime = [val for val in freeTime if val in set(tsTime)]
            else:
                freeTime = tsTime
#    print freeTime
    L = build_L(freeTime, ts)
#    for row in L: 
#        print row
    masterT = Timesheet("Alexis, David, Leann S16", L, ts["dayHeader"], ts["timeHeader"])
    masterT.disp()

run()
