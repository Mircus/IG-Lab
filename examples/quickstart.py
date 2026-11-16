"""Print reproducible numeric checkpoints from the companion booklet."""
import numpy as np
from iglab import categorical as c, gaussian as g, duality as d, learning as l

p=np.array([.2,.3,.5]);u=np.array([.2,-.1,-.1])
K=c.splitting_channel([2,3,5]);q,v=c.push_forward(K,p,u)
print('Čencov refinement Fisher squared norm:',c.fisher_inner(p,u,u),'=',c.fisher_inner(q,v,v))
noisy=np.array([[.8,.2,.5],[.2,.8,.5]])
print('Fisher information contraction gap:',c.fisher_contraction_gap(noisy,p,u))
print('Gaussian paths (mean, sigma) at midpoint:')
for fn in [g.e_path,g.m_path,g.fisher_path]:
    print(' ',fn.__name__,fn((-1,1),(1,1),.5))
base=np.array([.6,.3,.1]);proj=d.kl_projection_equal_first_two(base)
print('I-projection p1=p2:',proj,'KL(p||q)=',c.kl(proj,base))
print('Bernoulli natural gradient exact p(1) from p(0)=0.2, y=1:',l.bernoulli_natural_flow(.2,1,1.))
