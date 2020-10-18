from collections import Counter
import re
from flask import Flask, jsonify, request, render_template
finalDict={}
#dummy text
comment_words='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.Why do we use it?It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).'    
def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]
def generateWord(comment_words):

#reading the text input
#comment_words=input("Type something to test this out: ")
    
    word_list=comment_words.split()
    trimed_word=[]
    for word in word_list:
        if len(word)>1:
            temp=re.sub('[^A-Za-z]+', '', word)
            if temp:
                trimed_word.append(temp)
    stopWords=set(read_words('stopwords.txt'))
    newWord=[]

    #couting to occurence of each word and removing the stop words
    for i in range(len(trimed_word)):
        word=trimed_word[i]
        if word.lower() not in stopWords:
            newWord.append(word)
    freqDict=dict(Counter(newWord))

    freDict={k: v for k, v in sorted(freqDict.items(), key=lambda item: item[1],reverse=True)}
    #print(freDict)
    finalDict = {k: freDict[k] for k in list(freDict.keys())[:90]}
    base=1
    i=0
    for k,v in finalDict.items():
        if i==0:
            base=v
            finalDict[k]=100
            i+=1
        else:
            finalDict[k]=finalDict[k]*100//base
    return finalDict

app = Flask(__name__)

new_word =''

@app.route('/hello', methods=['GET', 'POST'])

def hello():
   
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        json=request.get_json() # parse as JSON
        new_word=json['text']
        finalDict=generateWord(new_word)
        return jsonify(dict=finalDict) 

    # GET request
    else:
        finalDict=generateWord(comment_words)
        #print(finalDict)
        return jsonify(dict=finalDict)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    return render_template('frontEnd.html')

if __name__ == "__main__":
	app.run()

