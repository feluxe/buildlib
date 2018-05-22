import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from buildlib import docker

# n = kubernetes.get_item_names(
#     namespace=['mw-prod'],
#     kind=['pods', 'replicaSets'],
#     label=['app=logcenter'],
#     namefilter='.*gui.*'
# )

# print(n)

# n = kubernetes.get_item_names(
#     namespace=['meyerwolters'],
#     kind=['pods'],
#     label=['app=logcenter'],
#     namefilter='.*gui.*',
#     # statusfilter=['Running'],
#     maxage=20,
# )

# print(n)

# print('OUT', n.out)
# print('ERR', n.err)

# kubernetes.logs(
#     name='logcenter-api-5ddd8ff4bc-dk74x', namespace='mw-prod', follow=True
# )

r = docker.cmd.ps(all_=False, filter='lala')

print(r.val)
