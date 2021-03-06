import sys
import os

# NOTE: download "Timesheet" & "Rehearsal-Space-Scheduler" repos into same directory
sys.path.append(os.path.realpath(os.path.abspath("../Timesheet")))
from timesheet_from_csv import *
from Classes import *

DANCE_TIMESHEET_FOLDER = "dance-timesheets"
SPACE_TIMESHEET_FOLDER = "space-timesheets"
ASSIGNED_UNASSIGNED_FILE = "ASSIGN_SPRING2016.csv"

day_order = { "Sunday" : 0, "Sun"  : 0, "Su"  : 0, "Sn"  : 0,
                            "Sun." : 0, "Su." : 0, "Sn." : 0,
              "Monday" : 1, "Mon"  : 1, "Mo"  : 1, "M"  : 1,
                            "Mon." : 1, "Mo." : 1, "M." : 1,
              "Tuesday" : 2, "Tues"  : 2, "Tue"  : 2, "Tu"  : 2, "T"  : 2,
                             "Tues." : 2, "Tue." : 2, "Tu." : 2, "T." : 2,
              "Wednesday" : 3, "Wed"  : 3, "We"  : 3, "W"  : 3,
                               "Wed." : 3, "We." : 3, "W." : 3,
              "Thursday" : 4, "Thurs"  : 4, "Thur"  : 4, "Thu"  : 4, "Th"  : 4, "H"  : 4,
                              "Thurs." : 4, "Thur." : 4, "Thu." : 4, "Th." : 4, "H." : 4,
              "Friday" : 5, "Fri"  : 5, "Fr"  : 5, "F"  : 5,
                            "Fri." : 5, "Fr." : 5, "F." : 5,
              "Saturday" : 6, "Sat"  : 6, "Sa"  : 6,
                              "Sat." : 6, "Sa." : 6 }

def merge_from_zero(s1, s2):
    res = ""
    for i in xrange(len(s1)):
        if s1[i] == s2[i]:
            res += s1[i]
        else:
            break
    return res

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
    ts["dayHeader"], ts["timeHeader"], ts["timeHeader_info"], ts["name"] = [], [], [], ""
    for filename in os.listdir(timesheet_folder.strip("/")):
        T = timesheet_from_csv(timesheet_folder + "/" + filename)
        ts[T.name] = T
        if len(ts["name"]) == 0:
            ts["name"] = T.name[:T.name.find("-") - 1]
        else:
            ts["name"] = merge_from_zero(ts["name"], T.name)
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
    count = 0
    for fT in freeTime:
        (day, time) = fT
        day_index, time_index = ts["dayHeader"].index(day), ts["timeHeader"].index(time)
        L[time_index][day_index] = ""
    return L

def merge_timesheets(timesheet_folder):
    ts = create_dict_of_timesheets(timesheet_folder)
    freeTime = []
    for name in ts:
        if type(ts[name]) is Timesheet:
            tsTime = free_times(ts[name]) #@TODO: Implement slack variable
            if len(freeTime) > 0:
                freeTime = [val for val in freeTime if val in set(tsTime)]
            else:
                freeTime = tsTime
    L = build_L(freeTime, ts)
    masterT = Timesheet(ts["name"], L, ts["dayHeader"], ts["timeHeader"])
    return masterT

def create_space_dict():
    sD = dict()
    sDict = create_dict_of_timesheets(SPACE_TIMESHEET_FOLDER)
    for skey in sDict:
        if sDict["name"] in skey:
            sD[skey[skey.find("-") + 2:]] = sDict[skey]
    return sD

def make_assign_list():
    aD = dict()
    last_choreographer = ""
    assign_file = open(ASSIGNED_UNASSIGNED_FILE, 'rU')
    for i, line in enumerate(assign_file):
        text = line.strip().split(",")

        try:
            parse_attempt = int(text[0])
            dancer = text[1].strip()
            aD[last_choreographer] += 1
            #print "Successfully added %s to %s's piece" % (dancer, last_choreographer)
        except:
            last_choreographer = text[0].strip()
            aD[last_choreographer] = 0 #create piece in assign_list
            #print "Successfully created %s's piece" % last_choreographer    
    assign_file.close()

    aL = sorted(aD, key=aD.get, reverse=True)
    return aL

def assign_dances(dT, sD, aL):
    #@TODO: this

def run():
    dT = merge_timesheets(DANCE_TIMESHEET_FOLDER)
    dT.write(os.getcwd()) # prints to "<dance name - sem/year>.txt"

    sD = create_space_dict()
    aL = make_assign_list() # ordered from largest to smallest, by increasing index

    schD = assign_dances(dT, sD, aL) # dictionary of scheduled dances, index by time
    
run()
