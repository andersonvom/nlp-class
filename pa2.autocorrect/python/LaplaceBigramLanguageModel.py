import math
from collections import Counter
from collections import defaultdict

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.count = defaultdict(Counter)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      prev_word = None
      for datum in sentence.data:
        word = datum.word
        self.count[prev_word][word] += 1
        prev_word = word
      self.count[prev_word][None] += 1 # make sure even the last word gets counted
    self.vocabulary_size = len(self.count) - 1 # 'None' is not part of the vocabulary

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_word = None
    for token in sentence:
      if prev_word != None:
        two_words_count = self.count[prev_word][token] + 1.0
        prev_word_count = sum(self.count[prev_word].values()) + self.vocabulary_size
        score += math.log(two_words_count)
        score -= math.log(prev_word_count)
      prev_word = token
    return score
