from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

set(stopwords.words('english'))

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    stop_words = stopwords.words('english')
    
    # Get input text and convert to lowercase
    text1 = request.form['text1'].strip().lower()
    
    # Check if input is empty
    if not text1:
        return render_template('form.html', error="Please provide input text.", final=None, text1=None, text2=None, text5=None, text4=None, text3=None)
    
    # Remove digits
    text_final = ''.join(c for c in text1 if not c.isdigit())
    
    # Remove stopwords    
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Perform sentiment analysis
    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound']) / 2, 2)

    return render_template('form.html', final=compound, text1=text_final, text2=dd['pos'], text5=dd['neg'], text4=compound, text3=dd['neu'])

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)