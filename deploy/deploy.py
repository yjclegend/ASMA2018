import time
import boto3
from botocore.exceptions import ClientError


from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

class Deployer(object):
	"""docstring for deployer"""
	def __init__(self, ):
		super(Deployer, self).__init__()
		self.initConnection()
		self.instances = list()
		self.volumes = list()
		self.summaryCurrentStatus()

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

	def summaryCurrentStatus(self):
		self.updateInstanceInfo()
		self.updateVolumeInfo()
		self.updateHostIni()

	def updateHostIni(self):
		#host_file = open('hosts.ini','w')
		pass

	def updateVolumeInfo(self):
		response = self.client.describe_volumes()
		volumes = response['Volumes']
		for vol in volumes:
			vol_info = dict()
			vol_info['vol_id'] = vol['VolumeId']
			vol_info['att'] = vol['Attachments']
			self.volumes.append(vol_info)
		print(self.volumes)

	def updateInstanceInfo(self):
		response = self.client.describe_instances()
		#print(res)
		reservations = response['Reservations']
		for reservation in reservations:
			for instance in reservation['Instances']:
				inst_info = dict()
				inst_info["id"] = instance['InstanceId']
				inst_info['ip'] = instance['PrivateIpAddress']
				self.instances.append(inst_info)
		print(self.instances)

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
				inst_info = dict()
				inst_info['id'] = instance.id
				#inst_info['ip'] = instance.ip
				self.instances.append(inst_info)
		except ClientError as e:
			print(e)

	def createVolume(self):
		volume = self.ec2.create_volume(
			AvailabilityZone='melbourne-qh2',
			Size=50,
			)
		print(volume)

	def attachVolume(self, vol_id, in_id):
		print(vol_id,in_id)
		instance = self.ec2.Instance(in_id)
		while instance.state['Name'] != 'running':
			print('Instance {} is {}'.format(instance.id,instance.state))
			time.sleep(5)
			instance.update()

		response = self.client.attach_volume(
			Device='/dev/vdc',
			InstanceId=in_id,
			VolumeId=	vol_id
			)
		print(response)

	def deployMaster(self):
		self.master_id = self.instances[0]['id']
		self.master_vol_id = self.volumes[0]['vol_id']
		#self.createVolume()
		self.attachVolume(self.master_vol_id, self.master_id)

	def terminateAll(self):
		ids = list()
		for instance in self.instances:
			ids.append(instance['id'])
		self.terminateInstance(ids)
		self.instances = list()

	def terminateInstance(self, ids):
		self.client.terminate_instances(InstanceIds=ids)


	def playbook(self):
		Options = namedtuple('Options',[
										'connection',
										'remote_user',
										'forks',
										'become',
										'become_user',
										'become_method', 
										'private_key_file',
										'listhosts',
										'listtasks',
										'listtags',
										'syntax',
										'check',
										'diff',
										'module_path'])
		loader = DataLoader()
		options = Options(
						connection='ssh',
						remote_user='ubuntu',
						forks=100,
						become=True,
						become_method='sudo',
						become_user='root', 
						private_key_file='huozhua.key',
						listhosts=False,
						listtasks=False,
						listtags=False,
						syntax=False,
						check=False,
						diff=False,
						module_path='')
		
		inventory = InventoryManager(loader=loader, sources='hosts.ini')
		variable_manager = VariableManager(loader=loader, inventory=inventory)

		playbook_path = 'apache.yaml'


		pbex = PlaybookExecutor(playbooks=[playbook_path],
								inventory=inventory,
								variable_manager=variable_manager,
								loader=loader,
								options=options,
								passwords=dict())
		result = pbex.run()

if __name__ == '__main__':
	de = Deployer()
	#de.deployMaster()
	#de.terminateAll()
	#de.addInstance()		
	de.playbook()
