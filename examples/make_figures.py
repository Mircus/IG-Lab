"""Reproduce the visual checks used in the research supplement.

Run from repository root: python examples/make_figures.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from iglab.gaussian import fisher_path, e_path, m_path
from iglab.categorical import fisher_contraction_gap, splitting_channel, fisher_geodesic
from iglab.learning import bernoulli_natural_flow

out=Path(__file__).resolve().parents[1]/'figures'
out.mkdir(exist_ok=True)

def gaussians():
    ts=np.linspace(0,1,201)
    for fn,lab,fmt in [(fisher_path,'Fisher geodesic','-'),(e_path,'exponential-affine','--'),(m_path,'mixture-affine','-.')]:
        xy=np.array([fn((-1,1),(1,1),t) for t in ts])
        plt.plot(xy[:,0],np.sqrt(2)*xy[:,1],fmt,label=lab,linewidth=2)
    plt.scatter([-1,1],[np.sqrt(2)]*2,color='black',s=22)
    plt.xlabel(r'$\mu$');plt.ylabel(r'$\sqrt{2}\sigma$')
    plt.title('Three paths in the Gaussian manifold')
    plt.legend(frameon=False);plt.tight_layout()
    plt.savefig(out/'gaussian_three_paths.png',dpi=180);plt.close()

def markov():
    p=np.array([.2,.3,.5]);u=np.array([.1,.1,-.2])
    K=np.array([[.8,.2,.5],[.2,.8,.5]])
    gap=fisher_contraction_gap(K,p,u)
    KR=splitting_channel([2,3,5]);gap2=fisher_contraction_gap(KR,p,u)
    plt.bar(['noisy channel','sufficient split'],[gap,gap2])
    plt.ylabel('Fisher norm contraction gap')
    plt.title('Local data processing')
    plt.tight_layout();plt.savefig(out/'data_processing.png',dpi=180);plt.close()

def bernoulli():
    ts=np.linspace(0,4,200)
    for y in [0,1]:
        ps=[bernoulli_natural_flow(.2,y,t) for t in ts]
        plt.plot(ts,ps,label=f'observation y={y}')
    plt.ylim(0,1);plt.xlabel('flow time');plt.ylabel('Bernoulli probability')
    plt.title('Natural-gradient flow is exactly solvable')
    plt.legend(frameon=False)
    plt.tight_layout();plt.savefig(out/'bernoulli_natural_flow.png',dpi=180);plt.close()

if __name__=='__main__':
    gaussians();markov();bernoulli();print(f'Saved 3 figures in {out}')
