# create RNN architecture
"""
learning_rate = 0.0001
seq_len = 50
max_epochs = 25
hidden_dim = 100
output_dim = 1
bptt_truncate = 5  # backprop through time --> lasts 5 iterations
min_clip_val = -10
max_clip_val = 10


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# takes x values and the weights matrices
# returns layer dictionary, final weights (mulu, mulw, mulv)
def calc_layers(x, U, V, W, prev_activation):
    layers = []
    mulu = None
    mulv = None
    mulw = None

    for timestep in range(seq_len):
        new_input = np.zeros(x.shape)
        new_input[timestep] = x[timestep]
        mulu = np.dot(U, new_input)
        mulw = np.dot(W, prev_activation)
        _sum = mulw + mulu
        activation = sigmoid(_sum)
        mulv = np.dot(V, activation)
        layers.append({'activation': activation, 'prev_activation': prev_activation})
        prev_activation = activation

    return layers, mulu, mulw, mulv


def backprop(x, U, V, W, dmulv, mulu, mulw, layers):
    dU = np.zeros(U.shape)
    dV = np.zeros(V.shape)
    dW = np.zeros(W.shape)

    dU_t = np.zeros(U.shape)
    dV_t = np.zeros(V.shape)
    dW_t = np.zeros(W.shape)

    dU_i = np.zeros(U.shape)
    dW_i = np.zeros(W.shape)

    _sum = mulu + mulw
    dsv = np.dot(np.transpose(V), dmulv)

    def get_previous_activation_differential(_sum, ds, W):
        d_sum = _sum * (1 - _sum) * ds
        dmulw = d_sum * np.ones_like(ds)
        return np.dot(np.transpose(W), dmulw)

    for timestep in range(seq_len):
        dV_t = np.dot(dmulv, np.transpose(layers[timestep]['activation']))
        ds = dsv
        dprev_activation = get_previous_activation_differential(_sum, ds, W)

        for _ in range(timestep - 1, max(-1, timestep - bptt_truncate - 1), -1):
            ds = dsv + dprev_activation
            dprev_activation = get_previous_activation_differential(_sum, ds, W)
            dW_i = np.dot(W, layers[timestep]['prev_activation'])

            new_input = np.zeros(x.shape)
            new_input[timestep] = x[timestep]
            dU_i = np.dot(U, new_input)

            dU_t += dU_i
            dW_t += dW_i

        dU += dU_t
        dV += dV_t
        dW += dW_t

        # take care of possible exploding gradients
        if dU.max() > max_clip_val:
            dU[dU > max_clip_val] = max_clip_val
        if dV.max() > max_clip_val:
            dV[dV > max_clip_val] = max_clip_val
        if dW.max() > max_clip_val:
            dW[dW > max_clip_val] = max_clip_val

        if dU.min() < min_clip_val:
            dU[dU < min_clip_val] = min_clip_val
        if dV.min() < min_clip_val:
            dV[dV < min_clip_val] = min_clip_val
        if dW.min() < min_clip_val:
            dW[dW < min_clip_val] = min_clip_val

    return dU, dV, dW


# training
def train(U, V, W, X, Y):
    for epoch in range(max_epochs):
        print(epoch, " time(s) training") """
'''
        # calculate initial loss, ie what the output is given a random set of weights
        loss, prev_activation = calculate_loss(X, Y, U, V, W)

        # check validation loss
        val_loss, _ = calculate_loss(X_validation, Y_validation, U, V, W)

        print(f'Epoch: {epoch + 1}, Loss: {loss}, Validation Loss: {val_loss}')
        '''
# train model/forward pass
'''
        for i in range(Y.shape[0]):
            x, y = X[i], Y[i]
            layers = []
            prev_activation = np.zeros((hidden_dim, 1))

            layers, mulu, mulw, mulv = calc_layers(x, U, V, W, prev_activation)

            # difference of the prediction
            dmulv = mulv - y
            dU, dV, dW = backprop(x, U, V, W, dmulv, mulu, mulw, layers)

            # update weights
            U -= learning_rate * dU
            V -= learning_rate * dV
            W -= learning_rate * dW
    return U, V, W


def print_redirect(x, file):
    with open('file', 'a') as f:
        with redirect_stdout(f):
            print(str(x) + '\n')


X = np.array([np.array([652, 328, 554]),
              np.array([554]),
              np.array([652, 325, 211, 554]),
              np.array([419, 328, 554]),
              np.array([652, 328, 756]),
              np.array([756]),
              np.array([419, 328, 756]),
              np.array([652, 328, 667]),
              np.array([1080, 325]),
              np.array([1080]),
              np.array([424]),
              np.array([667])])

maxim = 1080
for i in range(len(X)):
    for j in range(len(X[i])):
        X[i][j] /= maxim
for line in X:
    line.reshape((line.shape[0], seq_len))

Y = np.array([np.array([0, 0, 0, 0]),
              np.array([0, 0, 0, 0]),
              np.array([0, 0, 0, 0]),
              np.array([0, 0, 0, 0]),
              np.array([0, 0.2, 0, 0]),
              np.array([0, 0.2, 0, 0]),
              np.array([0, 0.2, 0, 0]),
              np.array([0, 0.4, 0, 0]),
              np.array([0, 0.4, 0, 0]),
              np.array([0, 0.4, 0, 0]),
              np.array([0, 0.4, 0, 0]),
              np.array([0, 0.4, 0, 0])], dtype=float)
for line in Y:
    line.reshape((line.shape[0], seq_len))

U = np.random.uniform(0, 1, (hidden_dim, seq_len))
V = np.random.uniform(0, 1, (output_dim, hidden_dim))
W = np.random.uniform(0, 1, (hidden_dim, hidden_dim))

U, V, W = train(U, V, W, X, Y)

print_redirect(U, 'params.txt')
print_redirect(V, 'params.txt')
print_redirect(W, 'params.txt')

predictions = []
for i in range(Y.shape[0]):
    x, y = X[i], Y[i]
    prev_activation = np.zeros((hidden_dim, 1))
    # forward pass
    for timestep in range(seq_len):
        mulu = np.dot(U, x)
        mulw = np.dot(W, prev_activation)
        _sum = mulu + mulw
        activation = sigmoid(_sum)
        mulv = np.dot(V, activation)
        prev_activation = activation
    predictions.append(mulv)

predictions = np.array(predictions)
print('Expected: ')
print(Y)
print('\n')
print("Result")
print(predictions)'''


'''
def sigmoid(Z):
    A = 1 / (1 + np.exp(np.dot(-1, Z)))
    cache = Z

    return A, cache


def cost_function(A, Y):
    m = Y.shape[1]

    cost = (-1 / m) * (np.dot(np.log(A), Y.T) + np.dot(np.log(1 - A), 1 - Y.T))

    return cost


class Network:

    def __init__(self, layer_dims: list):
        self.__Layer_Dims = layer_dims
        self.Params = {}
        self.__init_params()

    def __init_params(self):
        # np.random.seed(3)
        layers_count = len(self.__Layer_Dims)

        for layer in range(1, layers_count):
            self.Params['W' + str(layer)] = np.random.randn(self.__Layer_Dims[layer],
                                                            self.__Layer_Dims[layer - 1]) * 0.01
            self.Params['b' + str(layer)] = np.zeros((self.__Layer_Dims[layer], 1))

    def __forward_prop(self, X):

        A = X  # input to first layer i.e. training data
        caches = []
        layer_count = len(self.Params) // 2
        for layer in range(1, layer_count + 1):
            A_prev = A

            # Linear Hypothesis
            Z = np.dot(A_prev, np.transpose(self.Params['W' + str(layer)]))  # + self.Params['b' + str(layer)]

            # Storing the linear cache
            linear_cache = (A_prev, self.Params['W' + str(layer)], self.Params['b' + str(layer)])

            # Applying sigmoid on linear hypothesis
            A, activation_cache = sigmoid(Z)

            # storing the both linear and activation cache
            cache = (linear_cache, activation_cache)
            caches.append(cache)

        return A, caches

    def __one_layer_backward(self, dA, cache):
        linear_cache, activation_cache = cache

        Z = activation_cache
        print(dA.shape)
        dZ = dA * sigmoid(Z)[0] * (1 - sigmoid(Z)[0])  # The derivative of the sigmoid function

        A_prev, W, b = linear_cache
        m = A_prev.shape[1]

        dW = (1 / m) * np.dot(A_prev.T, dZ)
        db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
        dA_prev = np.dot(dZ, W)

        return dA_prev, dW, db

    def __backprop(self, AL, Y, caches):
        grads = {}
        L = len(caches)
        m = AL.shape[1]
        Y = Y.reshape(AL.shape)

        dAL = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

        current_cache = caches[L - 1]
        grads['dA' + str(L - 1)], grads['dW' + str(L - 1)], grads['db' + str(L - 1)] = self.__one_layer_backward(dAL, current_cache)
        for l in range(1, L):
            current_cache = caches[l]
            dA_prev_temp, dW_temp, db_temp = self.__one_layer_backward(grads["dA" + str(l)], current_cache)
            grads["dA" + str(l + 1)] = dA_prev_temp
            grads["dW" + str(l + 1)] = dW_temp
            grads["db" + str(l + 1)] = db_temp
        return grads

    def __update_parameters(self, grads, learning_rate):
        L = len(self.Params) // 2
        for l in range(L):
            self.Params['W' + str(l + 1)] = self.Params['W' + str(l + 1)].T - learning_rate * grads['dW' + str(l + 1)]
            # self.Params['b' + str(l + 1)] = self.Params['b' + str(l + 1)] - learning_rate * grads['db' + str(l + 1)]

    def train(self, X, Y, epochs, lr):
        cost_history = []

        for i in range(epochs):
            print('Training ', i+1)
            Y_hat, caches = self.__forward_prop(X)
            cost = cost_function(Y_hat, Y)
            cost_history.append(cost)
            grads = self.__backprop(Y_hat, Y, caches)
            print(grads)
            exit(1)

            self.__update_parameters(grads, lr)

        return self.Params, cost_history
'''
