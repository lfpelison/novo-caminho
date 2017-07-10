import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.externals import joblib

class NewsClassifier():

    def __init__(self):
        self.risk_classifier = joblib.load('datascience/risk_classifier.cls')
        self.category_classifier = joblib.load('datascience/category_classifier.cls')
        self.risk_voc = joblib.load("datascience/risk_voc.cls")
        self.cat_voc = joblib.load("datascience/cat_voc.cls")

    def risk_transform(self, summary):
        self.risk_summary_dtm = self.risk_voc.transform([summary])

    def category_transform(self, summary):
        self.cat_summary_dtm = self.cat_voc.transform([summary])

    def news_predictions(self, summary):
        self.risk_transform(summary)
        self.category_transform(summary)
        self.risk = self.risk_classifier.predict(self.risk_summary_dtm)
        self.category = self.category_classifier.predict(self.cat_summary_dtm)
        self.category = self.category_map(self.category)
        return {'risk':self.risk, 'category':self.category}

    def category_map(self, category_num):
        cat_template = {1:'Manifestacao', 2:'Crime', 3:'Economia', 4:'Politica', 5:'Dano-Ambiental', 6:'Positiva'}
        category = cat_template[int(category_num)]
        return category
