# Jack Schefer, pd. 6
#
from time import time
from sys  import argv
#
# not used
def blankBoard():
  board = ['.' for i in range(81)]
  return board
#
#
ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
ALL_COORDINATES = []
for i in range(81):
  ALL_COORDINATES.append( ROWS[i // 9] + str(i % 9) )
#
########################################################################################
#
def cross(A, B):
  return [a + b for a in A for b in B]
  #
#
########################################################################################
#
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789'  ]])
print(unitlist)
#
units = dict( (s, [u for u in unitlist if s in u]) for s in squares)
peers = dict( (s, set(sum(units[s],[])) - set([s])) for s in squares )
#
########################################################################################
#
def eliminate(values, s, d):
  #
  if d not in values[s]: return values
  #
  values[s] = values[s].replace(d, '')
  #
  if len(values[s]) == 0:  # contradiction
    return False
  #
  elif len(values[s]) == 1: 
    d2 = values[s]
    if not all(eliminate(values, s2, d2) for s2 in peers[s]):
      return False
  #
  for u in units[s]:
    dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0: return False
    elif len(dplaces) == 1:
      if not assign(values, dplaces[0], d): return False
    #
  #
  return values
  #
#
#####################################################################################
#
def assign(values, s, d):
  #
  other_values = values[s].replace(d, '')
  #
  if all(eliminate(values, s, d2) for d2 in other_values): return values
  else: return False
  #
#
#####################################################################################
#
#conver string to dictionary of values
def grid_values(grid):
  chars = [c for c in grid if c in digits or c in '0.']
  assert len(chars) == 81
  return dict(zip(squares, chars))
  #
#
#######################################################################################
#
def parse_grid(grid):
  values = dict( (s, digits) for s in squares )
  for s,d in grid_values(grid).items():
    if d in digits and not assign(values, s, d):
      return False
      #
    #
  #
  return values
  #
#
####################################################################################
#
#
#'''    --- CHECKS TO PRINT OUT PUZZLE CORRECTLY
s = list(open('sudoku128.txt'))
lines = []
for l in s:
  lines.append(l.rstrip())
#
###################################################################################
#
def display(values):
  width = 1 + max(len(values[s]) for s in squares)
  line = '+'.join(['-' * (width * 3)] * 3)
  for r in rows:
    print( ''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols ))
    if r in 'CF': print(line)
    #
  #
  print()
  #
#
###################################################################################
#
def solve(grid):
  return search(parse_grid(grid))
#
###################################################################################
#
def search(values):
  if values is False: return False
  #
  if all(len(values[s]) == 1 for s in squares): return values
  #
  n,s = min( (len(values[s]), s) for s in squares if len(values[s]) > 1)
  return some( search(assign(values.copy(), s, d)) for d in values[s])
  #
#
###################################################################################
#
def some(seq):
  for e in seq:
    if e: return e
  return False
  #
#
###################################################################################
#        ~~~ MAIN ~~~
#
out = open('sudokuOutput.txt','w')
ls = []                                          #tuples of form ( time, number , originalboard, finished board )
#
START = time()
N = 128
if len(argv) > 1: N = int(argv[1])
'''
for i in range(N):
  b = makeBoard(lines[i])
  p = makePossibilities(b)
  s = time()
  ans,bo= dictSolve(b,p)
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
'''
#
for i in range(N):
  print(i)
  print(lines[i])
  display(solve(lines[i]))
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
