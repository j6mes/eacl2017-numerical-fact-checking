import os
import pickle
from collections import defaultdict
import numpy as np
from sklearn.linear_model import LogisticRegression

from classifier.Classifier import Classifier
from classifier.features.bow import BOW
from classifier.features.linearise import flatten_without_labels
from classifier.features.pseudo_multiclass import IDPerColumnMultiClass
from distant_supervision.clean_html import has_text
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search


class LogisticRegressionClassifier(Classifier):
    def train(self, Xs, ys):
        print("Training classifier")
        self.lr = LogisticRegression(penalty='l1', C=0.9)
        self.lr.fit(Xs, ys)
        print("Trained")

    def predict(self, q_features):
        ys = self.lr.predict(q_features)
        return ys
