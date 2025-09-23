```python
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pickle
import json
import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import pandas as pd
import numpy as np

# Initialize the database
db = SQLAlchemy()

# Define the database models
Base = declarative_base()

class User(db.Model):
    """User model"""
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

class Article(db.Model):
    """Article model"""
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(256), nullable=False)

class SummarizedArticle(db.Model):
    """Summarized article model"""
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, db.ForeignKey('article.id'), nullable=False)
    summary = Column(Text, nullable=False)

class ExportOption(db.Model):
    """Export option model"""
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)

class ExportedArticle(db.Model):
    """Exported article model"""
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, db.ForeignKey('article.id'), nullable=False)
    export_option_id = Column(Integer, db.ForeignKey('export_option.id'), nullable=False)
    exported_content = Column(Text, nullable=False)

# Define the database tables
Base.metadata.create_all(db.engine)

# Define the AI-powered content summarizer functions
def extract_text_from_url(url):
    """Extract text from a URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from URL: {e}")
        return None

def summarize_text(text):
    """Summarize text using AI"""
    try:
        # Tokenize the text
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.lower() not in stop_words]
        
        # Lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # Tag the tokens with their parts of speech
        tagged_tokens = pos_tag(tokens)
        
        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        
        # Fit the vectorizer to the tokens and transform them into vectors
        vectors = vectorizer.fit_transform(tagged_tokens)
        
        # Train a Naive Bayes classifier on the vectors
        classifier = MultinomialNB()
        classifier.fit(vectors, [1]*len(vectors))
        
        # Use the classifier to predict the summary
        summary = classifier.predict(vectors)
        
        return ' '.join(summary)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

def export_article(article_id, export_option_id):
    """Export an article based on the selected export option"""
    try:
        article = Article.query.get(article_id)
        export_option = ExportOption.query.get(export_option_id)
        
        if article and export_option:
            exported_content = export_article_content(article.content, export_option.name)
            exported_article = ExportedArticle(article_id=article_id, export_option_id=export_option_id, exported_content=exported_content)
            db.session.add(exported_article)
            db.session.commit()
            return exported_article
        else:
            return None
    except Exception as e:
        print(f"Error exporting article: {e}")
        return None

def export_article_content(content, export_option):
    """Export article content based on the selected export option"""
    try:
        if export_option == 'pdf':
            # Export as PDF
            return 'PDF content'
        elif export_option == 'docx':
            # Export as DOCX
            return 'DOCX content'
        elif export_option == 'txt':
            # Export as plain text
            return 'TXT content'
        else:
            return None
    except Exception as e:
        print(f"Error exporting article content: {e}")
        return None
```