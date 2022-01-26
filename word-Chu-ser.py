"""
Written by Michael Chu
https://github.com/TheChuChuTrain
"""
import sys

wordList = 'sowpods.txt'

# parse args
inputLetters = sys.argv[1]
letters = inputLetters.replace('-', '')

# number of required wildcards
wildRequired = len(inputLetters) - len(letters)
letters = letters.replace('_', '')

# total number of wild cards we have
numWild = len(inputLetters) - len(letters)

# number of letters we must use
mustUse = sorted([i for i in letters if i.isupper()])
lowerLetters = ''.join(sorted(letters.lower()))
letters = ''
idx = 0

# We need sorted letters, but keeping uppercase letters
for i in range(len(lowerLetters)):
  if idx < len(mustUse) and mustUse[idx].lower() == lowerLetters[i]:
    letters += mustUse[idx]
    idx += 1
  else:
    letters += lowerLetters[i]
letterScores = {}
maxLength = 99
minLength = 2
toMatch = None
split = False
wwf = False
scoreSet = False
exactLength = None
cantUse = set()

# Set initial letter scores, the default value for each letter is 1
for i in range(ord('a'), ord('z') + 1):
  letterScores[chr(i)] = 1

for arg in sys.argv[2:]:
  if arg[0] == '-':
    maxLength = int(arg[1:])
  elif arg[0] == '+':
    minLength = int(arg[1:])
  elif arg[0] == '^':
    toMatch = arg[1:].lower()
    exactLength = len(toMatch)
  elif arg[0] == '%':
    split = True
  elif arg[0] == '#':
    cantUse = set(arg[1:])
  elif arg == 'wwf':
    wwf = True
    scoreSet = True
    wordList = 'enable1.txt'
  else:
    letterScores[arg[0].lower()] = float(arg[1:])
    scoreSet = True
if wwf:
  letterScores = {'a':1,'b':4,'c':4,'d':2,'e':1,'f':4,'g':3,'h':3,'i':1,'j':10,'k':5,'l':2,'m':4,'n':2,'o':1,'p':4,'q':10,'r':1,'s':1,'t':1,'u':2,'v':5,'w':4,'x':8,'y':3,'z':10}

bestScore = 0
bestWord = []

allWords = open(wordList)
# go through entire dictionary
for l in allWords:
  valid = True
  l = l.rstrip().lower()
  if len(l) != exactLength:
    continue
  if len(l) > maxLength:
    continue
  if len(l) < minLength:
    continue
  for i in range(len(l)):
    if toMatch != None and toMatch[i] != '_' and toMatch[i] != l[i]:
      valid = False
      break
    if l[i] in cantUse:
      valid = False
      break
  if not valid:
    continue

  currLetters = ''.join(sorted(l))
  letterIndex = 0
  currIndex = 0
  currScore = 0
  numMustUsed = 0
  possibleWild = 0
  wildUsed = 0
  # letters is what we need to use(sorted) currLetters is what letters are in the word we're checking.
  # zip letters together keeping track of how many wild letters we use
  while valid and currIndex < len(currLetters):

    # if we still have required letters left
    if letterIndex < len(letters):
      # if the letter matches
      if letters[letterIndex].lower() == currLetters[currIndex]:
        currScore += letterScores[letters[letterIndex].lower()]
        if letters[letterIndex].isupper():
          numMustUsed += 1
        letterIndex += 1
        currIndex += 1
        possibleWild += 1
      # if we have a letter not in the current word
      elif letters[letterIndex].islower() and letters[letterIndex] < currLetters[currIndex]:
        letterIndex += 1
      # use a wildcard
      elif wildUsed < numWild:
        wildUsed += 1
        currIndex += 1
      # no options left
      else:
        valid = False

    # no letters left, use wildcards
    elif wildUsed < numWild:
      wildUsed += 1
      currIndex += 1
    else:
      valid = False

    # if it is the end of the word
    if currIndex == len(currLetters):
      # check for if we've used all of the required options
      if not numMustUsed == len(mustUse) or possibleWild + wildUsed < wildRequired:
        valid = False

  # calculate best scoring words
  if valid and currIndex == len(currLetters):
    if exactLength is None or len(currLetters) == exactLength:
      if currScore > bestScore:
        bestScore = currScore
        bestWord = [l]
      elif currScore == bestScore:
        bestWord.append(l)

print 'Best score:', bestScore
for word in bestWord:
  print word, len(word)
