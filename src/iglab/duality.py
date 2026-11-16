"""Divergence, convex potentials, and information projection."""

import numpy as np
from .categorical import kl, simplex


def bregman(F, gradF, x, y):
    """B_F(x,y) = F(x)-F(y)-<gradF(y), x-y>."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    return float(F(x) - F(y) - np.dot(gradF(y), x-y))


def three_point_residual(F, gradF, x, y, z):
    """Both sides of the exact Bregman three-point identity."""
    x, y, z = map(lambda a: np.asarray(a, dtype=float), (x,y,z))
    left = bregman(F,gradF,x,z) - bregman(F,gradF,x,y) - bregman(F,gradF,y,z)
    right = np.dot(x-y, gradF(y)-gradF(z))
    return float(left), float(right)


def kl_projection_equal_first_two(q):
    """Minimize KL(p||q) over p1=p2 on the positive 3-simplex.

    Unique minimizer exists and has p1=p2 proportional to sqrt(q1*q2).
    """
    q = simplex(q)
    if q.size != 3:
        raise ValueError("q must have 3 entries")
    r = np.sqrt(q[0]*q[1])
    z = 2*r+q[2]
    return np.array([r/z,r/z,q[2]/z])


def neg_entropy(x):
    x = simplex(x)
    return float(np.dot(x, np.log(x)))


def neg_entropy_grad(x):
    return np.log(simplex(x)) + 1.
