import pickle
import os
import copy

TIMESHEET_FOLDERS = 'timesheets/'

def load_maps():
    pm = open(MAPS_PATH + 'piece_map.p', 'r+')
    piece_map = pickle.load(pm)
    piece_map_copy = copy.deepcopy(piece_map)
    pm.close()
    
    dm = open(MAPS_PATH + 'dancer_map.p', 'r+')
    dancer_map = pickle.load(dm)
    dancer_map_copy = copy.deepcopy(dancer_map)
    dm.close()
    
    return (piece_map_copy, dancer_map_copy)

def run():
    (piece_map, dancer_map) = load_maps()
    
    for filename in os.listdir(TIMESHEET_FOLDERS.strip('/')):
        f = open(filename)
run()
