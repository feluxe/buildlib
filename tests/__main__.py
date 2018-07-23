"""
"""

import sys
import os
import tests.npm as npm

npm.test_bump_version()
npm.test_bump_version(as_cmd=True)

print('\nTests Finished')

from buildlib import digitalocean
from pprint import pprint

lala = '8b92e8c4055ddf682f934b62b597ef5bbf9bb3f5f1355a0d6d706a7073534e89'
# lala = ''
r = digitalocean.cmd.set_access_token_envvar(lala)

# snaps = digitalocean.get_volume_snapshots(volume_id=None, name_contains=None)
# for snap in snaps:
#     pprint(snap['name'])
#     pprint(snap['id'])
#     pprint(snap['min_disk_size'])

# r = digitalocean.create_volume(
#     name='example3',
#     description='Test',
#     snapshot_id='5155aaf1-33bd-11e8-9b2b-0242ac116704'
# )
# pprint(r)

# vols = digitalocean.get_volumes(name_contains='example')
# pprint(vols)

# digitalocean.delete_volume(volume_id=vols[0]['id'])

# r = digitalocean.create_volume_snapshot(name='test_snap21', volume_id=vols[0]['id'])
# print(r)

# snaps = digitalocean.get_volume_snapshots(
#     # volume_id=vols[0]['id'], name_contains=['test_snap']
#     volume_id=None,
#     name_contains=['test_snap']
# )
# pprint(snaps)

# for snap in snaps:
#     digitalocean.delete_snapshot(snapshot_id=snap['id'])

# digitalocean.delete_snapshot(snapshot_id=snaps[0]['id'])
# digitalocean.delete_snapshot(snapshot_id=snaps[1]['id'])
# digitalocean.delete_snapshot(snapshot_id=snaps[2]['id'])
