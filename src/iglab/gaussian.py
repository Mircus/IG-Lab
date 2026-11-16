"""Univariate Gaussian information geometry."""

import numpy as np


def _check(mu, sigma):
    if not np.isfinite(mu) or not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("mu finite and sigma > 0 required")


def fisher_matrix(mu, sigma):
    _check(mu, sigma)
    return np.diag([1. / sigma**2, 2. / sigma**2])


def fisher_distance(first, second):
    """Exact distance in a hyperbolic plane of curvature -1/2."""
    m1, s1 = first
    m2, s2 = second
    _check(m1, s1)
    _check(m2, s2)
    a = ((m1 - m2)**2 + 2. * (s1 - s2)**2) / (4. * s1 * s2)
    return float(np.sqrt(2.) * np.arccosh(1. + max(0., a)))


def e_path(first, second, t):
    """Exponential-affine path via natural (precision) coordinates."""
    if not 0 <= t <= 1:
        raise ValueError("0 <= t <= 1 required")
    m1, s1 = first
    m2, s2 = second
    _check(m1, s1)
    _check(m2, s2)
    eta_1 = (1-t)*m1/s1**2 + t*m2/s2**2
    precision = (1-t)/s1**2 + t/s2**2
    return float(eta_1 / precision), float(np.sqrt(1. / precision))


def m_path(first, second, t):
    """Mixture-affine path via expectation (first, second moments) coordinates.

    This is not the literal mixture density of two Gaussians, which is usually
    non-Gaussian; it is a straight path in the Gaussian expectation parameters.
    """
    if not 0 <= t <= 1:
        raise ValueError("0 <= t <= 1 required")
    m1, s1 = first
    m2, s2 = second
    _check(m1, s1)
    _check(m2, s2)
    mean = (1-t)*m1 + t*m2
    second_moment = (1-t)*(m1*m1 + s1*s1) + t*(m2*m2 + s2*s2)
    return float(mean), float(np.sqrt(max(0., second_moment - mean**2)))


def fisher_path(first, second, t):
    """Hyperbolic geodesic by normalized square-root coordinate half-plane.

    Uses a hyperbolic circle orthogonal to the boundary, or a vertical line.
    Parameter t is normalized Euclidean angle, not constant Fisher speed.
    """
    if not 0 <= t <= 1:
        raise ValueError("0 <= t <= 1 required")
    m1, s1 = first
    m2, s2 = second
    _check(m1, s1)
    _check(m2, s2)
    x1, y1 = m1, np.sqrt(2.)*s1
    x2, y2 = m2, np.sqrt(2.)*s2
    if np.isclose(x1, x2):
        return float(x1), float(s1**(1-t)*s2**t)
    c = (x2*x2+y2*y2-x1*x1-y1*y1)/(2*(x2-x1))
    r = float(np.hypot(x1-c, y1))
    a1, a2 = np.arctan2(y1, x1-c), np.arctan2(y2, x2-c)
    a = (1-t)*a1 + t*a2
    return float(c + r*np.cos(a)), float(r*np.sin(a)/np.sqrt(2.))
