# Jack Schefer, pd. 6
#
import heapq
from time import time
from copy import deepcopy
#
def blankBoard():
  board = {}
  for i in range(9):
    for j in range(9):
      board[ (i,j) ] = '.'
  return board
#
#print(board)
#
ALL_COORDINATES = []
for i in range(9):
  for j in range(9):
    ALL_COORDINATES.append( (i,j) )
#
def makeBoard(string):
  b = blankBoard()
  for i in range(9):
    for k in range(9):
      sub = string[9*i+k]
      b[(i,k)] = sub
  return b
#
#
#
def printBoard(b):
  for r in range(9):
    s = ''
    for c in range(9):
      s += b[ (r,c) ]
      #s += str(r) + str(c)
      s += ' '
    print(s)
#
#printBoard(board)
#
#
def printBoard2(b):
  for r in range(9):
    s = ''
    for c in range(9):
      n,s,v = board[(r,c)]
      s += v
      #s += str(r) + str(c)
      s += ' '
    print(s)
#
#
#
#
def findNeighbors(board, row, col): #returns a list of tuples, the r,c of each neighbor
  nbrs = set()
  for i in range(9):
    if i != row: nbrs.add((i,col))
    if i != col: nbrs.add((row, i))
  #
  rowQuad = row // 3
  colQuad = col // 3
  for i in range(3):
    for j in range(3):
      nR = i+rowQuad*3
      nC = j+colQuad*3
      if nR != row and nC != col and (nR,nC) not in nbrs: nbrs.add( (nR,nC) )
  #
  return nbrs
#
#
#
#
#
'''   --- CHECKS FOR CORRECT NEIGHBROS ---
for r in range(9):
  for c in range(9):
    b = blankBoard()
    b[ (r,c) ] = '*'
    printBoard(b)
    nbrs = findNeighbors(b, r, c)
    for n in nbrs:
      ro,co = n
      b[(ro,co)] = 'X'
    printBoard(b)
    #print(nbrs)
    #print('\n')
'''
#
#
#
#
#
#'''    --- CHECKS TO PRINT OUT PUZZLE CORRECTLY
s = list(open('sudoku128.txt'))
lines = []
for l in s:
  lines.append(l.rstrip())
#
def isCorrect(board):
  rowsCorrect = True
  colsCorrect = True
  quadsCorrect = True
  #
  for i in range(9):
    rows = set()
    cols = set()
    for j in range(9):
      val = board[ (i, j) ]
      if val in rows or val == '.': return False
      rows.add(val)
      val = board[ (j,i) ]
      if val in cols: return False
      cols.add(val)
  #
  for i in range(3):
    for j in range(3):
      tQuad = set()
      for k in range(3):
        for m in range(3):
          val = board[ (3*i+k,3*j+m) ]
          if val in tQuad: return False
          tQuad.add(val)
          #
        #
      #
    #
  #
  return True
#
#
#
'''      --CHECKS IF THE isCorrect() is correct--
print(lines[0])
board = makeBoard(lines[0])
printBoard(board)
print(isCorrect(board))
board[(0,0)] = '4'
printBoard(board)
print(isCorrect(board))
'''
#
#
#
#
#
#
def isWrong(board):
  rowsCorrect = True
  colsCorrect = True
  quadsCorrect = True
  #
  for i in range(9):
    rows = set()
    cols = set()
    for j in range(9):
      val = board[ (i, j) ]
      if val in rows and val != '.': return True
      rows.add(val)
      val = board[ (j,i) ]
      if val in cols and val != '.': return True
      cols.add(val)
  #
  for i in range(3):
    for j in range(3):
      tQuad = set()
      for k in range(3):
        for m in range(3):
          val = board[ (3*i+k,3*j+m) ]
          if val in tQuad and val != '.': return True
          tQuad.add(val)
          #
        #
  
  #
    #
  #
  return False
#
#
#
'''      --CHECKS IF THE isWrong() is correct--
print(lines[0])
board = makeBoard(lines[0])
printBoard(board)
print(isWrong(board))
board[(0,0)] = '7'
printBoard(board)
print(isWrong(board))
'''
#
#
#
#          ~~EASY ONES~~
def recursiveSolve(b,p):        #return a tuple of the form (boolean, board)
  if isCorrect(b): return (True,b)
  if isWrong(b): return (False,b)
  #
  #printBoard(b)
  #print()
  #
  pair = (8,8)
  for r in range(9):
    for c in range(9):
      if b[r,c] == '.': pair = (r,c)
    nB = b
    nB[pair]=n
    nP = makePossibilities(b)
    ans,bo = recursiveSolve(b,nP)
    if ans: return (True,bo)
    #
  print('returned by default')  
  return (False,b)
#
#
#
#
#
#
def pqHelper(b,pq):
  if isCorrect(b): return (True, b)
  if isWrong(b): return (False,b)
  #
  numPoss,coordinates,possibilities = heapq.heappop(pq)
  while b[coordinates] != '.': numPoss,coordinates,possibilities = heapq.heappop(pq)
  newBoard = {}
  #newPQ = []
  #if numPoss ==0:
  #print(numPoss,'\t',coordinates,'\t',possibilities)
  cR,cC = coordinates
  nbrs = findNeighbors(b,cR,cC)
  for n in possibilities:
    newBoard = b
    newBoard[coordinates] = n
    newPQ = []
    for i in pq:
      nPoss,tC,poss = i
      if tC in nbrs and n in poss:
        poss.remove(n)
        nPoss -= 1
      heapq.heappush(newPQ, ( nPoss,tC,poss ) )  
    ans,bo = pqHelper(newBoard,newPQ)
    if ans: return (True,bo)
  return (False,b)
  #
#
def dictHelper(b,d):                                                            #THIS WORKS
  if isCorrect(b): return (True,b)
  if isWrong(b): return (False,b)
  #
  minC = (-1,-1)
  minNum = 10
  minSet = set()
  for c in ALL_COORDINATES:
    if b[c] == '.':
      tNum,tSet = d[c]
      if tNum < minNum: 
        minC = c
        minNum = tNum
        minSet = tSet
        #
      #
    #
  #
  if minNum == 10: print("minNum stil 10")
  #
  minCR,minCC = minC
  finalSet = minSet
  #print('begain: ',minSet,'\nCoordinates: ',minC)
  #if len(finalSet)>1: print('HAD TO GUESS')
  for eachPossibility in finalSet:
    newD = deepcopy(d)
    newB = deepcopy(b)
    #newD=d
    #newB=b
    #replace your dictionary with a one dimension list where the index is just 9*r+c...
    #newD = d[:]
    #newB =b[:]
    newB[minC] = eachPossibility
    for eachNeighbor in findNeighbors(newB,minCR,minCC):
      thNum,thSet = newD[eachNeighbor]
      if eachNeighbor != minC and eachPossibility in thSet:
        newSet = thSet
        newSet.remove(eachPossibility)
        thNum -= 1
        newD[eachNeighbor] = (thNum,newSet)
        #
      #
    #
    ans,bo = dictHelper(newB,newD)
    if ans:
      #print('GUESSED RIGHT')
      return (True,bo)
    #print('GUESSED WRONG')
    #print('end: ',minSet)
    #
  #
  return (False,b)
  #  
#
def dictHelper2(b,p,nums):                                                        #SUPAH FAST 
  if isCorrect(b): return (True,b)
  if isWrong(b): return (False,b)
  #
  minC = (-1,-1)
  minNum = 10
  minSet = set()
  for c in ALL_COORDINATES:
      #print(b[c])
      #if p[c]: return(False,b)
      if b[c] == '.' and nums[c] < minNum: 
        minC = c
        minNum = nums[c]
        minSet = p[c]
        #
      #
    #
  #
  if minNum == 10: print("minNum stil 10")
  #
  minCR,minCC = minC
  for eachPossibility in minSet.copy():
    rmList=[]
    b[minC]=eachPossibility
    for eachNeighbor in findNeighbors(b,minCR,minCC):
      if eachNeighbor != minC and eachPossibility in p[eachNeighbor]:
        rmList.append(eachNeighbor)
        newSet = p[eachNeighbor]
        newSet.remove(eachPossibility)
        p[eachNeighbor]=newSet
        newN = nums[eachNeighbor] 
        newN-= 1
        nums[eachNeighbor]=newN 
        #
      #
    #
    ans,bo = dictHelper2(b,p,nums)
    if ans:return (True,bo)
    #
    guess=b[minC]
    b[minC]='.'
    for changed in rmList:
      nSet=p[changed]
      nSet.add(guess)
      p[changed]=nSet
      nN=nums[changed]
      nN+=1
      nums[changed]=nN
    #
  #
  return (False,b)
  #  
#
#
def dictHelper3(b,p,nums):                                                        #THIS DOESN'T WORK 
  if isCorrect(b): return (True,b)
  if isWrong(b): return (False,b)
  #
  minC = (-1,-1)
  minNum = 10
  minSet = set()
  for c in ALL_COORDINATES:
      #print(b[c])
      #if p[c]: return(False,b)
      if b[c] == '.' and nums[c] < minNum: 
        minC = c
        minNum = nums[c]
        minSet = p[c]
        #
      #
    #
  #
  if minNum == 10: print("minNum stil 10")
  #
  minCR,minCC = minC
  for eachPossibility in minSet.copy():
    rmList=[]
    oldP=p
    b[minC]=eachPossibility
    for eachNeighbor in findNeighbors(b,minCR,minCC):
      if eachNeighbor != minC and eachPossibility in p[eachNeighbor]:
        rmList.append(eachNeighbor)
        newN = nums[eachNeighbor]
        newN-= 1
        nums[eachNeighbor]=newN 
        #
      #
    p=makePossibilities3(b)
    #
    ans,bo = dictHelper2(b,p,nums)
    if ans:return (True,bo)
    #
    guess=b[minC]
    b[minC]='.'
    for changed in rmList:
      nN=nums[changed]
      nN+=1
      nums[changed]=nN
    p=oldP
    #
  #
  return (False,b)
  #  
#
#
#
#
#
def priorityQueueAttempt(b,p):
  pq = []                           # priority queue of tuples with following structure: ( number of possibilites, coordinates ,set of possibilities)
  for pCoord in b.keys():
    pTuple = ( len(p[pCoord]),pCoord,p[pCoord])
    heapq.heappush(pq,pTuple)
  return pqHelper(b,pq)
#
#
def dictionaryAttempt(b,p):
  d = {}                       # dictionary with key of (r,c) and value of tuple (number of possiblities, set of possibilities)
  for c in b.keys():
    d[c] = (len(p[c]), p[c])
  return dictHelper(b,d)
#
#
#
def dictionaryAttempt2(b,p):
  newB=b                       # dict of value  SUPAH FAST
  #nbrs={}
  nums={}
  for c in b.keys():
    #nbrs[c]=p[c]
    nums[c]=len(p[c])
  #print(nbrs)
  return dictHelper2(newB,p,nums)
#
#
def dictionaryAttempt3(b,p):
  newB=b                       # dict of value  SUPAH FAST
  #nbrs={}
  nums={}
  for c in b.keys():
    #nbrs[c]=p[c]
    nums[c]=len(p[c])
  #print(nbrs)
  return dictHelper2(newB,p,nums)
#
#
#
#
#
def makePossibilities(board):
  neighbors ={}
  for r in range(9):
    for c in range(9):
      toAdd = set() 
      allTheNeighbors = findNeighbors(board,r,c)  #set containing all tuple coordinates of nbrs
      neighborValues = set()
      for i in allTheNeighbors:
        #print('Value of ',i,': ',board[i])
        if board[i] is not '.':neighborValues.add(board[i])
      #print(neighborValues)
      for j in range(1,10):
        #print(j, '/t',neighborValues)
        if str(j) not in neighborValues: toAdd.add(str(j))
      #
      #if 0 in toAdd: toAdd.remove(0)
      neighbors[ (r,c) ] = toAdd
    #
  #
  return neighbors
#
#
def makePossibilities3(board):
  neighbors ={}
  for r in range(9):
    for c in range(9):
      toAdd = set() 
      allTheNeighbors = findNeighbors(board,r,c)  #set containing all tuple coordinates of nbrs
      neighborValues = set()
      for i in allTheNeighbors:
        if board[i] is not '.':neighborValues.add(board[i])
      for j in range(1,10):
        if str(j) not in neighborValues: toAdd.add(str(j))
      #
      neighbors[ (r,c) ] = toAdd
    #
  #
  #ADD STUFF/MAKE MORE EFFICIENT
  #for r in range(9):
  #
  #
  #
  return neighbors
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
'''
i = 72
for i in range(10)
print(lines[i])
b = makeBoard(lines[i])
printBoard(b)
p = makePossibilities(b)
#print(p[(8,3)])
ans,bo = dictionaryAttempt(b,p)
print('\nResults: ',ans)
printBoard(bo)
'''
#
#
#'''
out = open('sudokuOutput.txt','w')
ls = []                                          #tuples of form ( time, number , originalboard, finished board )
'''
for i in range(18):
  print('---------- #',i+1,' ----------')
  b = makeBoard(lines[i])
  print(lines[i])
  printBoard(b)
  p = makePossibilities(b)
  #print(p[(0,0)])
  s = time()
  ans,board = dictionaryAttempt2(b,p)
  e = time()
  #while not ans: ans,board = priorityQueueAttempt(b,p)
  print('\nResults: ',ans)
  printBoard(board)
  heapq.heappush(ls, ((e-s)**-1,i+1,b,board)  )
  print('Time: ',e-s)
  print()
  print()
  #
print('\n\n\n~~~~~~~~~~ RESULTS ~~~~~~~~~~')
for i in range(3):
  t,n,orig,fin = heapq.heappop(ls)
  s=str( n) + ': ' +str(t**-1)
  print(s)
  out.write(s+'\n')
  printBoard(orig)
  print()
  printBoard(fin)
  print()
  print()
  #
'''
START = time()
for i in range(128):
  b = makeBoard(lines[i])
  p = makePossibilities(b)
  s = time()
  ans,bo= dictionaryAttempt2(b,p)
  e = time()
  heapq.heappush(ls,((e-s)**-1,i+1,b,bo  ))
  print(str(i+1),': ',ans,'\t\t','Time: ',str(e-s),'\t\tTotal: ',e-START)
print('\n\n\n~~~~~~~~~~ RESULTS ~~~~~~~~~~')
for i in range(3):
  t,n,orig,fin = heapq.heappop(ls)
  s=str( n) + ': ' +str(t**-1)
  print(s)
  out.write(s+'\n')
  #
out.close()
#'''
#
#
#
#          ~~NOTES~~
#   > Base Case 1: found solution.  (return stuff, something good)
#   > Base Case 2: determined that we guessed wrong (return false, etc)
#         - if the most constrained slot has zero options
#   > Recursive Case: pick an empty slot, loop over possibilites, try each one and recur down that side tree.
#         - return each recursive call using OR
#   > If none work, return false.
#
#
#
#I CAN COPY AND PASTE
#
#
# End of File
