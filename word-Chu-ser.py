"""
Written by Michael Chu
https://github.com/TheChuChuTrain
"""
import sys

wordList = 'sowpods.txt'

# parse args
inputLetters = sys.argv[1]
letters = inputLetters.replace('-', '')
wildRequired = len(inputLetters) - len(letters)
letters = letters.replace('_', '')
numWild = len(inputLetters) - len(letters)
mustUse = sorted([i for i in letters if i.isupper()])
lowerLetters = ''.join(sorted(letters.lower()))
letters = ''
idx = 0
for i in range(len(lowerLetters)):
  if idx < len(mustUse) and mustUse[idx].lower() == lowerLetters[i]:
    letters += mustUse[idx]
    idx += 1
  else:
    letters += lowerLetters[i]
letterScores = {}
maxLength = 99
toMatch = ''
split = False
wwf = False
scoreSet = False

# Set initial letter scores, the default value for each letter is 1
for i in range(ord('a'), ord('z') + 1):
  letterScores[chr(i)] = 1

for arg in sys.argv[2:]:
  if arg[0] == '-':
    maxLength = int(arg[1:])
  elif arg[0] == '^':
    toMatch = arg[1:].lower()
    maxLength = len(toMatch)
  elif arg[0] == '%':
    split = True
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

dict = open(wordList)
# go through entire dictionary
for l in dict:
  l = l.rstrip().lower()
  currLetters = ''.join(sorted(l))
  letterIndex = 0
  currIndex = 0
  currScore = 0
  valid = True
  numMustUsed = 0
  possibleWild = 0
  wildUsed = 0
  while True:
    # not a required letter
    if letters[letterIndex].islower():
      # if the letter matches
      if letters[letterIndex] == currLetters[currIndex]:
        currScore += letterScores[letters[letterIndex]]
        letterIndex += 1
        currIndex += 1
        possibleWild += 1
      # if we have a letter not in the current word
      elif letters[letterIndex] < currLetters[currIndex]:
        letterIndex += 1
      # if there's a letter in the word that isn't in our letters
      elif wildUsed < numWild:
        wildUsed += 1
        currIndex += 1
      # out of options, not a valid word
      else:
        valid = False
        break
    # required to be used letters
    else:
      # if the letter matches
      if letters[letterIndex].lower() == currLetters[currIndex]:
        currScore += letterScores[letters[letterIndex].lower()]
        letterIndex += 1
        currIndex += 1
        numMustUsed += 1
      elif wildUsed < numWild:
        wildUsed += 1
        currIndex += 1
      else:
        valid = False
        break
    # check for the end of the word
    if letterIndex == len(letters) or currIndex == len(currLetters):
      if not numMustUsed == len(mustUse) or possibleWild + wildUsed < wildRequired:
        valid = False
      break

  # calculate best scoring words
  if valid and currIndex == len(currLetters) and len(currLetters) <= maxLength:
    if currScore > bestScore:
      bestScore = currScore
      bestWord = [l]
    elif currScore == bestScore:
      bestWord.append(l)

print 'Best score:', bestScore
for word in bestWord:
  skip = False
  if len(toMatch) != 0 and len(word) == len(toMatch):
    for i in range(len(word)):
      if not toMatch[i] == '_' and not toMatch[i] == word[i]:
        skip = True
        break
  if skip:
    continue
  print word, len(word)
