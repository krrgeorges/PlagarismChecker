import psycopg2
from bs4 import BeautifulSoup as bs
from GooglePowerQuerier import GooglePowerQuerier
import json
from nltk.tokenize import sent_tokenize
import re
from AnswerParser import AnswerParser

class PlagiarismChecker:
	"""Generalized Module for thwarting attempts of plagiarism of answer by user.Checked locally insite and globally through GooglePowerQuerier"""
	"""
	Involved Attribute : text
	"""
	def __init__(self,html,depth=0):
		self.html = html
		self.text = AnswerParser(self.html).getPureAnswer();
		self.depth = depth

	def check(self):
		"""returns dict object containing results"""
		
		"""external"""
		"""document level:querying whole document as power query"""
		d_l_text = self.text
		results = GooglePowerQuerier(d_l_text).query_exact_match(multiple=True,limit=self.depth)
		
		comparables = []
		for result in results:
			comparables.append(result)

		full_comparison_match = len(results);

		"""sentential level:querying each sentence as power query"""
		delimiter = ".!?"
		tokens = []
		r_parts = sent_tokenize(d_l_text.replace("\n","."))
		print(d_l_text.replace("\n","."))
		for i in range(0,len(r_parts)):
			if len(r_parts[i].replace(" ","")) != 0:
				if len(r_parts[i].split(" ")) > 3:
					tokens.append(r_parts[i])


		batch = []
		mtoken_matches = []

		for token in tokens:
			batch.append(token)
			if tokens.index(token) == len(tokens)-1 or tokens.index(token)%2 == 0:
				results = GooglePowerQuerier(None).query_exact_matches(batch,multiple=True,limit=self.depth)
				token_matches = [];
				for i in range(0,len(batch)):
					token_matches.append(0)

				for result in results:
					comparables.append(result)
					for jtoken in batch:
						if jtoken in result["subscript"]:
							token_matches[batch.index(jtoken)] += 1
				for token_match in token_matches:
					mtoken_matches.append(token_match)
				batch = []




		matched_tokens = 0
		for token_match in mtoken_matches:
			if token_match >= 1:
				matched_tokens += 1
		if len(tokens) > 0:
			percent_plagiarized_sentences = (matched_tokens/len(tokens))*100
		else:
			percent_plagiarized_sentences = 0
		data = {}
		data["comparables"] = comparables
		data["full_comparison_match"] = full_comparison_match
		data["tokens"] = tokens
		data["token_matches"] = mtoken_matches
		data["percent_plagiarized_sentences"] = percent_plagiarized_sentences;

		return data

# print(PlagiarismChecker("Consistently delivering quality client services. Staying abreast of current business and industry trends relevant to the client's business").check())