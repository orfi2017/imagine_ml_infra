from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np

from melampus.preprocessor import Preprocessor


class MelampusClassifier(object):
    def __init__(self, filename: str, outcomes=[], target_col=None, scaling=False, dim_red=(False, 0), normalize=False):
        '''

        :param filename:
        :param outcomes:
        :param target_col:
        :param scaling:
        :param dim_red:
        :param normalize: Activator and norm.
                            The norm to use to normalize each non zero sample(values: 'l1' or 'l2'
        '''
        self.filename = filename
        self.target_col = target_col
        self.scaling = scaling
        self.dim_red = dim_red
        self.normalize = normalize
        self.data, self.outcomes = [], []
        self.outcomes = outcomes
        self.classifier = object
        self.coefficients = np.array
        self.intercepts = np.array
        self.preprocess_data()

    def preprocess_data(self):
        pre = Preprocessor(filename=self.filename, target_col=self.target_col)
        if self.scaling:
            pre.standarize_data()

        if self.dim_red[0]:
            num_components = self.dim_red[1]
            pre.dimensionality_reduction(num_components=num_components)

        if self.normalize:
            pre.normalize_data()

        self.data = pre.data
        if self.target_col is not None:
            self.outcomes = pre.outcomes

    def train(self):
        print('model training ..')
        self.classifier = LogisticRegression()
        try:
            self.classifier.fit(self.data, self.outcomes)
            print('Melampus model training finished successfully')
            self.coefficients = self.classifier.coef_
            self.intercepts = self.classifier.intercept_
        except Exception as e:
            print('Error: {}'.format(str(e)))
            pass

    def assess_classifier(self):
        scores = cross_val_score(self.classifier, X_scaled, y, cv=10)
        return scores.mean()