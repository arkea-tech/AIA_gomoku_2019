#!/usr/bin/env python3

import re
import threading
import queue
import time
import sys

class Gomoku:
    def __init__(self):
        self.threadParsing = None
        self.threadOutput = None
        self.threadInput = None
        self.input = None
        self.boardSize = 20
        self.leave = False
        self.queueInput = queue.Queue(1000)
        self.queueOutput = queue.Queue(1000)
        self.queueParsing = queue.Queue(1000)
        self.newBoard = False
        self.firstPlay = False
        self.getInfo = False
        self.oppMove = False
        self.oppMoveX = None
        self.oppMoveY = None
        self.iaMoveX = 0
        self.iaMoveY = 0
        self.piece_pos = []
        self.map = []

    def threadLaunch(self):
        try:
            self.threadParsing = threading.Thread(target= self.parsingHandler)
            self.threadInput = threading.Thread(target= self.inputHandler)
            self.threadOutput = threading.Thread(target= self.outputHandler)
            self.threadParsing.start()
            self.threadInput.start()
            self.threadOutput.start()
        except:
            sys.exit(0)

    def threadClose(self):
        self.threadParsing.join()
        self.threadInput.join()
        self.threadOutput.join()

    def parsingHandler(self):
        try:
            self.createMap()
            while (self.leave == False):
                self.input = input()
                if (re.search(r'^START (\d+)', self.input)):
                    size = int(re.match(r'^START (\d+)', self.input).group(1))
                    if (size >= 5 and size <= 100):
                        self.boardSize = size
                        print("OK")
                    else:
                        print("ERROR")
                elif (re.search(r'^INFO', self.input)): 
                    self.getInfo = True
                elif (re.search(r'^TAKEBACK (\d+),(\d+)', self.input)): 
                    takeX = int(re.match(r'^TAKEBACK (\d+)', self.input).group(1))
                    takeY = int(re.match(r'^TAKEBACK (\d+),(\d+)', self.input).group(2))
                    if (takeX >= 0 and takeX <= self.boardSize and takeY >= 0 and takeY <= self.boardSize and self.map[takeY][takeX] != 0):
                        self.map[takeY][takeX] = 0
                        print("OK")
                    else:
                        print("ERROR")
                elif (re.search(r'^RESTART', self.input)):
                    print("OK")
                    self.createMap()
                    self.firstPlay = False
                elif (re.search(r'^BEGIN', self.input)):
                    if (self.firstPlay == False):
                        self.firstPlay = True
                        print("10,10")
                        self.map[10][10] = 1
                elif (re.search(r'^STATUS', self.input)):
                    cpMap = self.copyMap()
                    for i in range(self.boardSize):
                        for j in range(self.boardSize):
                            if (cpMap[i][j] == -1):
                                cpMap[i][j] = 2
                    for x in cpMap:
                        print(x)
                elif (re.search(r'^BOARD', self.input)):
                    self.newBoard = True
                    while (self.newBoard == True):
                        self.input = input()
                        if (re.search(r'^DONE', self.input)):
                            self.iaMove()
                            self.map[self.iaMoveX][self.iaMoveY] = 1
                            print(str(self.iaMoveY) + ',' + str(self.iaMoveX))
                            self.newBoard = False   
                        elif (re.search(r'^(\d+),(\d+),(\d+)', self.input)):
                            self.piece_pos.append(int(re.match(r'^(\d+),(\d+),(\d+)', self.input).group(1)))
                            self.piece_pos.append(int(re.match(r'^(\d+),(\d+),(\d+)', self.input).group(2)))
                            self.piece_pos.append(int(re.match(r'^(\d+),(\d+),(\d+)', self.input).group(3)))
                            if (self.piece_pos[0] >= 0 and self.piece_pos[0] <= self.boardSize and 
                                self.piece_pos[1] >= 0 and self.piece_pos[1] <= self.boardSize and
                                self.piece_pos[2] >= 1 and self.piece_pos[2] <= 2):
                                if (self.piece_pos[2] == 2):
                                    self.map[self.piece_pos[1]][self.piece_pos[0]] = -1
                                else:
                                    self.map[self.piece_pos[1]][self.piece_pos[0]] = 1
                            for i in range(3):
                                self.piece_pos.pop(0)
                elif (re.search(r'^TURN (\d+),(\d+)', self.input)):
                    self.oppMoveX = int(re.match(r'^TURN (\d+)', self.input).group(1))
                    self.oppMoveY = int(re.match(r'^TURN (\d+),(\d+)', self.input).group(2))
                    if (self.oppMoveX >= 0 and self.oppMoveX <= self.boardSize and self.oppMoveY >= 0 and self.oppMoveY <= self.boardSize and self.map[self.oppMoveY][self.oppMoveX] == 0):
                        self.map[self.oppMoveY][self.oppMoveX] = -1
                        self.iaMove()
                        self.map[self.iaMoveX][self.iaMoveY] = 1
                        print(str(self.iaMoveY) + ',' + str(self.iaMoveX))
                    else:
                        print("ERROR")
                elif (re.search(r'^END', self.input)):
                    exit(0)
                elif (re.search(r'^QUIT', self.input)):
                    self.leave = True
                elif (re.search(r'^ABOUT', self.input)):
                    print("name='pbrain-minMax', version='1.0', author='Tony & Gabriel', country='France'")
                else:
                    print("UNKNOW")
        except:
            sys.exit(0)
                

    def IAHandler(self):
        self.createMap()
        while (self.leave == False):
            time.sleep(0.1)
            if (self.newBoard == True):
                self.replaceBoard()
            if (self.oppMove == True):
                self.iaMove()
                self.oppMove = False
                self.map[self.iaMoveX][self.iaMoveY] = 1
                print(str(self.iaMoveY) + ',' + str(self.iaMoveX))

    def inputHandler(self):
        try:
            while(self.leave == False):
                self.queueInput.put(input())
                time.sleep(0.1)
        except:
            sys.exit(0)

    def outputHandler(self):
        try:
            while (self.leave == False):
                if (self.queueOutput.empty() == False):
                    print(self.queueOutput.get())
                time.sleep(0.1)
        except:
            sys.exit(0)

    def replaceBoard(self):
        while (self.newBoard == True):
            if (self.queueParsing.empty() == False):
                if (self.piece_pos[0] >= 0 and self.piece_pos[0] <= self.boardSize and 
                    self.piece_pos[1] >= 0 and self.piece_pos[1] <= self.boardSize and
                    self.piece_pos[2] >= 1 and self.piece_pos[2] <= 2):
                    if (self.piece_pos[2] == 2):
                        self.map[self.piece_pos[1]][self.piece_pos[0]] = -1
                    else:
                        self.map[self.piece_pos[1]][self.piece_pos[0]] = 1
                for i in range(3):
                    self.piece_pos.pop(0)
                self.queueParsing.get()

    def createMap(self):
        self.map = []
        buf = None
        for i in range(self.boardSize):
            buf = [0] * self.boardSize
            self.map.append(buf)

    def iaMove(self):
        highestScore = 0
        tmp = 0
        tmp2 = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if (self.map[i][j] == 0 and
                ((  i - 1 >= 0 and j - 1 >= 0 and self.map[i - 1][j - 1] != 0)
                or (i - 1 >= 0 and self.map[i - 1][j] != 0)
                or (i - 1 >= 0 and j + 1 < self.boardSize and self.map[i - 1][j  + 1] != 0)
                or (j - 1 >= 0 and self.map[i][j - 1] != 0)
                or (j + 1 < self.boardSize and self.map[i][j + 1] != 0)
                or (i + 1 < self.boardSize and j - 0 >= 0 and self.map[i + 1][j - 1] != 0)
                or (i + 1 < self.boardSize and self.map[i + 1][j] != 0)
                or (i + 1 < self.boardSize and j + 1 < self.boardSize and self.map[i + 1][j + 1] != 0))
                ):
                    tmp = self.getScoreIa(i, j)
                    tmp2 = self.getScoreOpp(i, j)
                    if (tmp > tmp2 and highestScore <= tmp):
                        self.iaMoveX = i
                        self.iaMoveY = j
                        highestScore = tmp
                    elif (tmp2 > tmp and highestScore <= tmp2):
                        self.iaMoveX = i
                        self.iaMoveY = j
                        highestScore = tmp2

    def getScoreOpp(self, x, y):
        tmp = 0
        mapCopy = self.copyMap()
        mapCopy[x][y] = -1
        multiplier = 0

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if (mapCopy[i][j] == 1):
                    mapCopy[i][j] = -1
                elif (mapCopy[i][j] == -1):
                    mapCopy[i][j] = 1

        for i in range(self.boardSize):
            for j in range(self.boardSize - 4):
                for k in range(5):
                    tmp += mapCopy[i][j + k]
                    if (k > 3 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k - 2] == 1 and mapCopy[i][j + k - 3] == 1 and mapCopy[i][j + k - 4] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 400
                    elif (k > 2 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k - 2] == 1 and mapCopy[i][j + k - 3] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 200
                    elif (k > 0 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(self.boardSize):
                for k in range(5):
                    tmp += mapCopy[i + k][j]
                    if (k > 3 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k - 2][j] == 1 and mapCopy[i + k - 3][j] == 1 and mapCopy[i + k - 4][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 400
                    elif (k > 2 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k - 2][j] == 1 and mapCopy[i + k - 3][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 200
                    elif (k > 0 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k][j] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(self.boardSize - 4):
                for k in range(5):
                    tmp += mapCopy[i + k][j + k]
                    if (k > 3 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k - 2][j + k - 2] == 1 and mapCopy[i + k - 3][j + k - 3] == 1 and mapCopy[i + k - 4][j + k - 4] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 400
                    elif (k > 2 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k - 2][j + k - 2] == 1 and mapCopy[i + k - 3][j + k - 3] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 200
                    elif (k > 0 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k][j + k] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(4, self.boardSize):
                for k in range(5):
                    tmp += mapCopy[i - k][j - k]
                    if (k > 2 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k - 2][j - k + 2] == 1 and mapCopy[i + k - 3][j - k + 3] == 1 and mapCopy[i + k - 4][j - k + 4] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 400
                    elif (k > 2 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k - 2][j - k + 2] == 1 and mapCopy[i + k - 3][j - k + 3] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 200
                    elif (k > 0 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k][j - k] == -1):
                        multiplier -= 3
        return (tmp + multiplier)

    def getScoreIa(self, x, y):
        tmp = 0
        mapCopy = self.copyMap()
        mapCopy[x][y] = 1
        multiplier = 0

        for i in range(self.boardSize):
            for j in range(self.boardSize - 4):
                for k in range(5):
                    tmp += mapCopy[i][j + k]
                    if (k > 3 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k - 2] == 1 and mapCopy[i][j + k - 3] == 1 and mapCopy[i][j + k - 4] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 1000
                    elif (k > 2 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k - 2] == 1 and mapCopy[i][j + k - 3] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 36
                    elif (k > 1 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k - 2] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 12
                    elif (k > 0 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k] == 1):
                        multiplier += 3 
                    elif (k > 0 and mapCopy[i][j + k - 1] == 1 and mapCopy[i][j + k] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(self.boardSize):
                for k in range(5):
                    tmp += mapCopy[i + k][j]
                    if (k > 3 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k - 2][j] == 1 and mapCopy[i + k - 3][j] == 1 and mapCopy[i + k - 4][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 1000
                    elif (k > 2 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k - 2][j] == 1 and mapCopy[i + k - 3][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 36
                    elif (k > 1 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k - 2][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 12
                    elif (k > 0 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k][j] == 1):
                        multiplier += 3
                    elif (k > 0 and mapCopy[i + k - 1][j] == 1 and mapCopy[i + k][j] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(self.boardSize - 4):
                for k in range(5):
                    tmp += mapCopy[i + k][j + k]
                    if (k > 3 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k - 2][j + k - 2] == 1 and mapCopy[i + k - 3][j + k - 3] == 1 and mapCopy[i + k - 4][j + k - 4] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 1000
                    elif (k > 2 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k - 2][j + k - 2] == 1 and mapCopy[i + k - 3][j + k - 3] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 36
                    elif (k > 1 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k - 2][j + k - 2] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 12
                    elif (k > 0 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k][j + k] == 1):
                        multiplier += 3
                    elif (k > 0 and mapCopy[i + k - 1][j + k - 1] == 1 and mapCopy[i + k][j + k] == -1):
                        multiplier -= 3

        for i in range(self.boardSize - 4):
            for j in range(4, self.boardSize):
                for k in range(5):
                    tmp += mapCopy[i - k][j - k]
                    if (k > 2 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k - 2][j - k + 2] == 1 and mapCopy[i + k - 3][j - k + 3] == 1 and mapCopy[i + k - 4][j - k + 4] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 1000
                    elif (k > 2 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k - 2][j - k + 2] == 1 and mapCopy[i + k - 3][j - k + 3] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 36
                    elif (k > 1 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k - 2][j - k + 2] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 12
                    elif (k > 0 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k][j - k] == 1):
                        multiplier += 3
                    elif (k > 0 and mapCopy[i + k - 1][j - k + 1] == 1 and mapCopy[i + k][j - k] == -1):
                        multiplier -= 3
        return (tmp + multiplier)

    def copyMap(self):
        buf = []
        for x in self.map:
            buf.append(x.copy())
        return buf

def main():
    try:
        gomoku = Gomoku()
        gomoku.parsingHandler()
    except:
        sys.exit(0)
    return 0

if __name__ == "__main__":
    main() 