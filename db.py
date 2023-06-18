from sqlalchemy import create_engine, text
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
