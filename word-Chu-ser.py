import sys
dict = open("sowpods.txt")


letters = sys.argv[1]

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
  else:
    letterScores[arg[0].lower()] = int(arg[1:])

bestScore = 0
bestWord = []

for l in dict:
  l = l.rstrip().lower()
  currLetters = ''.join(sorted(l))
  letterIndex = 0
  currIndex = 0
  currScore = 0
  valid = True
  numMustUsed = 0
  while True:
    #not a required letter
    if letters[letterIndex].islower():
      if letters[letterIndex] == currLetters[currIndex]:
        currScore += letterScores[letters[letterIndex]]
        letterIndex += 1
        currIndex += 1
      elif letters[letterIndex] < currLetters[currIndex]:
        letterIndex += 1
      else:
        valid = False
        break
      if letterIndex == len(letters) or currIndex == len(currLetters):
        if not numMustUsed == len(mustUse):
          valid = False
        break
    #required to be used
    else:
      if letters[letterIndex].lower() == currLetters[currIndex]:
        currScore += letterScores[letters[letterIndex].lower()]
        letterIndex += 1
        currIndex += 1
        numMustUsed += 1
      else:
        valid = False
        break
      if letterIndex == len(letters) or currIndex == len(currLetters):
        if not numMustUsed == len(mustUse):
          valid = False
        break

  if valid and currIndex == len(currLetters) and len(currLetters) <= maxLength:
    if currScore > bestScore:
      bestScore = currScore
      bestWord = [l]
    elif currScore == bestScore:
      bestWord.append(l)

for word in bestWord:
  skip = False
  if len(toMatch) != 0 and len(word) == len(toMatch):
    for i in range(len(word)):
      if not toMatch[i] == '_' and not toMatch[i] == word[i]:
        skip = True
        break
  if skip:
    continue
  print word, 'length:', len(word)





  
