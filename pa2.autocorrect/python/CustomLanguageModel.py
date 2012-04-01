import math
from collections import Counter
from collections import defaultdict

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram_count = Counter()
    self.bigram_count = Counter()
    self.trigram_count = Counter()
    self.vocabulary_size = 0
    self.num_words = 0
    self.backoff_multiplier = 0.4
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      prev_word1 = None
      prev_word2 = None
      for datum in sentence.data:
        word = datum.word
        self.unigram_count[tuple([word])] += 1
        if prev_word1 != None:
          self.bigram_count[tuple([prev_word1,word])] += 1
        if prev_word2 != None:
          self.trigram_count[tuple([prev_word2,prev_word1,word])] += 1
        prev_word2 = prev_word1
        prev_word1 = word
      
    self.vocabulary_size = len(self.unigram_count)
    self.num_words = sum(self.unigram_count.values())

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_word1 = None
    prev_word2 = None
    for word in sentence:
      three_words_count = self.trigram_count[tuple([prev_word2, prev_word1, word])]
      two_words_count = self.bigram_count[tuple([prev_word2, prev_word1])]
      # Use the trigram if it exists
      if (three_words_count > 0):
        score += math.log(three_words_count)
        score -= math.log(two_words_count)
      else:
        two_words_count = self.bigram_count[tuple([prev_word1, word])]
        one_word_count = self.unigram_count[tuple([prev_word1])]
        # Use the bigram if it exists
        if (two_words_count > 0):
          score += math.log(self.backoff_multiplier)
          score += math.log(two_words_count)
          score -= math.log(one_word_count)
        # Use the unigram in case all else fails
        else:
          score += 2 * math.log(self.backoff_multiplier)
          score += math.log(self.unigram_count[tuple([word])] + 1.0)
          score -= math.log(self.num_words + self.vocabulary_size)
      prev_word2 = prev_word1
      prev_word1 = word
    return score
