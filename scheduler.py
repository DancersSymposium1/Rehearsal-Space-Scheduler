import pickle
import os

TIMESHEET_FOLDERS = 'timesheets/'

def load_maps():
    piece_map = pickle.load(open(MAPS_PATH + 'piece_map.p', 'r+'))
    dancer_map = pickle.load(open(MAPS_PATH + 'dancer_map.p', 'r+'))
    return (piece_map, dancer_map)

def run():
    (piece_map, dancer_map) = load_maps()
    
    for filename in os.listdir(TIMESHEET_FOLDERS.strip('/')):
        f = open(filename)
run()
