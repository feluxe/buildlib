import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from buildlib import kubernetes

n = kubernetes.get_item_names(
    namespace=['mw-prod'],
    kind=['pods', 'replicaSets'],
    label=['app=logcenter'],
    namefilter='.*gui.*'
)

print(n)

n = kubernetes.cmd.get_item_names(
    namespace=['mw-prod'],
    kind=['pods', 'replicaSets'],
    label=['app=logcenter'],
    namefilter='.*gui.*'
)

# print('OUT', n.out)
# print('ERR', n.err)

# kubernetes.logs(
#     name='logcenter-api-5ddd8ff4bc-dk74x', namespace='mw-prod', follow=True
# )
