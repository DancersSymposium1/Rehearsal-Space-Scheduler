import pickle
import os
import copy

from timesheet_from_csv import *
from Classes import *
from audition_program import Dancer, Piece, GenderConstraint

TIMESHEET_FOLDER = "timesheets/"
MAPS_PATH = "maps/"

def load_maps():
    piece_map = pickle.load(open(MAPS_PATH + "piece_map.p", "rb"))    
    dancer_map = pickle.load(open(MAPS_PATH + "dancer_map.p", "rb"))
    return (piece_map, dancer_map)

def run():
    # make sure the Audition code is run so that these maps are created 
    (piece_map, dancer_map) = load_maps()
    
    for filename in os.listdir(TIMESHEET_FOLDER.strip("/")):
        f = open(TIMESHEET_FOLDER + filename)

        #@TODO: everything!
        
        f.close()

run()
