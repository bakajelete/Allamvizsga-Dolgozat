import numpy as np
import random

class RBF(object):

    def __init__(self, shape, sigma=0.5, centers=None, weights=None):
        self.shape = shape
        self.sigma = sigma
        self.centers = centers
        self.weights = weights
        
        self.kernel_type = ''
        
    def gaussian_kernel(self, center, data_point):
        return np.exp(-1 * self.sigma * (np.linalg.norm(center - data_point) ** 2))        
    
    def cosine_kernel(self, center, data_point):
        return np.cos(self.sigma * (np.linalg.norm(center - data_point) ** 2))
    
    def sigmoid_kernel(self, center, data_point):
        return np.tanh(self.sigma * np.dot(center, data_point) + 1)
        
    
    def interpolation_matrix_Gauss(self, X):
        matrix = np.zeros(len(X) * self.shape)
        counter = 0
        for inp in X:
            for center in self.centers:
                kernel = self.gaussian_kernel(center, inp)
                matrix[counter] = kernel
                counter += 1
                
        return matrix.reshape(len(X), self.shape)
    
    def interpolation_matrix_Cosine(self, X):
        matrix = np.zeros(len(X) * self.shape)
        counter = 0
        for inp in X:
            for center in self.centers:
                kernel = self.cosine_kernel(center, inp)
                matrix[counter] = kernel
                counter += 1
                
        return matrix.reshape(len(X), self.shape)
    
    def interpolation_matrix_Sigmoid(self, X):
        matrix = np.zeros(len(X) * self.shape)
        counter = 0
        for inp in X:
            for center in self.centers:
                kernel = self.sigmoid_kernel(center, inp)
                matrix[counter] = kernel
                counter += 1
                
        return matrix.reshape(len(X), self.shape)

    def select_centers(self, X):
        centers = []
        random_indices = random.sample(range(0, len(X)), self.shape)
        for rnd in random_indices:
            centers.append(X[rnd])
            
        return np.array(centers)

    def fit(self, X, Y, kernel_type):
        self.centers = self.select_centers(X)
        self.kernel_type = kernel_type
        
        if kernel_type == "Cosine":
            im = self.interpolation_matrix_Cosine(X)
        elif kernel_type == "Sigmoid":
            im = self.interpolation_matrix_Sigmoid(X)
        else:
            im = self.interpolation_matrix_Gauss(X)
            
        self.weights = np.dot(np.linalg.pinv(im), Y)    
   
    def predict(self, X):
        
        if self.kernel_type == "Cosine":
            im = self.interpolation_matrix_Cosine(X)
        elif self.kernel_type == "Sigmoid":
            im = self.interpolation_matrix_Sigmoid(X)
        else:
            im = self.interpolation_matrix_Gauss(X)
            
        predictions = np.dot(im, self.weights)
        return predictions
