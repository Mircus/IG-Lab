import numpy as np
from iglab.duality import (bregman,three_point_residual,kl_projection_equal_first_two,
                          neg_entropy,neg_entropy_grad)
from iglab.categorical import kl


def test_kl_is_negative_entropy_bregman_on_simplex():
    p=np.array([.2,.3,.5]);q=np.array([.4,.4,.2])
    assert np.isclose(kl(p,q),bregman(neg_entropy,neg_entropy_grad,p,q))


def test_bregman_three_point_identity():
    a=np.array([.2,.3,.5]);b=np.array([.3,.3,.4]);c=np.array([.1,.6,.3])
    l,r=three_point_residual(neg_entropy,neg_entropy_grad,a,b,c)
    assert np.isclose(l,r)


def test_kl_projection_pythagorean_identity_for_affine_constraint():
    q=np.array([.6,.3,.1]);r=kl_projection_equal_first_two(q)
    for a in [.1,.2,.3,.4]:
        p=np.array([a,a,1-2*a])
        assert np.isclose(kl(p,q),kl(p,r)+kl(r,q),atol=1e-11)


def test_projection_is_local_minimum():
    q=np.array([.6,.3,.1]);r=kl_projection_equal_first_two(q)
    for a in np.linspace(.02,.48,200):
        p=np.array([a,a,1-2*a])
        assert kl(p,q)>=kl(r,q)-1e-10
