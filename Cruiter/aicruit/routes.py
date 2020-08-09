from aicruit import app
from flask import render_template, request
import json
from aicruit.data_utils import *

apply_bot_messages = ApplyQuestion()
application_details = {}
apply_bot_key = ""

post_bot_messages = JobQuestion()
job = {}
job_bot_key = ""

@app.route("/")
@app.route("/home")
def home():
	#home page
	return render_template("home.html")

@app.route("/applicant")
def applicant():
	#applicant's dashboard - displays all available jobs he / she can apply
	try:
		jobs = load_jobs()
	except:
		jobs = []
	return render_template("applicant.html", jobs=jobs)

@app.route("/job/<string:id>")
def job(id):
	#displays details of a single job & the applicant cant apply to it
	jobs = load_jobs()
	selected = [j for j in jobs if j['id'] == id][0]
	return render_template("job.html", selected=selected)

@app.route("/job/<string:id>/apply", methods=['GET', 'POST'])
def apply(id):
	#chatbot - fetches answers from the applicant & apply for the job
	global application_details, apply_bot_key

	if request.method=='GET':
		application_details = {"jobid" : id}
		apply_bot_key = ""
		apply_bot_messages.reset_index()
		apply_bot_key, bot_message = apply_bot_messages.get_message()

		return render_template("apply_for_job.html", message=bot_message, id=id)

	if apply_bot_key=="End":
		return "Please return to the home page"

	if request.method=='POST':
		data = json.loads(request.data)
		user_message = data['user_message']
		application_details[apply_bot_key] = user_message
		apply_bot_key, bot_message = apply_bot_messages.get_message()

		if apply_bot_key=="End":
			add_application(application_details)
		
		return bot_message

@app.route("/recruiter")
def recruiter():
	#recruiter's dashboard - displays all jobs he posted
	try:
		jobs = load_jobs()
	except:
		jobs = []
	return render_template("recruiter.html", jobs=jobs)

@app.route("/applications/<string:id>")
def application(id):
	#displays all candidates who applied for a particular job
	try:
		applications = load_applications()
	except:
		applications = []
	selected = [j for j in applications if j['details']['jobid'] == id]
	return render_template("application.html", selected=selected)

@app.route("/candidate/<string:id>")
def candidate(id):
	#displays details for a particular candidate
	applications = load_applications()
	selected = [c for c in applications if c['id'] == id][0]
	return render_template("candidate_details.html", selected=selected)

@app.route("/post", methods=['GET', 'POST'])
def post():
	#chatbot - fetches job details from recruiter & posts new job
	global job, job_bot_key

	if request.method=='GET':
		job = {}
		job_bot_key = ""
		post_bot_messages.reset_index()
		job_bot_key, bot_message = post_bot_messages.get_message()

		return render_template("post_job.html", message=bot_message)

	if job_bot_key=="End":
		return "Please return to the home page"

	if request.method=='POST':
		data = json.loads(request.data)
		user_message = data['user_message']
		job[job_bot_key] = user_message
		job_bot_key, bot_message = post_bot_messages.get_message()

		if job_bot_key=="End":
			add_job(job)
		
		return bot_message
