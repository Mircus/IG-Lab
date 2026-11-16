"""Coordinate-invariant learning flows on probability families."""

import numpy as np
from .categorical import simplex


def bernoulli_natural_velocity(p, y):
    if not 0 < p < 1 or y not in (0,1):
        raise ValueError("0<p<1 and y in {0,1} required")
    return y-p


def bernoulli_logit_velocity(theta, y):
    p = float(1. / (1. + np.exp(-theta)))
    return bernoulli_natural_velocity(p, y)/(p*(1.-p))


def replicator_velocity(p, costs):
    """Natural gradient descent of E_p[cost] for the categorical Fisher metric."""
    p = simplex(p)
    c = np.asarray(costs, dtype=float)
    if c.shape != p.shape or not np.all(np.isfinite(c)):
        raise ValueError("finite costs of matching shape required")
    return -p*(c-np.dot(p,c))


def bernoulli_natural_flow(p0, y, t):
    """Exact p(t) for negative log-likelihood natural gradient flow."""
    if not 0 < p0 < 1 or y not in (0,1) or t < 0:
        raise ValueError("valid p0, y, t>=0 required")
    return float(y + (p0-y)*np.exp(-t))
