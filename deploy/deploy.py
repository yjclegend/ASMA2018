import os
import time
import boto3
from botocore.exceptions import ClientError


from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
import credential_demo as credential

class Deployer(object):
	"""docstring for deployer"""
	def __init__(self, ):
		super(Deployer, self).__init__()
		self.instances = list()
		self.volumes = list()			#volumes 
		self.myKey = credential.key
		self.mySecret = credential.secret
		self.instSize = credential.size
		self.privateKey = credential.privateKey
		self.endpoint_url = 'https://nova.rc.nectar.org.au:8773/services/Cloud'
		self.initConnection()


	def initConnection(self):
		try:
			self.client = boto3.client(service_name='ec2',
                    region_name='melbourne-qh2',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.myKey,
                    aws_secret_access_key=self.mySecret)
			self.ec2 = boto3.resource(service_name='ec2',
                    region_name='melbourne-qh2',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.myKey,
                    aws_secret_access_key=self.mySecret)
		except Exception as e:
			print(e.message)
			exit()
	def summaryCurrentStatus(self):
		try:
			self.updateInstanceInfo()
			self.updateVolumeInfo()
		except Exception as e:
			print(e.message)
			exit()
	def updateHostIni(self):
		host_file = open('hosts.ini','w')
		host_file.write("[slave:vars]\n")
		host_file.write("ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n")
		host_file.write("[master]\n")
		#write master ip
		host_file.write(self.instances[0]['ip'])
		host_file.write('\n')

		#write slave ip
		host_file.write("[slave]\n")
		for i in range(1,len(self.instances)):
			host_file.write(self.instances[i]['ip'])
			host_file.write('\n')
		host_file.close()


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

	#add instances all at once, 
	def addInstance(self):
		try:
			print("spawning instances")
			instances = self.ec2.create_instances(
						ImageId='ami-00003837',
	                    KeyName='jiachuany',
	                    MaxCount=4,
	                    MinCount=1,
	                    Placement={'AvailabilityZone': 'melbourne-qh2'},
	                    SecurityGroups=['default','SSH'],
	                    InstanceType=self.instSize
	                    )
			for instance in instances:
				print('New instance {} has been created'.format(instance.id))
				inst_info = dict()
				in_id = instance.id
				while True:
					if instance.state['Name'] == 'running' and len(instance.private_ip_address) > 0:
						inst_info['id'] = instance.id
						inst_info['ip'] = instance.private_ip_address
						break
					print("instances initializing")
					time.sleep(5)
					instance = self.ec2.Instance(in_id)
				self.instances.append(inst_info)
			self.updateHostIni()
		except ClientError as e:
			print(e)

	def addVolume(self):
		print("creating volumes")
		for instance in self.instances:
			in_id = instance['id']
			try:
				volume = self.createVolume()
				print("attach volume " + volume.id + " to " + in_id)
				self.attachVolume(volume.id, in_id)
			except Exception as e:
				print(e.message)
	def createVolume(self):
		volume = self.ec2.create_volume(
			AvailabilityZone='melbourne-qh2',
			Size=50,
			)
		return volume

	def attachVolume(self, vol_id, in_id):
		print(vol_id,in_id)
		instance = self.ec2.Instance(in_id)
		while True:
			try:
				response = self.client.attach_volume(
					Device='/dev/vdc',
					InstanceId=in_id,
					VolumeId=vol_id
					)
				print(response)
				break
			except Exception as e:
				print(e)
				time.sleep(3)

	def terminateAll(self):
		ids = list()
		for instance in self.instances:
			ids.append(instance['id'])
		self.terminateInstance(ids)
		time.sleep(10)
		self.instances = list()
		for vol in self.volumes:
			self.client.delete_volume(VolumeId=vol["vol_id"])

	def terminateInstance(self, ids):
		if len(ids) > 0:
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
						private_key_file=self.privateKey,
						listhosts=False,
						listtasks=False,
						listtags=False,
						syntax=False,
						check=False,
						diff=False,
						module_path='')
		
		inventory = InventoryManager(loader=loader, sources='hosts.ini',)
		variable_manager = VariableManager(loader=loader, inventory=inventory)

		playbook_path = 'config.yaml'


		pbex = PlaybookExecutor(playbooks=[playbook_path],
								inventory=inventory,
								variable_manager=variable_manager,
								loader=loader,
								options=options,
								passwords=dict())
		result = pbex.run()
		print(result)

if __name__ == '__main__':
	de = Deployer()
	de.summaryCurrentStatus()
	# remove all instances and volumes
	de.terminateAll()
	# add new instances and attach volumes
	de.addInstance()
	de.addVolume()
	time.sleep(30)
	de.playbook()
