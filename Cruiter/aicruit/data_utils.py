import json

def load_jobs():
    # read all the jobs from database
	with open(r'aicruit/data/jobs.json') as jobs_file:
		jobs = json.load(jobs_file)
		return jobs

def load_applications():
    # read all applications from database
	with open(r'aicruit/data/applications.json') as applications_file:
		applications = json.load(applications_file)
		return applications

def add_job(job_details):
    # add new job
	new_job = {}
	try:
		data = load_jobs()
	except:
		data = []

	new_job['id'] = str(10000 + len(data) + 1)
	new_job['id'] = 'J' + new_job['id'][1:]
	new_job['details'] = job_details

	data.append(new_job)
	with open(r'aicruit/data/jobs.json', 'w') as jobs: 
		json.dump(data, jobs)

def add_application(application_details):
    # add new application
	new_application = {}
	try:
		data = load_applications()
	except:
		data = []

	new_application["id"] = str(10000 + len(data) + 1)
	new_application['id'] = 'C' + new_application['id'][1:]
	new_application['details'] = application_details

	data.append(new_application)
	with open(r'aicruit/data/applications.json', 'w') as applications: 
		json.dump(data, applications)

def read_job_questions():
    # returns all questions for a recruiter
	with open(r'aicruit/data/post_bot_messages.json') as messages_json:
		messages = json.load(messages_json)
		return messages

def read_apply_questions():
    # returns all questions for the applicant
	with open(r'aicruit/data/apply_bot_messages.json') as messages_json:
		messages = json.load(messages_json)
		return messages

class ApplyQuestion():
	def __init__(self):
		self.index = 0
		self.questions = read_apply_questions()
		self.total_questions = len(self.questions)
		self.keys = list(self.questions.keys())
		self.messages = list(self.questions.values())

	def get_message(self):
		key = self.keys[self.index]
		message = self.messages[self.index]
		self.index = (self.index + 1) % self.total_questions
		return key, message

	def reset_index(self):
		self.index = 0

class JobQuestion():
	def __init__(self):
		self.index = 0
		self.questions = read_job_questions()
		self.total_questions = len(self.questions)
		self.keys = list(self.questions.keys())
		self.messages = list(self.questions.values())

	def get_message(self):
		key = self.keys[self.index]
		message = self.messages[self.index]
		self.index = (self.index + 1) % self.total_questions
		return key, message

	def reset_index(self):
		self.index = 0
