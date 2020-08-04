from random import randint,random,choice
from sys import maxsize
from math import sqrt

class Population:
  def __init__(self,n,sq_size,better_pct,mutation_rate):
    self.n = n
    self.sq_size = sq_size
    self.n_cells = self.sq_size**2
    self.better_pct = better_pct
    self.mutation_rate = mutation_rate

    self.chromosomes = []
  def __str__(self):
    res = f"P({self.n=}-{self.sq_size=})[\n\t"
    for c in self.chromosomes:
      res = res + f"{c.__str__()},\n\t"
    res = res [:-1] + "]"
    return res

  def generate_first(self):
    for k in range(self.n):
      self.chromosomes.append(Chromosome(self.sq_size))
      genes = []
      for j in range(self.sq_size):
        for i in range(self.sq_size):
          val = randint(1, self.n_cells)
          genes.append(Gene(j,i,val))
      self.chromosomes[-1].genes = genes

  def select_next(self,states):
    sum_of_eval = 0
    for state in states:
      sum_of_eval += state.score
    if sum_of_eval != 0:
      for state in states:
        state.n_score = state.score/sum_of_eval

    states = sorted(states,key=lambda x:x.score,reverse=True)
    next_gen = [states[i] for i in range(int(self.n*self.better_pct))] 
    states = sorted(states,key=lambda x:x.score,reverse=False)

    cum_sum = [states[0].score]
    for p in range(1,len(states),1):
      cum_sum.append(cum_sum[-1]+states[p].score)
    cum_sum = cum_sum[::-1] #Reverse (avoid a sorted call as its just sorted in the wrong sense)
    cum_sum.append(0.0) #To end wheel properly

    while len(next_gen) < self.n:
      rnd = random()
      p1 = None
      for i in range(1,len(cum_sum),1):
        if cum_sum[i-1] >= rnd and rnd > cum_sum[i]:
          p1 = states[i-1]
          break
      rnd = random()
      p2 = None
      for i in range(1,len(cum_sum),1):
        if cum_sum[i-1] >= rnd and rnd > cum_sum[i]:
          p2 = states[i-1]
          break

      # print(str(p1),str(p2))
      next_gen.extend(self.create_childs(p1,p2))
      self.chromosomes = next_gen
      for ch in self.chromosomes:
        if random() <= self.mutation_rate:
          ch.mutate()
          # ch.swap()


  def create_childs(self,p1,p2):
    rnd = random()
    childs = [Chromosome(self.sq_size),Chromosome(self.sq_size)]
    childs[0].genes = [self.crossover(p1.genes[i],p2.genes[i],rnd) for i in range(self.sq_size**2)]
    childs[1].genes = [self.crossover(p2.genes[i],p1.genes[i],rnd) for i in range(self.sq_size**2)]
    return childs
  
  def crossover(self,g1,g2,rnd):
    assert g1.j == g2.j, f"Genes have different row idx => {g1.j=} : {g2.j=}"
    assert g1.i == g2.i, f"Genes have different row idx => {g1.i=} : {g2.i=}"
    n_val = int( (rnd*g1.val)+(1-rnd)*g2.val)
    return Gene(g1.j,g1.i,n_val)

class Chromosome:
  def __init__(self,size):
    self.genes = []
    self.size = size
    self.score = 0

  def __str__(self):
    res = f"C[\n\t\t"
    for g in self.genes:
      res = res + f"{g.__str__()}\n\t\t"
    res = res[:-1]+"]"
    return res

  def mutate(self):
    idx = self.genes.index(choice(self.genes))
    self.genes[idx].val = randint(1, len(self.genes))

  def swap(self):
    idx = self.genes.index(choice(self.genes))
    idx2 = self.genes.index(choice(self.genes))
    while idx == idx2:
      idx2 = self.genes.index(choice(self.genes))
    tmp = self.genes[idx].val
    self.genes[idx].val = self.genes[idx2].val
    self.genes[idx2].val = tmp

class Gene:
  def __init__(self,j,i,val):
    self.j = j
    self.i = i
    self.val = val

  def __str__(self):
    return f"G({self.j},{self.i}) {self.val}"
