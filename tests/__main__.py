import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'buildlib')))
from buildlib import kubernetes

n = kubernetes.get_item_names(
    namespace=['mw-prod'], kind=['pods', 'replicaSets'], label=['app=logcenter'], namefilter='.*gui.*')

print(n)
