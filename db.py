from sqlalchemy import create_engine, text, bindparam
import os

db_conn_string = os.environ['DB_CONNECTION_STR']
engine = create_engine(db_conn_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs():
  with engine.connect() as conn:
    result = conn.execute(text('select * from jobs'))
    jobs = []
    for row in result.all():
      jobs.append(row)
    return jobs


def load_job_page(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
                          {"val": id})
    row = result.fetchone()
    if row is None:
      return None
    else:
      columns = result.keys()
      values = [row[i] for i in range(len(columns))]
      return dict(zip(columns, values))


def apply_job(job_id, data):
  with engine.connect() as conn:
    query = text("""
            INSERT INTO applications
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url, application_status, create_at, update_at)
            VALUES
            (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url, 'PENDING', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """)
    parameters = {
      "job_id": job_id,
      "full_name": data["full-name"],
      "email": data["email"],
      "linkedin_url": data["linkedin"],
      "education": data["education"],
      "work_experience": data["work-experience"],
      "resume_url": data["resume"]
    }
    conn.execute(query, parameters)
