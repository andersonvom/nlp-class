import math
from collections import Counter
from collections import defaultdict

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram_count = Counter()
    self.bigram_count = defaultdict(Counter)
    self.vocabulary_size = 0
    self.num_words = 0
    self.backoff_multiplier = 0.4
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      prev_word = None
      for datum in sentence.data:
        word = datum.word
        self.unigram_count[word] += 1
        if prev_word != None:
          self.bigram_count[prev_word][word] += 1
        prev_word = word
      
    self.vocabulary_size = len(self.unigram_count)
    self.num_words = sum(self.unigram_count.values())

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_word = None
    for token in sentence:
      two_words_count = self.bigram_count[prev_word][token]
      prev_word_count = self.unigram_count[prev_word]
      if (two_words_count > 0):
        score += math.log(two_words_count)
        score -= math.log(prev_word_count)
      else:
        score += math.log(self.backoff_multiplier)
        score += math.log(self.unigram_count[token] + 1.0)
        score -= math.log(self.num_words + self.vocabulary_size)
      prev_word = token
    return score
