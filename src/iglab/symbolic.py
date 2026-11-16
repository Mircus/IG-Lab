"""Symbolic checks, not a general information-geometry tensor engine."""

import sympy as sp


def bernoulli_fisher_by_kl():
    p, q = sp.symbols('p q', positive=True)
    div = p*sp.log(p/q)+(1-p)*sp.log((1-p)/(1-q))
    return sp.simplify(sp.diff(div,q,2).subs(q,p))


def gaussian_fisher_by_scores():
    """Gaussian score moments from E Z^2=1, E Z^4=3."""
    sigma, z = sp.symbols('sigma z', positive=True, real=True)
    score_mu = z/sigma
    score_sig = (z*z-1)/sigma
    def E(expr):
        polynomial = sp.Poly(sp.expand(expr),z)
        moments = {0:1,1:0,2:1,3:0,4:3}
        return sp.simplify(sum(coef*moments.get(deg[0],0) for deg,coef in polynomial.terms()))
    return sp.Matrix([[E(score_mu**2), E(score_mu*score_sig)],
                      [E(score_mu*score_sig), E(score_sig**2)]])
