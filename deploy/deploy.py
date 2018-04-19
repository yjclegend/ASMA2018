import boto
from boto.ec2.regioninfo import RegionInfo


region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(aws_access_key_id='d76c0dd861f346b0acb093220c421eb4',
							aws_secret_access_key='d4acf02f362341b2ad66a7fdc43c14c6',
							is_secure=True,
							region=region,
							port=8773,
							path='/services/Cloud',
							validate_certs=False)

#images = ec2_conn.get_all_images()
#for img in images:
#	print('Image id:{}, image name:{}'.format(img.id, img.name))

reservation = ec2_conn.run_instances('ami-00003837',
									key_name='jiachuany',
									instance_type='m1.small',
									security_groups=['default'])
instance = reservation.instances[0]
print('New instance {} has been created'.format(instance.id))
