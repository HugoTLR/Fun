import argparse
from genetic import *
from collections import Counter
from copy import deepcopy



def visu(square):
  res = ""
  for row in square:
    res = res + '\t'.join([str(r) for r in row]) + "\n"
  return res

def squarify(ch):
  sqr = [[0 for _ in range(ch.size)] for _ in range(ch.size)]
  for j in range(ch.size):
    for i in range(ch.size):
      # print(f"{j=},{i=} {str(ch)}")
      v = ch.genes[j*ch.size+i].val
      sqr[j][i] = v
  return sqr

def transpose(square):
  return [list(i) for i in zip(*square)]

def verify(square):
  numbers = []
  value = None
  for row in square:
    if value == None:
      value = sum(row)
    else:
      if sum(row) != value:
        return False

    for col in row:
      if col not in numbers:
        numbers.append(col)
      else:
        return False

  t_square = transpose(square)
  for row in t_square:
    if sum(row) != value:
      return False

  diag1 = [square[i][i] for i in range(len(square))]
  diag2 = [square[i][len(square)-(i+1)] for i in range(len(square))]
  if sum(diag1) != value:
    return False
  if sum(diag2) != value:
    return False

  return True

def score(square):
  numbers = []
  sums = []
  for row in square:
    sums.append(sum(row))
    for col in row:
      numbers.append(col)
  s_numbers = set(numbers)
  # print(f"numbers: {numbers}")
  # print(f"set: {s_numbers}")
  score_1 = len(s_numbers)/len(numbers)
  # print(f"Score_1: {score_1}")

  t_square = transpose(square)
  for row in t_square:
    sums.append(sum(row))
  diag1 = [square[i][i] for i in range(len(square))]
  diag2 = [square[i][len(square)-(i+1)] for i in range(len(square))]
  sums.append(sum(diag1))
  sums.append(sum(diag2))

  most_common = Counter(sums).most_common(1)[0][1] #We only want the number of similar rows/cols

  # print(most_common)
  score_2 = most_common/(2*len(square) + 2) # + 2 diag
  # print(f"Score_2: {score_2}")

  total = score_1+score_2
  # print(f"Score: {total}")
  return total




def visu_states(states):
  for s in states:
    print(s.score)
    if s.score != 0:
      print(str(s))


high_score = 0
gen_since_high_score = 0
best = None
if __name__ == "__main__":

  NB_GENERATION = 100
  NB_BETTER = .1
  MUTATION_RATE = .1
  NB_CHROMOSOMES = 100
  s = 3
  # square = [[4,9,2],[3,5,7],[8,1,6]]
  # square_2 = [[4,9,2],[3,9,7],[8,1,6]]
  # squares = [square,square_2]

  # for s in squares:
  #   print(visu(s))
  #   print(verify(s))
  #   score(s)


  population = Population(NB_CHROMOSOMES,s,NB_BETTER,MUTATION_RATE)
  population.generate_first()

  # print(str(population.chromosomes[0]))

  # sqr = squarify(population.chromosomes[0])
  # print(visu(sqr))
  # print(verify(sqr))

 
  found = False
  avg_score = 0
  k = 0
  while not found:
    states = []
    for ch in population.chromosomes:
      sq = squarify(ch)
      if verify(sq):
        ch.score = 2.0
        print(f"GEN {k} FOUND !")
        high_score = ch.score
        best = deepcopy(ch)
        found = True
        break
      else:
        ch.score = score(sq)
      states.append(ch)

    if found:
      break
    states = sorted(states,key=lambda x:x.score,reverse=True)
    avg_score += states[0].score

    print(f"GEN:{k}\tBest: {states[0].score} Worst: {states[-1].score}")
    gen_since_high_score += 1
    if states[0].score > high_score:
      # print(f"NEW BEST : {high_score} => {states[0].score}")
      high_score = states[0].score
      best = deepcopy(states[0])
      gen_since_high_score = 0

    # if k < NB_GENERATION - 1:
    population.select_next(states)
    k += 1

  print(f"Avg: {avg_score/k}")
  print(f"Best of All : {best.score}\nSquare\n{visu(squarify(best))}")
