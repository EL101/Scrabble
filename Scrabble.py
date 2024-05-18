import requests
import random
import copy

#values of a square (negative = letter mult, positive = word mult)
value = [[3, 1, 1, -2, 1, 1, 1, 3, 1, 1, 1, -2, 1, 1, 3],
[0, 2, 1, 1, 1, -3, 1, 1, 1, -3, 1, 1, 1, 2, 1],
[0, 0, 2, 1, 1, 1, -2, 1, -2, 1, 1, 1, 2, 1, 1],
[-2, 1, 1, 2, 1, 1, 1, -2, 1, 1, 1, 2, 1, 1, -2],
[1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
[1, -3, 1, 1, 1, -3, 1, 1, 1, -3, 1, 1, 1, -3, 1],
[1, 1, -2, 1, 1, 1, -2, 1, -2, 1, 1, 1, -2, 1, 1],
[3, 1, 1, -2, 1, 1, 1, 1, 1, 1, 1, -2, 1, 1, 3],
[1, 1, -2, 1, 1, 1, -2, 1, -2, 1, 1, 1, -2, 1, 1],
[1, -3, 1, 1, 1, -3, 1, 1, 1, -3, 1, 1, 1, -3, 1],
[1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
[-2, 1, 1, 2, 1, 1, 1, -2, 1, 1, 1, 2, 1, 1, -2],
[0, 0, 2, 1, 1, 1, -2, 1, -2, 1, 1, 1, 2, 1, 1],
[0, 2, 1, 1, 1, -3, 1, 1, 1, -3, 1, 1, 1, 2, 1],
[3, 1, 1, -2, 1, 1, 1, 3, 1, 1, 1, -2, 1, 1, 3]]

#how much each letter is worth
points = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

#how many of each letter there are (Blanks can be used for any word)
bruhbag = {'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1, ' ': 2}

#getting the words from website
website="https://raw.githubusercontent.com/jesstess/Scrabble/master/scrabble/sowpods.txt"
response = requests.get(website).text
WORDS=list(response.split("\n"))
valid={}
for i in WORDS:
  valid[i]=True
#empty bag
def newBag():
  dict={}
  str="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
  for i in str:
    dict[i]=0
  return dict

def newRack(num):
  currBag=[]
  for letter in bruhbag:
    for i in range(bruhbag[letter]):
      currBag.append(letter)
  rack=random.sample(currBag, num)
  for i in rack:
    bruhbag[i]-=1
  return rack

def removeBag(bag):
  for i in bag:
    bruhbag[i]-=1
  return
#calculates the value of the word if we were to place it on the board
def wordValue(word, x1, y1, x2, y2, board):
  wordPoints=0
  wordMult=1
  if (x1==x2):
    i=y1
    while (i<=y2):
      if (value[x1-1][i-1]>0):
        wordMult*=value[x1-1][i-1]
        wordPoints+=points[word[i-y1]]
      else:
        wordPoints+=points[word[i-y1]]*abs(value[x1-1][i-1])
      i+=1
    wordPoints*=wordMult
  else:
    i=x1
    while (i<=x2):
      if (value[i-1][y1-1]>0):
        wordMult*=value[i-1][y1-1]
        wordPoints+=points[word[i-x1]]
      else:
        wordPoints+=points[word[i-x1]]*abs(value[i-1][y1-1])
      i+=1
    wordPoints*=wordMult
  return wordPoints

#places the word onto the board
def enterWord(word, x1, y1, x2, y2, board):
  if (x1==x2):
    i=y1
    while (i<=y2):
      board[x1-1][i-1]=word[i-y1]
      i+=1
  else:
    i=x1
    while (i<=x2):
      board[i-1][y1-1]=word[i-x1]
      i+=1
  return board

#setting up the board
def newBoard(board):
  for i in range(15):
    L=[]
    for j in range(15):
      L.append('_')
    board.append(L)
  return board


#displaying the board
def printBoard(board):
  for i in board:
    s=' '.join(str(x) for x in i)
    print(s)

def updateBag(bag, word):
  for i in word:
    if (bag[i]==0):
      bag[' ']-=1
    else:
      bag[i]-=1
  return bag

def validWord(rack, board, word, startx, starty, endx, endy):
  copyBoard=copy.deepcopy(board)
  dict=newBag()
  for i in rack:
    dict[i]+=1
  for i in word:
    dict[i]-=1
    if (dict[i]<0):
      return False
  if (startx==endx):
    for i in range(starty, endy+1):
      if (board[startx][i]!='_' and board[startx][i]!=word[i-starty]):
        return False
      copyBoard[startx][i]=word[i-starty]
  for i in range(0, 15):
    index=0
    while (index<15):
      str=""
      while (copyBoard[i][index]!='_'):
        str+=copyBoard[i][index]
        index+=1
      if (str!="" and valid.get(str)==0):
        return False
      index+=1
    index=0
    while (index<15):
      str=""
      while (copyBoard[index][i]!='_'):
        str+=copyBoard[i][index]
        index+=1
      if (str!="" and valid.get(str)==0):
        return False
      index+=1
  return True
#this calculates the most optimal word to choose as you're first word
def initialMove(board, rack):
  maxi=0
  maxWord=0
  initialx=0
  initialy=0
  finalx=0
  finaly=0
  for i in WORDS:
    wordPoints=0
    startx=0
    starty=0
    endx=0
    endy=0
    if (len(i)<8):
      startx=8
      starty=8-len(i)+1
      endx=8
      endy=8
    elif (len(i)==8):
      startx=7
      starty=1
      endx=8
      endy=8
    elif (len(i)<=12):
      startx=8
      starty=4
      endx=8
      endy=4+len(i)-1
    else:
      startx=8
      starty=15-len(i)+1
      endx=8
      endy=15
    if (validWord(rack, board, i, startx, starty, endx, endy)):
      print(i)
      wordPoints=wordValue(i, startx, starty, endx, endy, board)
    if (wordPoints>maxi):
      maxWord=i
      maxi=wordPoints
      initialx=startx
      initialy=starty
      finalx=endx
      finaly=endy
  printBoard(board)
  enterWord(maxWord, initialx, initialy, finalx, finaly, board)
  print(maxWord)
  for i in maxWord:
    rack.remove(i)
  rack+=newRack(len(maxWord))
  return wordValue(maxWord, initialx, initialy, finalx, finaly, board)

first=input("Who goes first? (me/opp) ")
#this starts the game
def play(oppPoints, myPoints, board, move, rack):
  print("Rack: ", rack)

  #handles the case where it's the opponent's turn
  if ((first=="me" and move%2==1) or (first=="opp" and move%2==0)):
    print("It's the opponent's move! Give some info on their move.")
    oppRack=[i for i in input("What new letters did your opponent put in his rack? ").split()]
    removeBag(oppRack)
    word=input("What word did you're opponent choose? ")
    if (word!="skipped"):
      print("What coords? (startx, starty, dir)")
      x1=int(input())
      y1=int(input())
      dir=input()
      if (dir=="up"):
        oppPoints+=wordValue(word, x1, y1, x1+len(word)-1, y1, board)
        board=enterWord(word, x1, y1, x1+len(word)-1, y1, board)
      else:
        oppPoints+=wordValue(word, x1, y1, x1, y1+len(word)-1, board)
        board=enterWord(word, x1, y1, x1, y1+len(word)-1, board)
  #handles the case where it's your turn
  else:
    #if it's the initial move
    if (move==0):
      print("You are the first to go. Computer has made good move for you!")
      L=initialMove(board, rack)
      myPoints+=L
    #if it's not the initial move
    else:
      print("It's your move! How do you want to play?")
      print("Move info (x, y, dir): ")
      x=int(input())
      y=int(input())
      dir=input()
      initialx=-1
      initialy=-1
      maxPoints=0
      maxWord="_"
      for i in WORDS:
        positions=[]
        for j in range(len(i)):
          if (i[j]==board[x-1][y-1]):
            positions.append(j)
        if (dir=="up"):
          for j in positions:
            startx=x-j
            starty=y
            if (startx<=0 or (startx+len(i))>15):
              continue
            prevBoard=board
            wordPoints=0
            if (validWord(rack, board, i, startx, starty, startx+len(i)-1, starty)):
              wordPoints=wordValue(i, startx, starty, startx+len(i)-1, starty, board)
            if (maxPoints<wordPoints):
              maxPoints=wordPoints
              maxWord=i
              initialx=startx
              initialy=starty
            else:
              board=prevBoard
        else:
          for j in positions:
            startx=x
            starty=y-j
            if (starty<=0 or (starty+len(i))>15):
              continue
            prevBoard=board
            wordPoints=0
            if (validWord(rack, board, i, startx, starty, startx, starty+len(i)-1)):
              wordPoints=wordValue(i, startx, starty, startx, starty+len(i)-1, board)
            if (maxPoints<wordPoints):
              maxPoints=wordPoints
              maxWord=i
              initialx=startx
              initialy=starty
            else:
              board=prevBoard
      if (maxWord=="_"):
        print("There is no word that works here! OOF :(")
      else:
        if (dir=="up"):
          board=enterWord(maxWord, initialx, initialy, initialx+len(maxWord)-1, initialy, board)
          myPoints+=wordValue(maxWord, initialx, initialy, initialx+len(maxWord)-1, initialy, board)
        else:
          board=enterWord(maxWord, initialx, initialy, initialx, initialy+len(maxWord)-1, board)
          myPoints+=wordValue(maxWord, initialx, initialy, initialx, initialy+len(maxWord)-1, board)
        for letter in maxWord:
          rack.remove(letter)
        rack+=newRack(len(maxWord))
  printBoard(board)
  print("My points: ", myPoints)
  print("Opponent points: ", oppPoints)
  play(oppPoints, myPoints, board, move+1, rack)

play(0, 0, newBoard([]), 0, newRack(7))