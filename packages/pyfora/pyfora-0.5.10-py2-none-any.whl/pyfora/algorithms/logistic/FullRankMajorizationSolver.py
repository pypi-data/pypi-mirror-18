#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import numpy
import math


from Solver import Solver, ReturnValue


class FullRankMajorizationSolver(Solver):
    """
    A pure-python implementation of l2-regularized logistic regression using
    an Algorithm 2 of T. Jebara and A. Choromanska's paper
    "Majorization for CRFs and Latent Likelihoods",
    Neural Information Processing Systems (NIPS), December 2012.
    """
    def __init__(
            self, X, y,
            classZeroLabel,
            regularizer,
            tol,
            maxIters,
            splitLimit=1000000):
        fSum = FullRankMajorizationSolver.computeFSum(
            X, y, classZeroLabel)

        self.X = X
        self.regularizer = float(regularizer)
        self.tol = tol
        self.maxIters = maxIters
        self.classZeroLabel = classZeroLabel
        self.fSum = fSum
        self.nFeatures = X.shape[1]
        self.nSamples = X.shape[0]
        self.splitLimit = splitLimit

    @staticmethod
    def computeFSum(X, y, classZeroLabel):
        nRows = X.shape[0]

        def columnSum(column):
            def f(rowIx):
                if y[rowIx] == classZeroLabel:
                    return float(column[rowIx])

                return 0.0

            return sum(f(rowIx) for rowIx in xrange(nRows))

        return numpy.array(
            [columnSum(column) for column in X.columns()]
            )

    def solve(self, theta=None):
        if theta is None:
            oldTheta = numpy.zeros(self.nFeatures)
        else:
            oldTheta = theta

        newTheta = self.updateTheta(oldTheta)

        iters = 1
        while iters < self.maxIters and \
              sum((newTheta - oldTheta) ** 2) > self.tol * self.tol:
            oldTheta = newTheta
            newTheta = self.updateTheta(oldTheta)
            iters = iters + 1

        return ReturnValue(newTheta, iters)

    def updateTheta(self, theta):
        thetaDotX = self.X.dot(theta, self.splitLimit)
        sigma = self.computeSigma(thetaDotX)
        muSum = self.computeMuSum(thetaDotX)

        A = sigma + _diagonal(
            sigma.shape[0], self.X.shape[0] * self.regularizer)
        b = muSum - self.fSum + theta * (self.regularizer * self.X.shape[0])

        return theta - numpy.linalg.solve(A, b)

    def computeSigma(self, thetaDotX, start=0, end=None):
        # we have a few choices here: 
        # 1) We can precompute all of the outer products of the rows
        #    of X. This will require nCols * storage of X to hold,
        #    which may be prohibitive. Assuming this is held in a 
        #    single flattened vector, it would require a "strided"
        #    access patten to compute the weighted sums of these 
        #    outer products.
        # 2) We can compute the outer products as needed in a manner
        #    similar to the way we compute the X^t X matrix for linear 
        #    regression, this time usin "weighted dot products" on the 
        #    columns of X. This is the choice we're using for now.

        return _computeSigma(
            thetaDotX, self.X._columns, self.splitLimit, start, end)

    def computeMuSum(self, thetaDotX):
        # we could also stash these values in a vector, since they're common
        # to all columns. which is better?
        def rowWiseScalarMultiplier(ix):
            return 1.0 / (1.0 + math.exp(-thetaDotX[ix]))

        columns = self.X.columns()
        def computeWeightedColumnSum(columnIx):
            column = columns[columnIx]
            return sum(
                rowWiseScalarMultiplier(ix) * column[ix] \
                for ix in xrange(self.X.shape[0])
                )

        return numpy.array([
            computeWeightedColumnSum(columnIx) for \
            columnIx in xrange(self.X.shape[1])
            ])

def _computeSigma(thetaDotX, columns, splitLimit, start=0, end=None):
    if end is None:
        end = len(thetaDotX)

    if (end - start) < splitLimit:
        numColumns = len(columns)

        def unsymmetrizedElementAt(row, col):
            if col < row:
                return 0.0

            right = columns[col][start:end]
            left = columns[row][start:end]
            weights = thetaDotX[start:end]

            return _weightedDotProduct(right, left, weights)

        unsymmetrizedValues = [
            [unsymmetrizedElementAt(row, col) for col in xrange(numColumns)] \
            for row in xrange(numColumns)
            ]

        symmetrizedValues = []
        for row in xrange(numColumns):
            for col in xrange(numColumns):
                if row <= col:
                    elt = unsymmetrizedValues[row][col]
                else:
                    elt = unsymmetrizedValues[col][row]
                symmetrizedValues = symmetrizedValues + [elt]

        tr = numpy.array(symmetrizedValues)
        return tr.reshape((numColumns, numColumns))

    mid = (start + end) / 2
    return _computeSigma(thetaDotX, columns, splitLimit, start, mid) + \
        _computeSigma(thetaDotX, columns, splitLimit, mid, end)


def _weightedDotProduct(x1, x2, x3):
    res = 0.0
    ix = 0
    top = len(x1)
    while ix < top:
        res = res + x1[ix] * x2[ix] * _weightFun(x3[ix])
        ix = ix + 1

    return res


def _weightFun(x):
    exp_x = math.exp(x)

    if abs(x) < 1.0e-5:
        # taylor expand (exp(x) - 1) / (2x) near the origin
        return (0.5 - 0.25 * x) / (exp_x + 1.0)

    return (exp_x - 1.0) / (exp_x + 1.0) / (2.0 * x)


def _diagonal(n, value):
    # TODO this should be replaced by a proper numpy call
    value = float(value)

    def eltAtIx(ix):
        if ix % n == ix / n:
            return value
        else:
            return 0.0

    vals = [eltAtIx(ix) for ix in xrange(n * n)]

    tr = numpy.array(vals)
    tr = tr.reshape((n, n))

    return tr
        
