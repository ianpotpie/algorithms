from math import ceil, log2
from random import random


def cmv(A, thresh=None, epsilon=0.99, delta=0.9):
    """
    Proposed by Sourav Chakraborty, Kuldeep S. Meel., and N. V. Vinodchandran
    in the paper "Distinct Elements in Streams: An Algorithm for the Textbook".

    This algorithm provides an unbiased estimator for the number of unique
    elements in a stream given a limited buffer size.

    epsilon: accuracy
    delta: confidence (probability of exceeding accuracy)

    space complexity (thresh) = ceil((12 / (epsilon ** 2)) * log2((8 / delta)))
    """

    p = 1
    X = set()
    if thresh is None:
        thresh = ceil((12 / (epsilon**2)) * log2((8 / delta)))

    for a in A:

        # remove previous elements, so only the probabilty of the
        # last element matters
        X.discard(a)

        # an element has a p=1/2^k probability of being added to X
        # where k is the number of 'halvings'
        if random() < p and len(X) < thresh:
            X.add(a)

        # an element has probability of 1/2^k of being added initially
        # elements are removed with probabilty 1/2
        # the probability of an element being added and remaining
        # p * 1/2 = 1/2^k * 1/2 = 1/2^(k+1)
        # p is updated to 1/2^(k+1)
        # future elements are added with the same probability p=1/2^(k+1)
        if len(X) >= thresh:
            X = {x for x in X if random() < 0.5}
            p /= 2

    # every element of A is in X with probability p=1/2^k
    # so |X|~|A|*p and |X|/p~|A|
    return len(X) / p
