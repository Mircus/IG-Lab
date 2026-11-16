import numpy as np
import sympy as sp
from iglab.learning import (bernoulli_natural_velocity,bernoulli_logit_velocity,
                            bernoulli_natural_flow,replicator_velocity)
from iglab.symbolic import bernoulli_fisher_by_kl,gaussian_fisher_by_scores


def test_bernoulli_coordinate_invariance():
    for p in [.13,.3,.7,.91]:
        theta=np.log(p/(1-p))
        for y in [0,1]:
            assert np.isclose(p*(1-p)*bernoulli_logit_velocity(theta,y),bernoulli_natural_velocity(p,y))


def test_natural_flow_exact():
    assert np.isclose(bernoulli_natural_flow(.2,1,0),.2)
    assert np.isclose(bernoulli_natural_flow(.2,1,1),1-.8*np.exp(-1))


def test_replicator_tangent_and_descent():
    p=np.array([.1,.3,.6]);c=np.array([2.,-1.,.3]);v=replicator_velocity(p,c)
    assert np.isclose(v.sum(),0)
    assert np.dot(v,c)<0


def test_bernoulli_fisher_symbolic():
    p=sp.symbols('p',positive=True)
    assert sp.simplify(bernoulli_fisher_by_kl()-1/(p*(1-p)))==0


def test_gaussian_fisher_symbolic():
    sigma=sp.symbols('sigma',positive=True,real=True)
    assert gaussian_fisher_by_scores()==sp.diag(1/sigma**2,2/sigma**2)
