from Tkinter import *

def string_to_time(timeString):
    timeString_list = timeString.split()
    hoursmins_list = timeString_list[0].split(":")
    hours, mins = int(hoursmins_list[0]), int(hoursmins_list[1])
    period = timeString_list[1].upper()
    return Time(hours, mins, period)

def get_maxCellWidth(d_t_l, option):
    maxCellWidth = 0
    if option == "day":
        for day in d_t_l:
            if maxCellWidth < len(day): 
                maxCellWidth = len(day)
    elif option == "time":
        for time in d_t_l:
            if maxCellWidth < len(time): 
                maxCellWidth = len(time)
    elif option == "L":
        for row in d_t_l:
            for item in row:
                if maxCellWidth < len(item):
                    maxCellWidth = len(item)
    else:
        print option
        error("This option should not be a possibility")
    return maxCellWidth

def points_to_pixels(pt): # techically (pt*4/3) but was making things too big on the page
    return round(pt * 3 / 3) 


class Timesheet(object):
    def __init__(self, name, L, dayHeader, timeHeader):
        self.name = name
        self.L = L
        self.dayHeader = dayHeader
        self.timeHeader = timeHeader
        self.timeIncrement = self.calcTimeIncr()
        self.startingTime, self.endingTime = self.calcEndpointTimes()

    def getIndices(self, day, time):
        if (day in dayHeader and time in timeHeader):
            return (self.dayHeader.index(day), self.timeHeader.index(time))
        else:
            print "The requested day or time does not exist in the headers"
            return False
            
    def checkAvail(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        return self.L[dayIndex][timeIndex] != "x"

    def markBusy(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        self.L[dayIndex][timeIndex] = "x"

    def markFree(self, day, time):
        (dayIndex, timeIndex) = getIndices(self, day, time)
        self.L[dayIndex][timeIndex] = ""
        
    def calcTimeIncr(self):
        if len(self.timeHeader) > 1: 
            return string_to_time(self.timeHeader[1]) - string_to_time(self.timeHeader[0])
        else: 
            return False #there is no timeIncrement
            
    def calcEndpointTimes(self):
        return string_to_time(self.timeHeader[0]), string_to_time(self.timeHeader[-1])
        
    def disp(self):
        # x is width, y is height
        maxCellWidth_day = get_maxCellWidth(self.dayHeader, "day")
        maxCellWidth_time = get_maxCellWidth(self.timeHeader, "time")
        maxCellWidth_L = get_maxCellWidth(self.L, "L")
        maxCellWidth_dL = max(maxCellWidth_day, maxCellWidth_L)

        font_size = 8
        cellWidth_dL = points_to_pixels(maxCellWidth_dL * font_size)
        cellWidth_time = points_to_pixels(maxCellWidth_time * font_size)
        cellHeight = 2 * font_size
        topMargin = 3 * font_size
        borderMargin = 20
        winWidth = cellWidth_time + cellWidth_dL * len(self.dayHeader) + 2 * borderMargin
        winHeight = cellHeight * len(self.timeHeader) + topMargin + 1.5 * borderMargin
        root = Tk()
        root.wm_title("Timesheet")
        canvas = Canvas(root, width=winWidth, height=winHeight)
        canvas.pack(expand=YES)

        # create title header
        canvas.create_text(winWidth/2 + cellWidth_time/2, topMargin/2, text=self.name)

        tH, dH, L = [""], [""], [[]]
        for t in self.timeHeader: tH.append(t)
        for d in self.dayHeader: dH.append(d)
        for row in self.L: 
            Lrow = [""]
            for item in row: Lrow.append(item)
            L.append(Lrow)

        maxCellLength = 0
        for row in xrange(len(tH)):
            for col in xrange(len(dH)):
                if (row == 0) and (col == 0):
                    continue
                elif row == 0: # day header
                    cellFill = ""
                    cellText = dH[col]
                    x0 = cellWidth_time + (col - 1) * cellWidth_dL + borderMargin
                    y0 = topMargin
                    x1 = x0 + cellWidth_dL
                    y1 = y0 + cellHeight
                elif col == 0: # time header
                    cellFill = ""
                    cellText = tH[row]
                    x0 = borderMargin
                    y0 = row * cellHeight + topMargin
                    x1 = x0 + cellWidth_time
                    y1 = y0 + cellHeight
                else: # inside L
                    cellFill = "red" if (len(L[row][col]) > 0) else "green"
                    cellText = L[row][col]
                    x0 = cellWidth_time + (col - 1) * cellWidth_dL + borderMargin
                    y0 = cellHeight * row + topMargin
                    x1 = x0 + cellWidth_dL
                    y1 = y0 + cellHeight
                canvas.create_rectangle(x0, y0, x1, y1, fill=cellFill)
                canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text=cellText) 
            
        root.mainloop()

class Time(object):
    def __init__(self, hours, mins, period):
        self.hours = hours
        self.mins = mins
        self.period = period.upper()
        
    def __repr__(self):
        return "%02d:%02d %s" % (self.hours, self.mins, self.period)
        
    def __sub__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if mins1 < mins2:
            hours1 = hours1 - 1 if (hours1 != 0) else hours + 24 - 1
            mins1 += 60
        
        hoursX, minsX = hours1 - hours2, mins1 - mins2
        if hoursX > 12:
            hoursX -= 12
            periodX = "PM"
        elif hoursX == 0:
            hoursX += 12
            periodX = "AM"
        else:
            periodX = "AM"
        return Time(hoursX, minsX, periodX)
        
    def __lt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 < hours2: 
            return self
        elif hours2 < hours1: 
            return other
        else: #hours1 == hours2
            return self if mins1 < mins2 else other 

    def __gt__(self, other):
        hours1, mins1 = self.convert_to_24hr()
        hours2, mins2 = other.convert_to_24hr()
        
        if hours1 > hours2: 
            return self
        elif hours2 > hours1: 
            return other
        else: #hours1 == hours2
            return self if mins1 > mins2 else other 

    def convert_to_24hr(self): 
        hours = self.hours + 12 if (self.period == "PM") else self.hours
        hours = 0 if (self.period == "AM" and self.hours == 12) else hours
        mins = self.mins
        
        return hours, mins
