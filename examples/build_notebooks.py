"""Generate four small self-contained lab notebooks (uses only stdlib)."""
import json
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'notebooks'

def nb(name,steps):
    cells=[]
    for index,(kind,source) in enumerate(steps):
        cells.append({'cell_type':'markdown' if kind=='md' else 'code',
                      'id':f'cell-{index:02d}','metadata':{},'source':source.splitlines(keepends=True),
                      **({} if kind=='md' else {'execution_count':None,'outputs':[]})})
    doc={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
    (out/name).write_text(json.dumps(doc,indent=2)+'\n',encoding='utf8')

nb('01_cencov_uniqueness.ipynb',[
('md','# Čencov and the metric forced by refinement\n\n**Claim:** split a rational probability vector into equal cells. Fisher norms are preserved; arbitrary noisy channels cannot increase them. This is a computational check, **not** a proof of the theorem.'),
('code','import numpy as np\nfrom iglab.categorical import *\ncounts=[2,3,5]\np=np.array(counts)/sum(counts)\nu=np.array([.2,-.1,-.1])\nK=splitting_channel(counts)\nq,v=push_forward(K,p,u)\nprint("refinement:",fisher_inner(p,u,u),fisher_inner(q,v,v))\nprint("recovery:",np.allclose(deterministic_recovery(counts)@K,np.eye(3)))'),
('code','noisy=np.array([[.8,.2,.5],[.2,.8,.5]])\nprint("noisy-channel contraction:", fisher_contraction_gap(noisy,p,u))')])
nb('02_gaussian_three_paths.ipynb',[
('md','# Three geometries of straightness\n\nThe exponential and mixture paths are *affine coordinate lines*; the Fisher geodesic minimizes Riemannian length. They are generally different.'),
('code','from iglab.gaussian import *\nimport numpy as np\nfor f in [e_path,m_path,fisher_path]:\n    m,s=f((-2,1),(2,1),.5)\n    print(f.__name__,m,"variance",s*s)')])
nb('03_dual_projection.ipynb',[
('md','# Bregman–KL projection\n\nMinimize KL(p||q) on the affine constraint p1=p2. The Pythagorean equality holds for *every* feasible p, because the projection lands in the relative interior of an affine set.'),
('code','from iglab.categorical import kl\nfrom iglab.duality import kl_projection_equal_first_two\nimport numpy as np\nq=np.array([.6,.3,.1]);r=kl_projection_equal_first_two(q)\nfor a in [.1,.25,.4]:\n p=np.array([a,a,1-2*a])\n print(a,kl(p,q),kl(p,r)+kl(r,q))')])
nb('04_natural_gradient.ipynb',[
('md','# Natural-gradient invariance\n\nThe same Bernoulli probability flow emerges in probability p and logit θ coordinates.'),
('code','import numpy as np\nfrom iglab.learning import *\nfor p in [.1,.4,.8]:\n th=np.log(p/(1-p))\n print(p, bernoulli_natural_velocity(p,1), p*(1-p)*bernoulli_logit_velocity(th,1))'),
('code','print("replicator velocity:",replicator_velocity(np.array([.2,.3,.5]),np.array([1.,2.,-1.])))')])
print('wrote four notebooks')
