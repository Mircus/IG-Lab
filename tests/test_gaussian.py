import numpy as np
from iglab.gaussian import fisher_matrix, fisher_distance, e_path,m_path,fisher_path


def test_gaussian_metric():
    assert np.allclose(fisher_matrix(2,3),[[1/9,0],[0,2/9]])


def test_equal_mean_vertical_hyperbolic_distance():
    assert np.isclose(fisher_distance((0,1),(0,2)),np.sqrt(2)*np.log(2))


def test_gaussian_invariance_translation_and_scale():
    a=(-1,1); b=(2,3)
    for factor,shift in [(2,3),(.25,-8)]:
        assert np.isclose(fisher_distance(a,b),fisher_distance((a[0]*factor+shift,a[1]*factor),(b[0]*factor+shift,b[1]*factor)))


def test_three_different_gaussian_midpoints():
    a=2
    left=(-a,1);right=(a,1)
    em=e_path(left,right,.5)
    mm=m_path(left,right,.5)
    fm=fisher_path(left,right,.5)
    assert np.isclose(em[1]**2,1)
    assert np.isclose(mm[1]**2,1+a*a)
    assert np.isclose(fm[1]**2,1+a*a/2)


def test_path_endpoints():
    for fn in [e_path,m_path,fisher_path]:
        a=(-2,.4);b=(1,1.5)
        assert np.allclose(fn(a,b,0),a)
        assert np.allclose(fn(a,b,1),b)


def test_curvature_metric_scaling():
    # In u=mu, v=sqrt(2)*sigma coordinates, g=2*(du^2+dv^2)/v^2.
    sigma=.7
    guu=2/(np.sqrt(2)*sigma)**2
    assert np.isclose(fisher_matrix(0,sigma)[0,0],guu)
