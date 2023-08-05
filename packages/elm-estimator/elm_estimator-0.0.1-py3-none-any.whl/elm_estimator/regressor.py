# coding:utf-8
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from .function import sigmoid, gaussian


class ELMRegressor(BaseEstimator, RegressorMixin):
    hidden_types = ['sigmoid', 'gaussian']

    def __init__(self, n_hidden=2000, hidden_type='sigmoid'):
        self.n_hidden = n_hidden
        self.a = None
        self.b = None
        self.beta = None
        self.hidden_type = hidden_type
        self.single_output = False

    def _forward(self, X):
        if self.hidden_type == 'sigmoid':
            return sigmoid(X, self.a, self.b)
        if self.hidden_type == 'gaussian':
            return gaussian(X, self.a, self.b)

    def fit(self, X, y):
        if y.ndim == 1:
            self.single_output = True
        n, d = X.shape
        self.a = np.random.randn(self.n_hidden, d)
        self.b = np.random.randn(self.n_hidden)
        h = self._forward(X)
        self.beta = np.dot(np.linalg.pinv(h), y)
        return self

    def predict(self, X):
        n, d = X.shape
        h = self._forward(X)
        res = np.dot(h, self.beta)
        if self.single_output:
            return res.reshape(n)
        return res
