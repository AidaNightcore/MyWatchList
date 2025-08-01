import pandas as pd
import requests

# Colectează toate fișierele sursă pentru a extrage nume unice de worker + job
CSV_FILES = ["data.csv", "books.csv", "TMDB_all_movies(2).csv", "TMDB_tv_dataset_v3.csv"]
API_WORKER = "http://localhost:5000/api/people/workers"
API_JOB = "http://localhost:5000/api/people/jobs"
API_CREATE_WORKER = "http://localhost:5000/api/people/worker"  # Asigură-te că ai această rută POST!
API_CREATE_JOB = "http://localhost:5000/api/people/job"        # Asigură-te că ai această rută POST!
TOKEN = "Bearer <TOKEN>"  # Înlocuiește cu token valid

all_workers = set()
all_jobs = set()
worker_job_pairs = set()

crew_roles = ["author", "director", "writer", "screenplay", "actor", "producer", "editor", "cinematographer", "composer", "creator", "showrunner"]
for csv_file in CSV_FILES:
    try:
        df = pd.read_csv(csv_file)
    except Exception:
        continue
    for col in df.columns:
        role = None
        for cr in crew_roles:
            if cr in col.lower():
                role = col
        if role:
            for val in df[col].dropna():
                for name in str(val).replace(";", ",").split(","):
                    name = name.strip()
                    if name:
                        all_workers.add(name)
                        all_jobs.add(role)
                        worker_job_pairs.add((name, role))
        if "author" in col.lower():
            for val in df[col].dropna():
                for name in str(val).replace(";", ",").split(","):
                    name = name.strip()
                    if name:
                        all_workers.add(name)
                        all_jobs.add("Author")
                        worker_job_pairs.add((name, "Author"))

# Creează workerii
worker_to_id = {}
for name in all_workers:
    resp = requests.post(API_CREATE_WORKER, json={"name": name}, headers={"Authorization": TOKEN})
    if resp.status_code in (200, 201):
        data = resp.json()
        worker_to_id[name] = data.get("id")
        print(f"Worker: {name} (created id={data.get('id')})")
    elif resp.status_code == 409:  # Already exists
        # Fă lookup
        resp2 = requests.get(API_WORKER + f"/search?query={name}", headers={"Authorization": TOKEN})
        if resp2.status_code == 200 and resp2.json():
            worker_to_id[name] = resp2.json()[0].get("id")
    else:
        print(f"Worker {name}: {resp.text}")

# Creează job-urile asociate workerilor
for name, job in worker_job_pairs:
    worker_id = worker_to_id.get(name)
    if worker_id:
        resp = requests.post(API_CREATE_JOB, json={"title": job, "worker_id": worker_id}, headers={"Authorization": TOKEN})
        if resp.status_code in (200, 201):
            print(f"Job: {job} for {name} (worker_id={worker_id})")
        elif resp.status_code == 409:
            print(f"Job: {job} for {name} already exists.")
        else:
            print(f"Job: {job} for {name}: {resp.text}")

print("Populare worker/job completă.")
