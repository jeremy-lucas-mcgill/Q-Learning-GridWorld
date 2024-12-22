import numpy as np
class Network:
    def __init__(self, input_size, hidden_size, output_size,learning_rate = 0.01, activation_function='relu', momentum=0.9):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.v = np.random.uniform(-1, 1, size=(self.input_size, self.hidden_size))
        self.b1 = np.random.uniform(-1, 1, size=(self.hidden_size)).reshape(1, -1)
        self.w = np.random.uniform(-1,1, size=(self.hidden_size, self.output_size))
        self.b2 = np.random.uniform(-1, 1, size=(output_size)).reshape(1,-1)
        self.mv = np.zeros_like(self.v)
        self.mb1 = np.zeros_like(self.b1)
        self.mw = np.zeros_like(self.w)
        self.mb2 = np.zeros_like(self.b2)
    def train(self, x, y, epochs=10, batchsize=32):
        x = x.reshape(-1,self.input_size)
        y = y.reshape(-1, self.output_size)
        #foreach epoch
        for _ in range(epochs):
            #split data into batches
            indices = np.random.permutation(len(x))
            num_batches = int(np.ceil(len(x) / batchsize))
            for i in range(num_batches):
                start = i * batchsize
                end = start + batchsize
                x_batch = x[indices[start:end]]
                y_batch = y[indices[start:end]]
                self.trainBatch(x_batch,y_batch)
            print(f"Training Loss: {self.evaluate(x,y)}")
        pass
    def forwardPass(self, x):
        x = x.reshape(-1,self.input_size)
        #forward pass
        z = np.dot(x,self.v) + self.b1
        h = self.activation_function(z)
        y_pred = np.dot(h,self.w) + self.b2
        return y_pred, h, z
    def predict(self, x):
        x = x.reshape(-1,self.input_size)
        #forward pass
        z = np.dot(x,self.v) + self.b1
        h = self.activation_function(z)
        y_pred = np.dot(h,self.w) + self.b2
        return y_pred
    def evaluate(self, x, y):
        y_pred = self.predict(x)
        mse = np.mean((y-y_pred) ** 2)
        return mse
    def trainBatch(self,x,y):
        x = x.reshape(-1,self.input_size)
        y = y.reshape(-1,self.output_size)
        #forward pass
        y_pred, h, z = self.forwardPass(x)
        #backprop
        dy = (y_pred - y)
        #dw
        dw = np.dot(h.T,dy)
        #db2
        db2 = np.sum(dy, axis=0, keepdims=True)
        #dv
        dv = np.dot(x.T,np.dot(dy,self.w.T) * self.derivative_activation_function(z))
        #db1
        db1 = np.sum(np.dot(dy,self.w.T) * self.derivative_activation_function(z), axis=0, keepdims=True)
        #update momentum
        self.mw = self.momentum * self.mw + self.learning_rate * dw
        self.mb2 = self.momentum * self.mb2 + self.learning_rate * db2
        self.mv = self.momentum * self.mv + self.learning_rate * dv
        self.mb1 = self.momentum * self.mb1 + self.learning_rate * db1
        #update weights
        self.w -= self.mw
        self.b2 -= self.mb2
        self.v -= self.mv
        self.b1 -= self.mb1
    def activation_function(self,data):
            return np.maximum(0,data)
    def derivative_activation_function(self, data):
            return np.where(data > 0, 1, 0)