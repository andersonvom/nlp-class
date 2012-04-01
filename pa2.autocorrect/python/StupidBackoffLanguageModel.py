import math
from collections import Counter
from collections import defaultdict

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.n_gram = 2
    self.backoff_modifier = 0.4
    self.count = []
    for i in range(self.n_gram):
      self.count.append(Counter())
    self.total_words = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      prev_words = []
      for datum in sentence.data:
        word = datum.word
        if len(prev_words) >= self.n_gram:
          prev_words = prev_words[1:]
        prev_words.append(word)
        prev_words_size = len(prev_words)
        for i in range(prev_words_size):
          prev_range_idx = prev_words_size-1-i
          word_tuple = tuple(prev_words[prev_range_idx:])
          self.count[i][word_tuple] += 1
      
    self.vocabulary_size = len(self.count[0])
    self.total_words = sum(self.count[0].values())

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_words = []
    for token in sentence:
      prev_words.append(token)
      if len(prev_words) > self.n_gram:
        prev_words = prev_words[1:]
      else:
        continue
      
      curr_n_gram = self.n_gram - 1
      while (curr_n_gram > 0):
        curr_idx = self.n_gram - 1 - curr_n_gram
        all_words = tuple( prev_words[curr_idx:] )
        if self.count[curr_n_gram][all_words] == 0:
          curr_n_gram -= 1
          continue
        #print all_words
        all_words_count = self.count[curr_n_gram][all_words]
        #print all_words_count
        #print all_words[0:-1]
        prefix_words_count = self.count[curr_n_gram-1][all_words[0:-1]]
        #print prefix_words_count
        #print "====="
        score += math.log(all_words_count)
        score -= math.log(prefix_words_count)
        break

      if curr_n_gram == 0:
        score += math.log( self.count[0][(token)] + 1.0 )
        score -= math.log( self.total_words + self.vocabulary_size )
        
    return score

