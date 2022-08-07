import numpy
from copy import deepcopy

import sys

# -------------------------
# Feed-forward network
# -------------------------
class Network:

    def __init__(self, layers):
        self.layers = layers

    def forward(self, Y, phase='TEST'):
        for l in self.layers: Y = l.forward(Y,phase)
        return Y

    def backward(self, DY, phase='TEST'):
        for l in self.layers[::-1]: DY = l.backward(DY,phase)
        return DY

        def update(self, lr):
                for l in self.layers: l.update(lr)

        def dump(self):
                for l in self.layers: l.dump()


        def train_softmaxontop(self, X, Y, Xval=[], Yval=[], batchsize=25, iters=10000, lrate=0.0005, lrate_decay='phase', lrdecay_step = 3000, lrdecay_factor = 0.5 , status=250, transform=None):

            '''        
                X the training data
                Y the training labels
               
                Xval some validation data
                Yval the validation data labels
               
                batchsize the batch size to use for training
                iters max number of training iterations.
                lrate the learning rate is adjusted during training with increased model performance. See lrate_decay
                lrate_decay controls if and how the learning rate reduced
                    'none' or None disables this behaviour
                    'sublinear' adjusts the learning rate to lrate*(1-Accuracy^2) during an evaluation step resulting in a better performing model
                    'linear' adjusts the learning rate to lrate*(1-Accuracy) during an evaluation step resulting in a better performing model
                status number of iterations of silent training until status print and evaluation on validation data.
                convergence number of consecutive allowed status evaulations with no more model improvements until we accept the model has converged. Set <=0 to disable.
                transform a function taking as an input a batch of training data sized [N,D] and returning a batch sized [N,D] with added noise or other various data transformations.
                    default value is None for no transformation.
            '''

        

            testbatchsize=50
            accuracyiterationnumber_cap=60

            learningFactor = 1.0
            bestAccuracy = 0.0
            bestLayers = deepcopy(self.layers)
                   
            #N, D = X.shape 
            N=X.shape[0]
       
            for i in xrange(iters):
                #print 'iter ',i
                # the actual training: pick samples at random
                r = numpy.random.permutation(N)
                samples = r[0:batchsize]
               
                if transform == None:
                    batch = X[samples, :]
                else:
                    batch = transform(X[samples, :])

                if lrate_decay == None or lrate_decay == 'none':
                    pass  # no adjustment
                elif lrate_decay == 'phase':
            if (i>0) and (i % lrdecay_step == 0 ) :
                learningFactor = learningFactor * lrdecay_factor
               
                # forward and backward propagation steps with parameter update
                    # run a forward pass            
                Ypred = self.forward(batch, phase='TRAIN')
                    #backpropagate the gradient 
                self.backward(Ypred - Y[samples, :], phase='TRAIN')
                    #update parameters
                self.update(lrate * learningFactor)


                # periodically evaluate network and optionally adjust learning rate or check for convergence.
                if (i + 1) % status == 0:
            testiters1=  min(int(N/testbatchsize), accuracyiterationnumber_cap/2)
            acc=0
            print ' computing train accuracy'
            for t in xrange(testiters1):
                #print 'training set accuracy iter ',t ,'out of', testiters1
                        Ypred = self.forward(X[t*testbatchsize:(t+1)*testbatchsize,:])
                v= numpy.mean(numpy.argmax(Ypred, axis= len(Ypred.shape)-1 ) == \
                numpy.argmax(Y[t*testbatchsize:(t+1)*testbatchsize,:], axis=len(Y.shape)-1 ))*1.0
                        acc = acc+ v*1.0/testiters1
                    print
                    print 'Accuracy after {0} iterations: {1}%'.format(i + 1, acc * 100)
                    if not Xval == [] and not Yval == []:
                print ' computing validation accuracy'
                Nval=Xval.shape[0]
                testiters2= min(int(Nval/testbatchsize), accuracyiterationnumber_cap)

                acc_val = 0
                for t in xrange(testiters2):
                #print 'validation set accuracy iter ',t ,'out of', testiters2
                            Ypred = self.forward(Xval[t*testbatchsize:\
                (t+1)*testbatchsize,:])                
                            acc_val = acc_val+numpy.mean(numpy.argmax(Ypred, axis= len(Y.shape)-1 ) == \
                numpy.argmax(Yval[t*testbatchsize:(t+1)*testbatchsize,:], axis= len(Y.shape)-1 ))*1.0/testiters2
                        print 'Accuracy on VALIDATION set: {1}%'.format(i + 1, acc_val * 100)


                       print 'Accuracy on TRAIN SET after {0} iterations: {1}%'.format(i + 1, acc * 100)

            if not Xval == [] and not Yval == []:
                acc = acc_val

                    if acc > bestAccuracy:
                        print '    New optimal parameter set encountered. saving....'
                        bestAccuracy = acc
                        bestLayers = deepcopy(self.layers)

                   
                elif (i + 1) % (status / 10) == 0:
                    # print 'alive' signal
                    sys.stdout.write('.')
                    sys.stdout.flush()
           
            # after training, either due to convergence or iteration limit
            print 'Setting network parameters to best encountered network state with {0}% accuracy.'.format(bestAccuracy * 100)
            self.layers = bestLayers

   

# -------------------------
# ReLU activation layer
# -------------------------
class ReLU:

    def forward(self, X, phase='TEST'):
        pass
        #please implement here
        self.X = X
        return np.max(X, np.zeros(X.shape))

    def backward(self, DY, phase='TEST'):
        pass
        #please implement here
        self.DY = DY
        return DY * np.sign(np.max(X, np.zeros(X.shape)))

        def update(self, lr): pass

        def dump(self): pass


# -------------------------
# Fully-connected layer
# -------------------------
class Linear:

    '''
    def __init__(self, name):
        self.W = numpy.loadtxt(name + '-W.txt')
        self.B = numpy.loadtxt(name + '-B.txt')
    '''
        def __init__(self,m,n,name):

                self.name = name
                self.W = numpy.random.normal(0,1.0/m**.5,[m,n])
                self.B = numpy.zeros([n])

        self.oldDW=None
        self.oldDB=None    
        self.momentum=0.9

        self.rmspropnorm=0
        self.rmsprop_emaconst=0.9

        self.updnorm = 0

    def forward(self, X, phase='TEST'):
        self.X = X
        return numpy.dot(self.X, self.W) + self.B

    def backward(self, DY, phase='TEST'):
        self.DY = DY
        return numpy.dot(self.DY, self.W.T)

        def update(self, lr):
        #standard update
                self.DW = numpy.dot(self.X.T, self.DY)
                self.DB = self.DY.sum(axis=0)
                self.W -= lr * self.DW
                self.B -= lr * self.DB
                #self.B = numpy.minimum(0, self.B)

 

        def dump(self):
                numpy.savetxt(self.name + '-W.txt', self.W, fmt='%.3f')
                numpy.savetxt(self.name + '-B.txt', self.B, fmt='%.3f')


# -------------------------
# Sum-pooling layer
# -------------------------
class Pooling:

    def forward(self, X, phase='TEST'):
        self.X = X
        self.Y = 0.5 * (X[:, ::2, ::2, :] + X[:, ::2, 1::2, :] + X[:, 1::2, ::2, :] + X[:, 1::2, 1::2, :])
        return self.Y

    def backward(self, DY, phase='TEST'):
        self.DY = DY
        DX = self.X * 0
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]: DX[:, i::2, j::2, :] += DY * 0.5
        return DX

        def update(self, lr): pass

        def dump(self): pass


