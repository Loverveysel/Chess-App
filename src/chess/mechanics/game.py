# game.py
import sys
from os.path import abspath, dirname

# Get the current directory of the file
currentDir = dirname(abspath(__file__))

sys.path.append(currentDir)
import pieces


class Game:
    def __init__(self):
        # Initialize the game board and other attributes
        self.board = {}
        self.round = "white"
        self.xCoordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.yCoordinates = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.check = False
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = {
            "white" : self.whitePieces,
            "black" : self.blackPieces
        }

        self.castling = {
            "white":{
                "queenSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "a1",
                    "castledKingCoordinate": "c1",
                    "castledRookCoordinate": "d1"
                },
                "kingSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "h1",
                    "castledKingCoordinate": "g1",
                    "castledRookCoordinate": "f1" 
                }
            },
            "black":{
                "queenSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate" : "a8",
                    "castledKingCoordinate": "c8",
                    "castledRookCoordinate": "d8"
                },
                "kingSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "h8",
                    "castledKingCoordinate": "g8",
                    "castledRookCoordinate": "f8"
                }
            }
        }
        self.castlingCoordinate = {
                        "coordinate" : None,
                        "side" : None
                    }

        """self.roundLabel = RoundWidget()"""
    
        for row in self.xCoordinates:
            for col in  self.yCoordinates:
                coordinate = row + col
                
                self.board.update({coordinate : {
                    "piece": None, 
                    "coordinate": coordinate,
                } })

        ##Setting the Pieces on the start
        self.setStartPiece()

    def setStartPiece(self):
        # Set up the initial pieces on the board

        for col in self.xCoordinates:
            self.board[col + "2"]["piece"] = pieces.Pawn("white", col + "2", True)
            self.whitePieces.append(self.board[col + "2"]["piece"])

        for col in self.xCoordinates:
            self.board[col + "7"]["piece"] = pieces.Pawn("black", col + "7", True)
            self.blackPieces.append(self.board[col + "7"]["piece"])

        self.board["a1"]["piece"] = pieces.Rook("white", "a1", True)
        self.whitePieces.append(self.board["a1"]["piece"])
        self.castling["white"]["queenSide"]["rook"] = self.board["a1"]["piece"]
        self.board["h1"]["piece"] = pieces.Rook("white", "h1", True)
        self.whitePieces.append(self.board["h1"]["piece"])
        self.castling["white"]["kingSide"]["rook"] = self.board["h1"]["piece"]
        self.board["a8"]["piece"] = pieces.Rook("black", "a8", True)
        self.blackPieces.append(self.board["a8"]["piece"])
        self.castling["black"]["queenSide"]["rook"] = self.board["a8"]["piece"]
        self.board["h8"]["piece"] = pieces.Rook("black", "h8", True)
        self.blackPieces.append(self.board["h8"]["piece"])
        self.castling["black"]["kingSide"]["rook"] = self.board["h8"]["piece"]

        self.board["b1"]["piece"] = pieces.Knight("white", "b1", True)
        self.whitePieces.append(self.board["b1"]["piece"])
        self.board["g1"]["piece"] = pieces.Knight("white", "g1", True)
        self.whitePieces.append(self.board["g1"]["piece"])
        self.board["b8"]["piece"] = pieces.Knight("black", "b8", True)
        self.blackPieces.append(self.board["b8"]["piece"])
        self.board["g8"]["piece"] = pieces.Knight("black", "g8", True)
        self.blackPieces.append(self.board["g8"]["piece"])

        self.board["f1"]["piece"] = pieces.Bishop("white", "f1", True)
        self.whitePieces.append(self.board["f1"]["piece"])
        self.board["c1"]["piece"] = pieces.Bishop("white", "c1", True)
        self.whitePieces.append(self.board["c1"]["piece"])
        self.board["f8"]["piece"] = pieces.Bishop("black", "f8", True)
        self.blackPieces.append(self.board["f8"]["piece"])
        self.board["c8"]["piece"] = pieces.Bishop("black", "c8", True)
        self.blackPieces.append(self.board["c8"]["piece"])

        self.board["d1"]["piece"] = pieces.Queen("white", "d1", True)
        self.whitePieces.append(self.board["d1"]["piece"])
        self.board["d8"]["piece"] = pieces.Queen("black", "d8", True)
        self.blackPieces.append(self.board["d8"]["piece"])
        
        self.whiteKing = self.board["e1"]["piece"] = pieces.King("white", "e1", True) 
        self.whitePieces.append(self.board["e1"]["piece"])
        self.blackKing = self.board["e8"]["piece"] = pieces.King("black", "e8", True)
        self.blackPieces.append(self.board["e8"]["piece"])

        self.kings = {
            "white" :{
                "startPoint" : "e1",
                "object" : self.whiteKing 
            } 
            ,
            "black" :{
                "startPoint" : "e8",
                "object" : self.blackKing 
            } 
        }
        
        for row in self.xCoordinates:
            for col in  self.yCoordinates:
                coordinate = row + col
                square = self.board[coordinate]
                if square["piece"] != None:
                    if square["piece"].color[0] == 'w':
                        self.whitePieces.append(square["piece"])
                    else:
                        self.blackPieces.append(square["piece"])
    
    def checkMoveableCoordinates(self, coordinate):        
        # Check the movable coordinates for a given piece


        """
        Check the movable coordinates for a given piece.
        Consider possible moves while checking for checks.
        """
        
        piece = self.board[coordinate]["piece"]
        coordinateList = piece.moveableCoors(self.board)

        checkedCoordinates = []

        #Check the coordinate is able to move(Checking checks :D)
        #CHECKİNG CHECKS...
        for coor in coordinateList:
            old = self.board[coor]["piece"]
            oldCoor = piece.coordinate
            self.board[coor]["piece"] = piece
            piece.coordinate = coor
            isCheck = self.checkCheck()
            if isCheck == True:
               checkedCoordinates.append(coor)
            self.board[coor]["piece"] = old
            piece.coordinate = oldCoor
            
        ##CHECK CASTLING...
        sides = ["queenSide", "kingSide"]
        if isinstance(piece, pieces.King):
            for side in sides:
                if self.castling[piece.color][side]["did"] != True:  
                    if self.castling[piece.color][side]["able"] == True:
                        print(self.castling[piece.color][side]["castledKingCoordinate"])
                        coordinateList.append(self.castling[piece.color][side]["castledKingCoordinate"])
                        self.castlingCoordinate = {
                            "coordinate" : self.castling[piece.color][side]["castledKingCoordinate"],
                            "side" : side
                        }
                        

        for coor in checkedCoordinates:
            coordinateList.remove(coor)

        return coordinateList
    
    def move(self, coordinate, piece, oldCoordinate, coordinateList):
        # Move a piece to a new coordinate

        """
        Move a piece to a new coordinate on the board.
        Handle turn switching and additional logic for special moves like castling.
        """

        self.board[coordinate]["piece"] = piece
        self.board[oldCoordinate]["piece"] = None
        
        if self.round[0] == "w":
            self.round = "black"
        else:
            self.round = "white"
        
        #CHECKING CASTLING...
        if coordinate == self.castlingCoordinate["coordinate"]:
            rook = self.castling[piece.color][self.castlingCoordinate["side"]]["rook"]
            rookOldCoordinate = rook.coordinate
            self.board[rookOldCoordinate]["piece"] = None
            side = self.castlingCoordinate["side"]
            rookNewCoordinate = self.castling[piece.color][side]["castledRookCoordinate"]
            self.board[rookNewCoordinate]["piece"] = rook
            rook.coordinate = rookNewCoordinate
            self.castlingCoordinate = {
                        "coordinate" : None,
                        "side" : None
                    }
            self.castling[piece.color]["queenSide"]["did"] = True
            self.castling[piece.color]["kingSide"]["did"] = True
        
        self.checks()
        

    def checks(self):
        # Perform checks after a move

        self.check = self.checkCheck()
        self.checkCastling()

    def checkCheck(self):
        # Check if a king is under check

        if self.round[0] == 'w':
            for piece in self.blackPieces:
                moveableCoordinates = piece.moveableCoors(self.board)
                if self.whiteKing.coordinate in moveableCoordinates:
                    return True
        else:
            for piece in self.whitePieces:
                moveableCoordinates = piece.moveableCoors(self.board)
                if self.blackKing.coordinate in moveableCoordinates:
                    return True
        return False

    def checkCastling(self):
        # Check if castling is possible

        """
        Check if castling is possible for both players.
        """

        colors = ["white", "black"]
        sides = ["queenSide", "kingSide"]
        for color in colors:
            for side in sides:
                if self.castling[color][side]["did"] == False:
                    if self.castling[color][side]["rook"].coordinate != self.castling[color][side]["coordinate"]:
                        print("1")
                        self.castling[color][side]["did"] = True
                    elif self.kings[color]["startPoint"] != self.kings[color]["object"].coordinate:
                        print(self.kings[color]["startPoint"])
                        self.castling[color]["queenSide"]["did"] = True
                        self.castling[color]["kingSide"]["did"] = True
                    else:
                        isEmpty = True
                        xIndex = self.xCoordinates.index(self.kings[color]["object"].coordinate[0])
                        if side[0] == 'k':
                            stop = 7
                            step = +1
                            xIndex +=1
                        else:
                            stop = 0
                            step = -1
                            xIndex -=1

                        for index in range(xIndex, stop, step):
                            y = self.castling[color][side]["rook"].coordinate[1]
                            coordinate = self.xCoordinates[index] + y
                            if self.board[coordinate]["piece"] != None:
                                isEmpty = False
                        
                        if isEmpty:
                            self.castling[color][side]["able"] = True
                        else:
                            self.castling[color][side]["able"] = False
    