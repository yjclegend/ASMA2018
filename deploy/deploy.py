import boto3
from botocore.exceptions import ClientError
class Deployer(object):
	"""docstring for deployer"""
	def __init__(self, ):
		super(Deployer, self).__init__()
		self.initConnection()

	def initConnection(self):
		self.client = boto3.client(service_name='ec2',
                    region_name='melbourne-qh2',
                    endpoint_url='https://nova.rc.nectar.org.au:8773/services/Cloud',
                    aws_access_key_id='d76c0dd861f346b0acb093220c421eb4',
                    aws_secret_access_key='d4acf02f362341b2ad66a7fdc43c14c6')
		self.ec2 = boto3.resource(service_name='ec2',
                    region_name='melbourne-qh2',
                    endpoint_url='https://nova.rc.nectar.org.au:8773/services/Cloud',
                    aws_access_key_id='d76c0dd861f346b0acb093220c421eb4',
                    aws_secret_access_key='d4acf02f362341b2ad66a7fdc43c14c6')

	def addInstance(self):
		try:
			instances = self.ec2.create_instances(
						ImageId='ami-00003837',
	                    KeyName='jiachuany',
	                    MaxCount=4,
	                    MinCount=1,
	                    Placement={'AvailabilityZone': 'melbourne-qh2'},
	                    SecurityGroups=['default','SSH'],
	                    InstanceType='m2.medium'
	                    )
			for instance in instances:
				print('New instance {} has been created'.format(instance.id))
		except ClientError as e:
			print(e)
	def showInstances(self):
		response = self.client.describe_instances()
		return response

	def terminateAll(self):
		ids = list()
		res = self.showInstances()
		instances = res['Reservations']
		for instance in instances:
			ids.append(instance['Instances'][0]['InstanceId'])
		self.terminateInstance(ids)

	def terminateInstance(self, ids):
		self.client.terminate_instances(InstanceIds=ids)


	def playbook():
		pass

if __name__ == '__main__':
	de = Deployer()
	#de.terminateAll()
	#de.addInstance()		
	#de.showInstances()
	#de.terminateInstance(['i-3e87513d'])
