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

	def updateInstanceInfo(self):
		res = self.client.describe_instances()
		print(res)
		instances = res['Reservations']
		for inst_info in instances:
			core_info = instance['Instances'][0]
			instance = dict()
			instance["id"] = core_info['InstanceId']
			instance['ip'] = core_info['']

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

	def terminateAll(self):
		ids = list()
		res = self.showInstances()
		inst_data = res['Reservations']
		for instance in instances:
			ids.append(instance['Instances'][0]['InstanceId'])
		self.terminateInstance(ids)

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
	de.updateInstanceInfo()
	#de.terminateAll()
	#de.addInstance()		
	#de.playbook()
