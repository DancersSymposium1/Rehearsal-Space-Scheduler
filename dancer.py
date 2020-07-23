# PIECE SCHEDULER ATTEMPT 1.0
# Author: Amy Zhang
# Date: July 23, 2020
import openpyxl
from typing import Dict, List
from collections import defaultdict


class DancerDirectory():
    # Class to hold all of the information about dancers and their pieces
    def __init__(self, dancer_file_name: str) -> None:
        self.dancerFile: str = dancer_file_name
        self._import_assigned()  

    # helper function for creating a dictionary of DS piece people using the dancer_file_name
    def _import_assigned(self) -> None:
        self.Dancers: Dict[str, List[str]] = defaultdict(lambda: [])
        self.Pieces: List[str] = []
        book = openpyxl.load_workbook(self.dancerFile)
        sheet = book.active
        has_piece = False
        piece = ""
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if row[0] is None and row[1] is None:
                # end of the last piece
                if has_piece is False:
                    break
                else:
                    piece = ""
                    has_piece = False
                    continue
            if has_piece is False:
                # beginning of a new piece
                piece = row[0].lower()
                has_piece = True
                self.Pieces.append(piece)
            else:
                # dancer for piece
                dancer = row[1].lower().strip()
                if len(dancer) is not 0:
                    self.Dancers[dancer].append(piece)
                elif has_piece is False:
                        print("error: no piece name")

    # list_pieces: a class function to list all pieces
    # INPUT: none
    # OUTPUT: a list of all pieces (string list)
    def list_pieces(self) -> List[str]:
        return self.Pieces

    # list_dancer_pieces: a class function to list the number of pieces a dancer is in
    # INPUT: a dancer (string)
    # OUTPUT: a list of pieces the dancer is in (string list)
    def list_dancer_pieces(self, dancer: str) -> List[str]:
        dancer = dancer.lower()
        pieces = self.Dancers[dancer]
        if dancer is not []:
            return pieces
        else:
            print("error: Dancer %s not found\n", dancer)
            return []
