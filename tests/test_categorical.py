import numpy as np
import pytest
from iglab.categorical import (simplex,tangent,fisher_inner,fisher_distance,
    fisher_geodesic,kl,splitting_channel,deterministic_recovery,
    fisher_contraction_gap,push_forward)


def test_fisher_positive_and_symmetric():
    p = [.2,.3,.5]; u=[.1,-.3,.2]; v=[-.2,.1,.1]
    assert fisher_inner(p,u,u)>0
    assert np.isclose(fisher_inner(p,u,v), fisher_inner(p,v,u))


def test_fisher_sphere_formula():
    p=np.array([.1,.3,.6]); q=np.array([.3,.5,.2]);
    assert np.isclose(fisher_distance(p,q), 2*np.arccos(np.dot(np.sqrt(p),np.sqrt(q))))


def test_geodesic_endpoints_and_constant_speed():
    p=np.array([.1,.3,.6]); q=np.array([.5,.4,.1])
    assert np.allclose(fisher_geodesic(p,q,0),p)
    assert np.allclose(fisher_geodesic(p,q,1),q)
    m=fisher_geodesic(p,q,.4)
    assert np.isclose(fisher_distance(p,m),.4*fisher_distance(p,q),rtol=1e-11,atol=1e-9)


def test_kl_locally_half_spherical_distance_squared():
    p=np.array([.2,.3,.5]);u=np.array([1.,-1.,0.])
    for eps in [1e-3,1e-4]:
        q=p+eps*u
        assert abs(kl(p,q)-0.5*fisher_distance(p,q)**2)<20*eps**3


def test_chentsov_refinement_isometry_for_rationals():
    counts=[2,3,5]
    p=np.array(counts,dtype=float)/sum(counts)
    u=np.array([.2,-.1,-.1]); v=np.array([.1,-.3,.2])
    K=splitting_channel(counts);L=deterministic_recovery(counts)
    q,ku=push_forward(K,p,u);_,kv=push_forward(K,p,v)
    assert np.allclose(q,np.full(sum(counts),1/sum(counts)))
    assert np.allclose(L@K,np.eye(3))
    assert np.isclose(fisher_inner(p,u,v),fisher_inner(q,ku,kv))


def test_uniform_barycenter_comparison():
    for n,m in [(2,3),(3,4),(5,2)]:
        k=splitting_channel([m]*n)
        p=np.full(n,1/n);u=np.array([1,-1]+[0]*(n-2),dtype=float)
        q,ku=push_forward(k,p,u)
        assert np.isclose(fisher_inner(q,ku,ku),fisher_inner(p,u,u))


def test_markov_data_processing_fisher():
    p=np.array([.2,.3,.5]);u=np.array([.1,.1,-.2])
    K=np.array([[.8,.2,.5],[.2,.8,.5]])
    assert fisher_contraction_gap(K,p,u)>=-1e-12
    assert fisher_contraction_gap(K,p,u)>1e-3


def test_markov_data_processing_kl():
    p=np.array([.2,.3,.5]);q=np.array([.3,.2,.5]);K=np.array([[.7,.4,.3],[.3,.6,.7]])
    assert kl(push_forward(K,p),push_forward(K,q))<=kl(p,q)+1e-12


@pytest.mark.parametrize('bad', [[0,1],[.2,.2],[np.nan,.5],[1.1,-.1]])
def test_simplex_rejects_boundary_and_invalid(bad):
    with pytest.raises(ValueError):
        simplex(bad)


def test_rejects_nontangent_vector():
    with pytest.raises(ValueError):
        tangent([.5,.5],[.2,.3])
