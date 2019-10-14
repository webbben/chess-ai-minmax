###########################################
##########  CHESS FINAL PROJECT  ##########
###########################################

### Board ###
# 2d array

### Pieces ###
# team 1 and 2
# team 1 is human, team 2 is AI
# separate class for pieces?
# data:
## team
## type
## coords?
## bool alive

#king = Ki
#queen = Qu
#bishop = Bi
#knight = Kn
#rook = Ro
#pawn = Pa

#Pawn - 1 point
#Knight - 3 points
#Bishop - 3 points
#Rook - 5 points
#Queen - 9 points

### AI ###
# minimax and alpha beta
## optimizations for alpha beta
# dictionary for dynamic programming

#how to keep track of check most efficiently:
#--players cannot make a move that will make their king in check
#----must be automatically updated with each move then
#------after a move is made (and board child is created) the board's check status is automatically updated?

import copy

class Board():

    def __init__(self, orig=None):
        self.size = 8
        #self.board = [[None for i in range(self.size)] for i in range(self.size)]
        self.board = []
        if orig:
            self.board = copy.deepcopy([list(col) for col in orig.board])
            self.player1check = orig.player1check
            self.player2check = orig.player2check
        else:
            self.player1check = False
            self.player2check = False
            for row in range(self.size):
                r = []
                if row == 0:
                    r.append(("Ro", 2))
                    r.append(("Kn", 2))
                    r.append(("Bi", 2))
                    r.append(("Qu", 2))
                    r.append(("Ki", 2))
                    r.append(("Bi", 2))
                    r.append(("Kn", 2))
                    r.append(("Ro", 2))
                elif row == 1:
                    for i in range(self.size):
                        r.append(("Pa", 2))
                elif row == 6:
                    for i in range(self.size):
                        r.append(("Pa", 1))
                elif row == 7:
                    r.append(("Ro", 1))
                    r.append(("Kn", 1))
                    r.append(("Bi", 1))
                    r.append(("Qu", 1))
                    r.append(("Ki", 1))
                    r.append(("Bi", 1))
                    r.append(("Kn", 1))
                    r.append(("Ro", 1))
                else:
                    r = [" * " for i in range(8)]
                self.board.append(r)


    #because I can't make the board into a tuple and store it in a dictionary (like we've done before)
    #I decided to make a "hash" function that converts the 2d array of tuples into a 1d array of strings
    #this function wont be used to recreate boards, just to represent a board in a dictionary for dynamic programming
    #empty space = '00'
    #pawn = '1'
    #rook = '2'
    #knight = '3'
    #bishop = '4'
    #queen = '5'
    #king = '6'
    #second integer in string will represent the team 1/2
    def hashList(self):
        ref = [" * ", "Pa", "Ro", "Kn", "Bi", "Qu", "Ki"]
        h = []
        for i in range(self.size):
            for j in range(self.size):
                p = self.board[i][j]
                if p == " * ":
                    h.append('00')
                else:
                    h.append(str(ref.index(p[0])) + str(p[1]))
        return h


    #determines the score of the board
    #score = sum of values of player1 pieces - sum of values of player2 pieces
    def score(self):
        boardScore = 0
        if self.isTerminal(True): #if player1 lost...
            return -1000
        if self.isTerminal(False): #if player2 lost...
            return 1000
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != " * ":
                    p = self.board[i][j]
                    if p[1] == 1:
                        mult = 1
                    else:
                        mult = -1
                    if p[0] == "Pa":
                        boardScore += (1 * mult)
                    if p[0] == "Kn":
                        boardScore += (3 * mult)
                    if p[0] == "Bi":
                        boardScore += (3 * mult)
                    if p[0] == "Ro":
                        boardScore += (5 * mult)
                    if p[0] == "Qu":
                        boardScore += (9 * mult)
        return boardScore


    #determines if the game is over for the given player
    def isTerminal(self, isPlayerOne):
        if isPlayerOne:
            team = 1
        else:
            team = 2
        #finds possible moves for the player
        #determines if player's king is in check
        #if no possible moves AND king is in check: --> gameover
        possibleMoves = self.generateChildren(isPlayerOne)
        if len(possibleMoves) == 0:
            if isPlayerOne:
                return self.player1check
            else:
                return self.player2check


    #updates the status of check for each player
    #should be done after any move is made
    def updateChecks(self):
        #find kings coordinates
        #generate constraints for both teams
        #if kings coords in a constrained space:
        #---set player's check to True
        #else:
        #---set player's check to False
        #print("updating checks.......")
        p1King = None
        p2King = None
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != " * ":
                    p = self.board[i][j]
                    if p[0] == "Ki":
                        if p[1] == 1:
                            p1King = (i, j)
                        else:
                            p2King = (i, j)
        p1constraints = self.getConstraints(True) #spots that player1 can attack
        p2constraints = self.getConstraints(False) #spots that player2 can attack
        if p1King in p2constraints:
            self.player1check = True
        else:
            self.player1check = False
        if p2King in p1constraints:
            self.player2check = True
        else:
            self.player2check = False
        #print("....updating done")


    #returns a list of tuples containing the coordinates in which the given team can currently attack
    #used mostly for determining if a king is in check (for kingMoves)
    #FIX:
    #--needs to handle pawns correctly (pawns can't attack directly in front)
    def getConstraints(self, isPlayerOne):
        constraintList = []
        if isPlayerOne:
            team = 1
        else:
            team = 2
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != " * ":
                    p = self.board[i][j]
                    if p[1] == team:
                        moves = self.getConstraintsHelper(p, i, j)
                        if moves == None:
                            continue
                        for move in moves:
                            if p[0] == "Pa": #exception for pawns
                                if move[1] != j: #move directly in front is not an attacking move for pawns...
                                    if not move in constraintList:
                                        constraintList.append(move)
                            else: #for non pawns...
                                if not move in constraintList:
                                    constraintList.append(move)
        return constraintList


    #does the same thing as getMoves except ignores kings
    def getConstraintsHelper(self, p, x, y):
        pType = p[0]
        if pType == "Pa":
            return self.pawnMoves(x, y)
        if pType == "Ro":
            return self.rookMoves(x, y)
        if pType == "Kn":
            return self.knightMoves(x, y)
        if pType == "Bi":
            return self.bishopMoves(x, y)
        if pType == "Qu":
            return self.queenMoves(x, y)
        return None
                        

    #algorithm:
    #for each spot on board:
    #---if spot == correct team:
    #------find moves function
    #------generate new board for each of those moves
    #------add to list of children
    #return list of children
    #FIX:
    #--if king is in check, limit moves to those that will render king not in check
    def generateChildren(self, isPlayerOne):
        possibleChildren = []
        if isPlayerOne:
            team = 1
        else:
            team = 2
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != " * ":
                    if self.board[i][j][1] == team:
                        p = self.board[i][j]
                        #print(str(i) + ", " + str(j))
                        moves = self.getMoves(p, i, j)
                        if moves == None:
                            continue
                        for move in moves:
                            if p[0] == "Pa":
                                if move[0] in ["Pa", "Kn", "Bi", "Ro", "Qu"]: #for reviving dead pieces
                                    b = Board(self)
                                    b.board[i][j] = move
                                    possibleChildren.append(b)
                                    continue
                            b = Board(self)
                            b.movePiece(i, j, move[0], move[1])
                            possibleChildren.append(b)
        returnList = []
        for child in possibleChildren: #subtract out moves where the king is in check
            if isPlayerOne:
                if not child.player1check:
                    returnList.append(child)
            else:
                if not child.player2check:
                    returnList.append(child)
        return returnList


    #sends p to its proper function for determining possible moves
    #returns list of moves generated from function it passes to
    def getMoves(self, p, x, y):
        pType = p[0]
        if pType == "Pa":
            return self.pawnMoves(x, y)
        if pType == "Ro":
            return self.rookMoves(x, y)
        if pType == "Kn":
            return self.knightMoves(x, y)
        if pType == "Bi":
            return self.bishopMoves(x, y)
        if pType == "Qu":
            return self.queenMoves(x, y)
        else:
            return self.kingMoves(x, y)


    #returns a list of all the non-pawn dead pieces for the given team
    #this list is used for when pawns replace themselves with a dead piece
    #it should go without saying that kings are not revived...
    def getDeadPieces(self, isPlayerOne):
        pieces = ["Ro", "Ro", "Kn", "Kn", "Bi", "Bi", "Qu"]
        if isPlayerOne:
            team = 1
        else:
            team = 2
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != " * ":
                    p = self.board[i][j]
                    if p[1] == team:
                        if p[0] in pieces:
                            pieces.remove(p[0])
        return pieces
    

    #pawns can only move forward, or diagonal-forward if it can attack there
    #pawn can move two squares if it's its first move
    #pawns can also exchange themselves for a dead piece if they reach the other teams side
    def pawnMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        if p[1] == 1:
            #player 1 goes up the board
            if x == 0: #on other team's side
                replaceOptions = self.getDeadPieces(True)
                for option in replaceOptions:
                    moves.append((option, 1)) #since this move doesn't involve changing spots, it will be handled as an exception
            if x == 6: #this is the first move for this pawn, so can move 2 squares
                if self.board[x - 2][y] == " * ":
                    moves.append((x - 2, y))
            if x > 0:
                if self.board[x - 1][y] == " * ":
                    moves.append((x - 1, y))
                if self.onBoard(x - 1, y - 1):
                    if self.board[x - 1][y - 1] != " * ":
                        if self.board[x - 1][y - 1][1] != p[1]: #attack front-left
                            moves.append((x - 1, y - 1))
                if self.onBoard(x - 1, y + 1):
                    if self.board[x - 1][y + 1] != " * ":
                        if self.board[x - 1][y + 1][1] != p[1]: #attack front-left
                            moves.append((x - 1, y + 1))
        else:
            #player 2 goes down the board
            if x == 7: #on other team's side
                replaceOptions = self.getDeadPieces(False)
                for option in replaceOptions:
                    moves.append((option, 2)) #since this move doesn't involve changing spots, it will be handled as an exception
            if x == 1: #this is the first move for this pawn, can move 2 squares
                if self.board[x + 2][y] == " * ":
                    moves.append((x + 2, y))
            if x < self.size - 1:
                if self.board[x + 1][y] == " * ":
                    moves.append((x + 1, y))
                if self.onBoard(x + 1, y - 1):
                    if self.board[x + 1][y - 1] != " * ":
                        if self.board[x + 1][y - 1][1] != p[1]: #attack front-left
                            moves.append((x + 1, y - 1))
                if self.onBoard(x + 1, y + 1):
                    if self.board[x + 1][y + 1] != " * ":
                        if self.board[x + 1][y + 1][1] != p[1]: #attack front-left
                            moves.append((x + 1, y + 1))
        return moves


    #rooks can only move in straight lines up, down, left, and right
    #cannot move over pieces
    def rookMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for direc in directions:
            blocked = False
            x1 = x
            y1 = y
            dx, dy = direc
            while not blocked:
                x1 += dx
                y1 += dy
                if self.onBoard(x1, y1):
                    if self.board[x1][y1] == " * ": #if its an empty spot
                        moves.append((x1, y1))
                    else:
                        if self.board[x1][y1][1] != p[1]: #if its an enemy spot
                            moves.append((x1, y1))
                        blocked = True
                else:
                    blocked = True
        return moves


    #knights can only move in L shapes
    #knights can also move over other pieces
    def knightMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        directions = [(-2, 1), (-2, -1),
                      (-1, -2), (1, -2),
                      (-1, 2), (1, 2),
                      (2, 1), (2, -1)]
        for direc in directions:
            dx, dy = direc
            x1 = x + dx
            y1 = y + dy
            if self.onBoard(x1, y1):
                if self.board[x1][y1] == " * ":
                    moves.append((x1, y1))
                else:
                    if self.board[x1][y1][1] != p[1]: #attacking enemy piece
                        moves.append((x1, y1))
        return moves


    def bishopMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for direc in directions:
            blocked = False
            x1 = x
            y1 = y
            dx, dy = direc
            while not blocked:
                x1 += dx
                y1 += dy
                if self.onBoard(x1, y1):
                    if self.board[x1][y1] == " * ": #if its an empty spot
                        moves.append((x1, y1))
                    else:
                        if self.board[x1][y1][1] != p[1]: #if its an enemy spot
                            moves.append((x1, y1))
                        blocked = True
                else:
                    blocked = True
        return moves


    def queenMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        for direc in directions:
            blocked = False
            x1 = x
            y1 = y
            dx, dy = direc
            while not blocked:
                x1 += dx
                y1 += dy
                if self.onBoard(x1, y1):
                    if self.board[x1][y1] == " * ": #if its an empty spot
                        moves.append((x1, y1))
                    else:
                        if self.board[x1][y1][1] != p[1]: #if its an enemy spot
                            moves.append((x1, y1))
                        blocked = True
                else:
                    blocked = True
        return moves


    #can only moves 1 tile in any direction
    #cannot make a move that would put it in check (has an enemy targeting the tile)
    def kingMoves(self, x, y):
        moves = []
        p = self.board[x][y]
        #need to make a function that gets all constrained tiles based on checks
        directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        for direc in directions:
            dx, dy = direc
            x1 = x + dx
            y1 = y + dy
            if self.onBoard(x1, y1):
                if self.board[x1][y1] == " * ":
                    moves.append((x1, y1))
                else:
                    if self.board[x1][y1][1] != p[1]: #enemy piece
                        moves.append((x1, y1))
        if p[1] == 1:
            isPlayerOne = True
        else:
            isPlayerOne = False
        returnMoves = []
        constrainedSpaces = self.getConstraints(not isPlayerOne)
        for move in moves: #king cannot move to a spot in check
            if not move in constrainedSpaces:
                returnMoves.append(move)
        return returnMoves
        
    
    
    #moves the given piece p to the coordinates x, y
    def movePiece(self, x, y, x1, y1):
        if self.board[x][y] != " * ":
            self.board[x1][y1] = self.board[x][y]
            self.board[x][y] = " * "
            self.updateChecks()
        else:
            print("ERROR: movePiece: you tried moving an empty spot!")


    #determines if the given coordinates are on the board
    def onBoard(self, x, y):
        if x >= 0:
            if x <= self.size - 1:
                if y >= 0:
                    if y <= self.size - 1:
                        return True
        return False
    

    #prints out the board
    def print(self):
        rowCoord = 0
        print("   -----------------------------------\n")
        for row in self.board:
            s = str(rowCoord) + " | "
            for spot in row:
                if spot == " * ":
                    s = s + " " + spot
                else:
                    s = s + " " + spot[0] + str(spot[1])
            s = s + "  |\n"
            print(s)
            rowCoord += 1
        print("   -----------------------------------")
        print("      0   1   2   3   4   5   6   7")
        

