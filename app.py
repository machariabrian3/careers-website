from flask import Flask, render_template, jsonify, request
from db import load_jobs, load_job_page, apply_job

app = Flask(__name__)

JOBS_static = [{
  "id": 1,
  "title": "Software Engineer",
  "location": "San Francisco",
  "salary": "$100,000 - $120,000"
}, {
  "id": 2,
  "title": "Data Analyst",
  "location": "New York City",
  "salary": "$80,000 - $90,000"
}, {
  "id": 3,
  "title": "Marketing Manager",
  "location": "Chicago",
  "salary": "$90,000 - $110,000"
}, {
  "id": 4,
  "title": "Graphic Designer",
  "location": "Los Angeles",
  "salary": "$70,000 - $80,000"
}, {
  "id": 5,
  "title": "Project Manager",
  "location": "Seattle",
  "salary": "$95,000 - $105,000"
}, {
  "id": 6,
  "title": "Sales Representative",
  "location": "Boston",
  "salary": "$60,000 - $70,000"
}, {
  "id": 7,
  "title": "Product Manager",
  "location": "Austin",
  "salary": "$110,000 - $130,000"
}, {
  "id": 8,
  "title": "Human Resources Specialist",
  "location": "Washington, D.C.",
  "salary": "$75,000 - $85,000"
}, {
  "id": 9,
  "title": "Financial Analyst",
  "location": "San Diego",
  "salary": "$85,000 - $95,000"
}, {
  "id": 10,
  "title": "Customer Service Representative",
  "location": "Miami"
}]


@app.route("/")
def index():
  jobs = load_jobs()
  return render_template('home.html', jobs=jobs)


@app.route("/apiv1/jobs")
def job_list():
  jobs = load_jobs()
  return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id):
  job = load_job_page(id)
  if not job:
    return "Not found", 404
  return render_template('widgets/jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_job_func(id):
  data = request.form
  job = load_job_page(id)
  apply_job(id, data)
  return render_template('widgets/application_submitted.html',
                         application=data,
                         job=job)


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
