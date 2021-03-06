from pyexpat import model
import streamlit as st
import pickle 
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps=PorterStemmer()


def transform_text(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text=y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text=y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)


tfidf=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))


st.title("Email/SMS Classifier")
sms_input=st.text_area("Enter your message")


if st.button('Predict'):
    #1.preprocess
    transformed_sms = transform_text(sms_input)

    #2.vectorize
    vector_input = tfidf.transform([transformed_sms])

    #3.model predict
    res=model.predict(vector_input)[0]

    #4.Display
    if res==1:
        st.header("Spam")
    else:
        st.header("Not Spam")


