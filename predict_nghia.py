from transformers import pipeline
import torch
import time

class Predictor():
    def __init__(self):
        self.model_checkpoint1 = "HieuLV3/QA_UIT_xlm_roberta_large"
        # self.model_checkpoint2 = "nguyenvulebinh/vi-mrc-large"
        self.nlp1 = pipeline('question-answering', model=self.model_checkpoint1,
                   tokenizer=self.model_checkpoint1)
        # self.nlp2 = pipeline('question-answering', model=self.model_checkpoint2,
                  #  tokenizer=self.model_checkpoint2)
    def getPredictions1(self, examples, domain):
      if domain==1:
        time_start = time.time()
        predictions = self.nlp1(examples)
        time_end = time.time() - time_start
        predictions['total_time'] = time_end
        return predictions
      elif domain==2:
        tim = {} 
        time_start = time.time()
        predictions = self.nlp1(examples)
        time_end = time.time() - time_start
        predictions['total_time'] = time_end
        return predictions
      elif domain==3:
        tim = {} 
        time_start = time.time()
        predictions = self.nlp1(examples)
        time_end = time.time() - time_start
        tim['total_time'] = time_end
        predictions.append(tim)
        return predictions



    # def getPredictions2(self, examples, domain):
      # if domain==1:
      #   time_start = time.time()
      #   predictions = self.nlp2(examples)
      #   time_end = time.time() - time_start
      #   predictions['total_time'] = time_end
      #   return predictions
      # elif domain==2:
      #   tim = {} 
      #   time_start = time.time()
      #   predictions = self.nlp2(examples)
      #   time_end = time.time() - time_start
      #   tim['total_time'] = time_end
      #   predictions.append(tim)
      #   return predictions
      # elif domain==3:
      #   tim = {} 
      #   time_start = time.time()
      #   predictions = self.nlp2(examples)
      #   time_end = time.time() - time_start
      #   tim['total_time'] = time_end
      #   predictions.append(tim)
      #   return predictions