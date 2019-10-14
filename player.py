from board import Board
import random
import time

class Player():

    def __init__(self, depth, AItype, isPlayerOne):
        self.depth = depth
        self.isPlayerOne = isPlayerOne
        self.alreadySeen = {}
        self.AItype = AItype
        self.start = 0 #this is used as a global time variable


    def getTime(self):
        return time.time() - self.start

    
    def findMove(self, board):
        print(self.AItype + " AI is making its move...")
        self.start = time.time()
        if self.AItype == "minimax":
            move = self.minimaxAI(board, self.depth, -1000, 1000, self.isPlayerOne)[0]
        elif self.AItype == "naive":
            move = self.naiveAI(board, self.isPlayerOne)
        else: #goes to random if ai type not recognized
            move = self.randomAI(board, self.isPlayerOne)
        print("time elapsed: " + str(self.getTime()) + " seconds")
        return move

    #naive AI just chooses the highest score board out of its immediate options
    #it does not traverse any depth of minimax
    def naiveAI(self, board, isPlayerOne):
        children = board.generateChildren(isPlayerOne)
        if len(children) == 0: #if there are no moves that means it lost
            return None
        if isPlayerOne:
            maxScore = -100
            maxMove = children[0]
            for child in children:
                if child.score() > maxScore:
                    maxScore = child.score()
                    maxMove = child
            return maxMove
        else:
            minScore = 100
            minMove = children[0]
            for child in children:
                if child.score() < minScore:
                    minScore = child.score()
                    minMove = child
            return minMove


    #picks a random move
    def randomAI(self, board, isPlayerOne):
        children = board.generateChildren(isPlayerOne)
        r = random.randrange(len(children))
        return children[r]


    #ideas to speed up search:
    #as depth approaches zero (assuming initial depth is >2)
    #---decrease children nodes that are searched per node
    #------# of children explored = current depth * 2?
    def minimaxAI(self, board, depth, alpha, beta, isPlayerOne):
        #print(str(depth))
        #if self.getTime() > 80:
            #print("time up...")
            #return (None, board.score())
        if depth == 0:
            finalScore = board.score()
            #print("heuristic: " + str(finalScore))
            return (None, finalScore)
        if tuple(board.hashList()) in self.alreadySeen: #if current board has already been evaluated
            print("Already seen")
            return self.alreadySeen[tuple(board.hashList())]
        #if board.isTerminal(True): #if player1 lost in this state
            #return (None, -1000)
        #if board.isTerminal(False): #if player2 lost
            #return (None, 1000)
        children = board.generateChildren(isPlayerOne)
        #children = list(sorted(children, key=lambda x: x.score()))

        #trying to cut down on children explored lower in the tree

        if len(children) == 0:
            return (None, board.score())
        
        
        if isPlayerOne:
            children = sorted(children, key=lambda x: x.score(), reverse=True)
            children = children[:depth * 3] #cuts number of children explored at deeper levels
            maxScore = -100
            r = random.randrange(len(children))
            #print(str(r))
            progress = 0 #use this for displaying % doneness
            bestMove = children[r]
            for child in children:
                boardScore = self.minimaxAI(child, depth - 1, alpha, beta, not isPlayerOne)[1]
                if boardScore > maxScore:
                    maxScore = boardScore
                    bestMove = child
                alpha = max(boardScore, alpha)
                if depth == self.depth:
                    progress += 1
                    print("top order move evaluated")
                    print("current time elapsed: " + str(round(self.getTime())) + " seconds")
                    print(str(round((progress / len(children)) * 100)) + "% done...")
                if alpha > beta:
                    print("PRUNE")
                    break
            self.alreadySeen[tuple(board.hashList())] = (bestMove, maxScore)
            return (bestMove, maxScore)
        else:
            children = sorted(children, key=lambda x: x.score())
            children = children[:depth * 3] #cuts number of children explored at deeper levels
            minScore = 100
            r = random.randrange(len(children))
            #print(str(r))
            bestMove = children[r]
            for child in children:
                boardScore = self.minimaxAI(child, depth - 1, alpha, beta, not isPlayerOne)[1]
                if boardScore < minScore:
                    minScore = boardScore
                    bestMove = child
                beta = min(boardScore, beta)
                if alpha > beta:
                    print("PRUNE")
                    break
            self.alreadySeen[tuple(board.hashList())] = (bestMove, minScore)
            return (bestMove, minScore)


                



                    
