"""Finite-simplex Fisher geometry and stochastic transformations.

All laws lie in the strictly positive categorical simplex. Stochastic matrices
use columns for INPUT classes and rows for OUTPUT classes: q=K @ p.
"""

from __future__ import annotations
import numpy as np


def simplex(p):
    """Validate a strictly positive, normalized probability vector."""
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or p.size < 2 or not np.all(np.isfinite(p)):
        raise ValueError("p must be a finite probability vector with >=2 entries")
    if np.any(p <= 0.0) or not np.isclose(p.sum(), 1., atol=1e-12):
        raise ValueError("p must have strictly positive entries summing to one")
    return p


def tangent(p, u):
    p = simplex(p)
    u = np.asarray(u, dtype=float)
    if u.shape != p.shape or not np.all(np.isfinite(u)) or not np.isclose(u.sum(), 0., atol=1e-12):
        raise ValueError("tangent vectors must have the same shape as p and sum to zero")
    return u


def fisher_inner(p, u, v):
    p = simplex(p)
    u, v = tangent(p, u), tangent(p, v)
    return float(np.dot(u / p, v))


def fisher_distance(p, q):
    p, q = simplex(p), simplex(q)
    if p.shape != q.shape:
        raise ValueError("p and q must have the same dimension")
    affinity = np.dot(np.sqrt(p), np.sqrt(q))
    return 2. * float(np.arccos(np.clip(affinity, -1., 1.)))


def fisher_geodesic(p, q, t):
    """Constant-speed Fisher geodesic; t lies in [0,1]."""
    p, q = simplex(p), simplex(q)
    if p.shape != q.shape or not 0 <= t <= 1:
        raise ValueError("matching simplexes and 0 <= t <= 1 required")
    a, b = np.sqrt(p), np.sqrt(q)
    theta = float(np.arccos(np.clip(np.dot(a, b), -1., 1.)))
    if theta < 1e-8:
        y = (1-t)*a + t*b
    else:
        y = np.sin((1-t)*theta)/np.sin(theta)*a + np.sin(t*theta)/np.sin(theta)*b
    result = y*y
    return result / result.sum()


def kl(p, q):
    p, q = simplex(p), simplex(q)
    if p.shape != q.shape:
        raise ValueError("dimension mismatch")
    return float(np.sum(p * np.log(p/q)))


def channel(K):
    K = np.asarray(K, dtype=float)
    if K.ndim != 2 or min(K.shape) < 2 or not np.all(np.isfinite(K)):
        raise ValueError("channel must be a finite matrix with >=2 rows and columns")
    if np.any(K < 0) or not np.allclose(K.sum(axis=0), 1., atol=1e-12):
        raise ValueError("each column of K must be a probability distribution")
    return K


def push_forward(K, p, u=None):
    K, p = channel(K), simplex(p)
    if K.shape[1] != p.size:
        raise ValueError("input dimension mismatch")
    q = K @ p
    if np.any(q <= 0):
        raise ValueError("output channel has unreachable outcomes: restrict to active support")
    if u is None:
        return q
    return q, K @ tangent(p, u)


def fisher_contraction_gap(K, p, u):
    """Nonnegative by conditional Jensen: g_p(u,u)-g_{Kp}(Ku,Ku)."""
    q, v = push_forward(K, p, u)
    return fisher_inner(p, u, u) - fisher_inner(q, v, v)


def splitting_channel(block_sizes):
    """Congruent embedding: split input i uniformly into block_sizes[i] states."""
    sizes = np.asarray(block_sizes, dtype=int)
    if sizes.ndim != 1 or sizes.size < 2 or np.any(sizes < 1):
        raise ValueError("positive block sizes with >=2 inputs required")
    K = np.zeros((int(sizes.sum()), sizes.size))
    start = 0
    for i, a in enumerate(sizes):
        K[start:start+a, i] = 1. / a
        start += a
    return K


def deterministic_recovery(block_sizes):
    """Recovery L with L @ K = I for K=splitting_channel(block_sizes)."""
    sizes = np.asarray(block_sizes, dtype=int)
    L = np.zeros((sizes.size, int(sizes.sum())))
    start = 0
    for i, a in enumerate(sizes):
        L[i, start:start+a] = 1.
        start += a
    return L
