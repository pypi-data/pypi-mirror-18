# This package is created by Jiangshan(Tonny) Ma in his Ph.D. work in Tokyo Institute of Technology
# In some Linux distributions such as Redhat, Fedora or Centos, you may see the 
# "error: g++ error:/usr/lib/rpm/redhat/redhat-hardened-cc1 No that file and directory",
# in that case, "sudo dnf install redhat-rpm-config" will solve the problem
# if your OS is Centos, you need to add epel source first by "sudo yum -y install epel-release"
## Tutorial
```
import numpy as np
import pydhs

# the graph is a string array
arr = np.array(pydhs.sample.get_bell2009())
sarr =arr[:,:3].astype('int').astype('str')

# the last 2 columns are minimum and maximum link weights
w_min, w_max = arr[:,-2], arr[:,-1]

# calculate the number of nodes and links
n, m = pydhs.describe(sarr)

# build the graph topology
g = pydhs.make_graph(sarr, n, m)

# call DHS algorithm in Ma et al. 2013
alg = pydhs.Ma2013(g)

# use no node potentials here
h = np.zeros(m)

# search hyperpath from node 1 to 37
alg.run('1','37', w_min, w_max, h)

# hyperpath results in terms of link ID and choice possibility
print '------------------------------------'
print 'eid\tvid pair\tpossibility'
print '------------------------------------'
for i in alg.hyperpath:
    edge = g.get_edge(i[0])
    eid, p = i
    print eid, '\t', edge.get_fv().id,'-->', edge.get_tv().id, '\t', round(p, 2)
print '------------------------------------'
```
