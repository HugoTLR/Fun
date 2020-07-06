import string
import sympy

def generate_primes():
  prime_list = []
  i = 1
  while len(prime_list) < 26:
    prime_list.append(sympy.nextprime(i))
    i = prime_list[-1]
  return prime_list

def score(w):
  score = BIND[w[0]]
  for c in w[1:]:
    score *= BIND[c]
  return score

def is_anagram(w1,w2):
  w1 = "".join([w for w in w1.lower() if w in BIND.keys()])
  w2 = "".join([w for w in w2.lower() if w in BIND.keys()])
  if len(w1) != len(w2):
    return False
  s1 = score(w1)
  s2 = score(w2)
  return s1 == s2

if __name__ == "__main__":
  BIND = {}
  prime_list = generate_primes()

  for c,p in zip(string.ascii_lowercase,prime_list):
    BIND[c] = p

  w1 = "Trump et bolsonaro"
  w2 = "T'es bon pour la mortt"
  if is_anagram(w1,w2):
    print(f"{w1}\n\tis anagram of\n{w2}")
  else:
    print(f"{w1}\n\tis not anagram of\n{w2}")