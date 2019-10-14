from board import Board
from player import Player

class Game():

    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board


    #this function runs a game of chess
    #player1 always goes first
    #should loop between player1's turn and player2's turn until gameover
    def playGame(self):
        gameover = False
        print("###NEW GAME###")
        self.board.print()
        numTurns = 0
        while not gameover:
            if self.board.player1check:
                print("!!Player 1 is in check!!")
            if self.board.player2check:
                print("!!Player 2 is in check!!")
            print("Player1's turn~~")
            self.board = self.player1.findMove(self.board)
            if self.board == None: #Game is over if no move can be made
                print("###GAME OVER###")
                print("Player2 wins!")
                break
            if self.board.isTerminal(True):
                print("###GAME OVER###")
                print("Player2 wins!")
                break
            self.board.print()
            if self.board.player1check:
                print("!!Player 1 is in check!!")
            if self.board.player2check:
                print("!!Player 2 is in check!!")
            print("Player2's turn~~")
            self.board = self.player2.findMove(self.board)
            if self.board == None: #Game is over if no move can be made
                print("###GAME OVER###")
                print("Player1 wins!")
                break
            if self.board.isTerminal(False):
                print("###GAME OVER###")
                print("Player1 wins!")
                break
            self.board.print()
            numTurns += 1


##test##
b = Board()
p1 = Player(3, "minimax", True)
p2 = Player(3, "naive", False)
g = Game(p1, p2, b)
g.playGame()
