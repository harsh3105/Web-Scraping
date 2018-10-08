from sklearn.feature_extraction.text import CountVectorizer
import codecs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from bs4 import BeautifulSoup
import urllib2
import requests
import re,math
import os


#This Function will calculate the cosine similarity between the query and the doc's.

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

#This Function will calculate the vectors of the text and return it.

def text_to_vector(text):
     words = WORD.findall(text)
     #print(Counter(words)
     return Counter(words)

#This function will crawl the LINKS from the given List and will copy text data into a text file.

def func(i,name):
        html = requests.get(i).content
        unicode_str = html.decode("ISO-8859-1")
        encoded_str = unicode_str.encode("ascii",'ignore')
        news_soup = BeautifulSoup(encoded_str, "html.parser")
        a_text = news_soup.find_all('p')
        y=[re.sub(r'<.+?>',r'',str(a)) for a in a_text]

        file1 = open('test.txt', 'w')
        for item in y:
            file1.write("%s\n" % item)
        os.rename("test.txt",name)

        
WORD = re.compile(r'\w+')

#TASK: 1
#The URL if of the wikipedia which will contain the details of VIT Vellore.  
url = "https://en.wikipedia.org/wiki/Vellore_Institute_of_Technology"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'lxml')
links = []

#All the links which are found on the wikipedia page are stored in list 

for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    links.append(link.get('href'))

print(links)

#TASK: 3
#All the link which were store in the previous section are crawled one by one and the text data is stored. 

name=[]
for i in range(50):
    s = "file"+ str(i) +".txt" 
    name.append(s)
x=0
for i in links:
    func(i,name[x])
    x=x+1

#The Stopword are removed using the NLTK library.
stop_words = set(stopwords.words('english'))
filtered_sentence = []

main =[]
i=0
for item in name:
    file1 = codecs.open(item, encoding='utf-8')
    word_tokens = word_tokenize(file1.read())
    for w in word_tokens:
        if w not in stop_words:
            s = s + " "+w
    main.append(s)

#TASK: 3
#Vectorization of all the document is done and printed as a Matrix.

vectorizer = CountVectorizer()
p = vectorizer.fit_transform(main)
print(p.toarray())

#TASK: 4
#The query will be takes as an user input and the cosine similarity will calculated with each of the document.
all_cos=[]
text1 = raw_input("Please Enter a Query")
vector1 = text_to_vector(text1)
for i in range(50):
    text2 = codecs.open(name[i], encoding='utf-8').read()
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    all_cos.append(cosine)
    print 'Cosine:', i, cosine

#TASK: 5
#The Rank and the Link of top 10 doc's will be Displayed here.
for i in range(10):
    a= all_cos.index(max(all_cos))
    print i+1
    print(links[a%30]+"\n")
    all_cos.pop(a)