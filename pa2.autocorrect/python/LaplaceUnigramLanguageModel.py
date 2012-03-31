import math
from collections import *

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.count = Counter()
    self.vocabulary_size = 0
    self.num_words = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        self.count[word] += 1
    self.vocabulary_size = len(self.count.items())
    self.num_words = sum(self.count.values())

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    # Laplace Add_1 smoothing
    for token in sentence:
      score += math.log(self.count[token] + 1.0)
      score -= math.log( self.num_words + self.vocabulary_size )
    return score
