## Course 1: Natural Language Processing
## Module 1: Intro to NLP in Python
## Coding Exercise 1

from nltk.tokenize import word_tokenize

def find_usernames(emails):
  return [[word_tokenize(email)[0]] for email in emails]

emails = ['skateboard@bobaround.com', 'investigators@dangerous.com', 'vehicles@floatingvehicles.com', 'pipes@cars.com', 'engine@shutdown.com', 'water@power.com']
print(find_usernames(emails))


## Course 1: Natural Language Processing
## Module 1: Intro to NLP in Python
## Coding Exercise 2

from nltk.tokenize import word_tokenize

def common_words(sentences):
  count_dict = {}
  for sentence in sentences:
    words = word_tokenize(sentence)
    for word in words:
      word = word.lower()
      count_dict[word] = count_dict.get(word, 0) + 1
  return sorted(count_dict.items(), key=lambda item: item[1], reverse=True)[:4]

many_sentences = ["How many blankets do you want?", "There are many dogs here.", "How come there aren't many cats here?", "There are many people in the world."]
print(common_words(many_sentences))



## Course 1: Natural Language Processing
## Module 1: Intro to NLP in Python
## Coding Exercise 3
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords

def find_pronouns(sentences):
  pronouns = []
  for sentence in sentences:
    words = word_tokenize(sentence)
    words = [words for words in word_tokenize(sentence) if words not in set(stopwords.words('english'))]   
    for word, pos in pos_tag(words):
      #print(word, pos)
      if pos == 'PRP':
        pronouns.append(word)
  return pronouns

sentences = ['They are good at playing football.', \
             'He has many backpacks.', \
             'She has lots of pens in her bag.', \
             'I forgot my ID.', \
             'The dog stared at himself in the reflection.', \
             'She told me it had to be done by end of day.']
print(find_pronouns(sentences))


from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

def find_names(text):
  tags = pos_tag(word_tokenize(text))
  labeled_chunks = ne_chunk(tags, binary=True)
  return set(
    " ".join(word[0] for word in chunked_word)
    for chunked_word in labeled_chunks
    if hasattr(chunked_word, "label") and chunked_word.label() == "NE")

text = "The various continuations of William of Tyre above mentioned represent the opinion of the native Franks (which is hostile to Richard I.); while in Nicetas, who wrote a history of the Eastern empire from 1118 to 1206, we have a Byzantine authority who, as Professor Bury remarks, 'differs from Anna and Cinnamus in his tone towards the crusaders, to whom he is surprisingly fair.'"
print(find_names(text))


import nltk

def remove_verbs(sents):
  sent = ' '.join(sents)
  sent = nltk.word_tokenize(sent)
  sent = nltk.pos_tag(sent)
  pattern = r"""ChinkAllVerbs: {<.*>+}
  }<VB.*>{""" #'NP: {<DT>?<JJ>*<NN>}'
  cp = nltk.RegexpParser(pattern)
  cs = cp.parse(sent)
  return cs

sentences = ["He washed the car yesterday.", "I bought her a book and a coffee.", "She thinks going outside is healthy.", "The dog runs away."]
print(remove_verbs(sentences))


from sklearn.feature_extraction.text import CountVectorizer

# Collect user input
documents = []
text = input("Enter document contents or type `exit` to end input: ")
while text.strip() != 'exit':
    documents.append(text.strip())
    text = input("Enter document contents or type `exit` to end input: ")

# WRITE YOUR CODE HERE
#vectorizer = CountVectorizer(analyzer='word', ngram_range=(2,2), stop_words='english', lowercase=True)
#X = vectorizer.fit_transform(documents)
#print(vectorizer.get_feature_names_out())
#print(X.toarray())

vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 2), stop_words='english')
X = vectorizer.fit_transform(documents)
print(vectorizer.get_feature_names())
print(X.toarray())


from sklearn.feature_extraction.text import TfidfVectorizer

# Collect user input
documents = []
text = input("Enter document contents or type `exit` to end input: ")
while text.strip() != 'exit':
    documents.append(text.strip())
    text = input("Enter document contents or type `exit` to end input: ")

# WRITE YOUR CODE HERE
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)
print(vectorizer.get_feature_names())
print(X.toarray())


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

# Collect user input
documents = []
documents.append(input("Enter first document contents: ").strip())
documents.append(input("Enter second document contents: ").strip())
print("The Jaccard similarity coefficient score between these documents is: ")

# WRITE YOUR CODE HERE
vectorizer = CountVectorizer(stop_words='english', binary=True)
X = vectorizer.fit_transform(documents)
print(jaccard_score(X.toarray()[0], X.toarray()[1]))


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances

# Collect user input
documents = []
text = input("Enter document contents or type `exit` to end input: ")
while text.strip() != 'exit':
    documents.append(text.strip())
    text = input("Enter document contents or type `exit` to end input: ")
print("The eucledian distances between these documents are: ")

# WRITE YOUR CODE HERE
vectorizer = CountVectorizer(stop_words='english', binary=True)
X = vectorizer.fit_transform(documents)
print( euclidean_distances(X) )

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Collect user input
documents = []
text = input("Enter document contents or type `exit` to end input: ")
while text.strip() != 'exit':
    documents.append(text.strip())
    text = input("Enter document contents or type `exit` to end input: ")
print("The cosine similarities between these documents are: ")

# WRITE YOUR CODE HERE
vectorizer = CountVectorizer(stop_words='english', binary=True)
X = vectorizer.fit_transform(documents)
print( cosine_similarity(X) )


from nltk.chat.util import Chat

# WRITE YOUR CODE HERE
# Generating response
def get_bot_response():
  pairs = [
  ('(.*)the weather(.*)', ['It\'s sweater weather!']),
  ('(.*)your day(.*)', ['It was great! Thanks for asking!']),
  ('(hi|hey|hello|hola), how are you(.*)', ['I\'m good! How about you?'])
  ]
  chat = Chat(pairs)
  chat.converse()

get_bot_response()


import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))

document = input("Enter the text to lemmatize: ")

# WRITE YOUR CODE HERE
import string
#remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
tokens = nltk.word_tokenize(document) #.translate(remove_punct_dict))
lemmatizer = WordNetLemmatizer()
print([lemmatizer.lemmatize(token) for token in tokens if token.lower() not in list(stop_words) + list(string.punctuation) if token.isalnum()])
#LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


import requests
import nltk

from googlesearch import search
from lxml import html
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

# helper function to generate text corpus from html elements
def generate_corpus(all_p_elements):
  corpus = ""
  for p_element in all_p_elements:
    corpus += '\n' + ''.join(p_element.findAll(text = True))
  return corpus

# Collect user input
query = input("Enter the query to search on Google: ")

# WRITE YOUR CODE HERE
google_search_results = list(search(query, stop=3, pause=1))
# use the requests api to fetch the top result webpage
webpage = requests.get(google_search_results[0])
webpage_tree = html.fromstring(webpage.content)
webpage_soup = BeautifulSoup(webpage.content, "lxml")
# extract all <p> elements from webpage soup object
all_p_list = webpage_soup.findAll('p')
# generate corpus from all <p> elements
google_search_corpus = generate_corpus(all_p_list)
# Tokenisation
sentence_tokens = nltk.sent_tokenize(google_search_corpus)# converts raw text to list of sentences
# Calculate TFIDF matrix
sentence_tokens.append(query)
tfidf_vectorizer = TfidfVectorizer(stop_words='english') #lowercase=False, 
tfidf = tfidf_vectorizer.fit_transform(sentence_tokens)
print(google_search_results[0])
print(tfidf_vectorizer.get_feature_names_out())
print(tfidf.toarray())


import requests
import nltk

from googlesearch import search
from lxml import html
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Collect user input
query = input("Enter the query to search on Google: ")

# WRITE YOUR CODE HERE
# helper function to generate text corpus from html elements
def generate_corpus(all_p_elements):
  corpus = ""
  for p_element in all_p_elements:
    corpus += '\n' + ''.join(p_element.findAll(text = True))
  return corpus

# WRITE YOUR CODE HERE
google_search_results = list(search(query, stop=3, pause=1))
# use the requests api to fetch the top result webpage
webpage = requests.get(google_search_results[0])
webpage_tree = html.fromstring(webpage.content)
webpage_soup = BeautifulSoup(webpage.content, "lxml")
# extract all <p> elements from webpage soup object
all_p_list = webpage_soup.findAll('p')
# generate corpus from all <p> elements
google_search_corpus = generate_corpus(all_p_list)
# Tokenisation
sentence_tokens = nltk.sent_tokenize(google_search_corpus)# converts raw text to list of sentences
# Calculate TFIDF matrix
sentence_tokens.append(query)
vectorizer = CountVectorizer(stop_words='english', binary=True) #lowercase=False, 
X = vectorizer.fit_transform(sentence_tokens)
print(google_search_results[0])
#print(vectorizer.get_feature_names_out())
#print(X.toarray())
print(cosine_similarity(X))

import os
import transformers

# WRITE YOUR CODE HERE
model = transformers.pipeline("conversational", model="microsoft/DialoGPT-small")
os.environ["TOKENIZERS_PARALLELISM"] = "true"
print(type(model))

