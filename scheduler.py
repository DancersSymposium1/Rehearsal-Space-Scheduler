"""
Objectives:
    -Take all of the dances' timesheets
    -Starting with the largest dance, find the best availability for the dance
    -Recursively backtrack to the next best availability
    -Add a timesheet that gives the priorities of each day and time
    -Output the data in a text file, list format

Input:
    -Dances' timesheets
        -.csv, timesheet_from_csv.py
    -Order of dance sizes
        -.csv, selectionOrder_from_csv
    -Priority of rehearsal time map
        -.csv, priorityMap_from_csv
    -Space availability
        -.csv, spaceMap_from_csv
        
Objects:
    -Timesheets
        -timesheet_from_csv.py
    -Time
        -timesheet_from_csv.py
    -SelectionOrder
        -1D list
    -PriorityMap
        -Timesheet(priorities -> name)
    -SpaceAvailability
        -book of Timesheet    
    -ListOutput
        -dictionary
        
Output:
    -Text list of rehearsal times for each dance
    
"""

