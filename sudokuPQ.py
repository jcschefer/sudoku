# Jack Schefer, pd. 6
#
import heapq
from time import time
from copy import deepcopy
#
def blankBoard():
  board = ['.' for i in range(81)]
  return board
#
#
ALL_COORDINATES = []
for i in range(9):
  for j in range(9):
    ALL_COORDINATES.append( (i,j) )
#
def makeBoard(string):
  b = blankBoard()
  for i in range(len(b)): b[i] = string[i]
  return b
#
#
#
def printBoard(b):
  for r in range(9):
    s = ''
    for c in range(9):
      s += b[ 9 * r + c]
      s += ' '
    print(s)
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
    if i != row: nbrs.add( 9 * i + col )
    if i != col: nbrs.add( 9 * row + i )
  #
  rowQuad = row // 3
  colQuad = col // 3
  for i in range(3):
    for j in range(3):
      nR = i+rowQuad*3
      nC = j+colQuad*3
      nP = 9 * nR + nC
      if nR != row and nC != col and nP not in nbrs: nbrs.add( nP) 
  #
  return nbrs
#
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
      val = board[ 9 * i + j ]
      if val in rows or val == '.': return False
      rows.add(val)
      val = board[ 9 * j  + i ]
      if val in cols: return False
      cols.add(val)
  #
  for i in range(3):
    for j in range(3):
      tQuad = set()
      for k in range(3):
        for m in range(3):
          val = board[ 9 * (3*i+k) + 3 * j + m ]
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
      val = board[ 9 * i + j ]
      if val in rows and val != '.': return True
      rows.add(val)
      val = board[ 9 * j + i ]
      if val in cols and val != '.': return True
      cols.add(val)
  #
  for i in range(3):
    for j in range(3):
      tQuad = set()
      for k in range(3):
        for m in range(3):
          val = board[ 9 * (3*i+k) + 3 * j + m ]
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
#
#
#
#
def pqHelper(b,p,nums):                                                        #SUPAH FAST 
  if isCorrect(b): return (True,b)              # b --> the board array
  if isWrong(b): return (False,b)               # p --> the possibilities dictionary
  #                                             # nums -->  the pq of tuples (numPossible, coordinate)
  try: minNum, minC = heapq.heappop(nums)
  except IndexError:
    return (False, b)
  #
  numCopy = nums[:]
  minSet = p[minC]
  minCR = minC // 9
  minCC = minC %  9
  for eachPossibility in minSet.copy():
    #numCopy = nums[:]
    rmList=[]
    b[minC] = eachPossibility
    nbrs = findNeighbors(b, minCR, minCC)
    #
    # replace num poss heap
    for i in range(len(nums)):
      np, coord = nums[i]
      nN = np
      if coord in nbrs and eachPossibility in p[coord]:
        nN -= 1 
        #
      nums[i] = (nN, coord)
      #
    #
    heapq.heapify(nums)
    #
    # replace the possibilities dict
    for eachNeighbor in nbrs:
      if eachNeighbor != minC and eachPossibility in p[eachNeighbor]:
        rmList.append(eachNeighbor)
        newSet = p[eachNeighbor]
        newSet.remove(eachPossibility)
        p[eachNeighbor] = newSet
        #
      #
    #
    ans,bo = pqHelper(b,p,nums)
    if ans:return (True,bo)
    #
    guess = b[minC]     # the incorrect guess
    b[minC] = '.'
    nums = numCopy[:]
    for changed in rmList:
      nSet = p[changed]
      nSet.add(guess)
      p[changed] = nSet
      #
      #nN = nums[changed]
      #nN += 1
      #nums[changed]=nN
    #
    for i in range(len(nums)):
      np, coor = nums[i]
      #nN = np
      #if i in rmList:
      #  nN += 1
      #
      #nums[i] = (nN, coor)
      #
      nums[i] = ( len(p[coor]) , coor )
      #
    #
    heapq.heapify(nums)
    #
  #
  return (False,b)
  #  
#
#
#
#
def pqSolve(b,p):
  newB=b                       # dict of value  SUPAH FAST
  nums = []
  for c in range(81):
    if newB[c] == '.': heapq.heappush(nums, (len(p[c]), c)  )
  return pqHelper(newB,p,nums)
#
#
#
#
def makePossibilities(board):
  neighbors = {}
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
      neighbors[ 9 * r + c  ] = toAdd
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
  ans,bo= pqSolve(b,p)
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
