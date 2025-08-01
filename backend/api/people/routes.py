from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from .models import Worker, Job, Crew
from api.middleware import jwt_required_middleware

people_bp = Blueprint('people', __name__, url_prefix='/api/people')

@people_bp.route('/workers', methods=['GET'])
@jwt_required_middleware()
def get_workers():
    workers = Worker.query.all()
    return jsonify([{
        'id': worker.id,
        'name': worker.name,
        'jobs': [job.title for job in worker.jobs]
    } for worker in workers]), HTTPStatus.OK

@people_bp.route('/crew/<int:title_id>', methods=['GET'])
@jwt_required_middleware()
def get_crew_for_title(title_id):
    crew_members = Crew.query.filter_by(titleID=title_id).all()
    return jsonify([{
        'id': crew.id,
        'worker_id': crew.job.worker.id,
        'worker': crew.job.worker.name,
        'job_id': crew.job.id,
        'job': crew.job.title
    } for crew in crew_members]), HTTPStatus.OK

@people_bp.route('/worker/<int:worker_id>/titles', methods=['GET'])
@jwt_required_middleware()
def get_titles_for_worker(worker_id):
    # Fetch all jobs for the worker
    jobs = Job.query.filter_by(workerID=worker_id).all()
    if not jobs:
        return jsonify({'error': 'Worker not found or has no jobs'}), HTTPStatus.NOT_FOUND

    results = []
    for job in jobs:
        # For each job, find all crew entries (i.e., all titles where they worked)
        for crew in job.crew:
            if crew.title:
                results.append({
                    'title_id': crew.title.id,
                    'title': crew.title.title,
                    'job': job.title
                })

    return jsonify(results), HTTPStatus.OK

@people_bp.route('/job/<string:job_title>/workers', methods=['GET'])
@jwt_required_middleware()
def get_workers_for_job(job_title):
    jobs = Job.query.filter_by(title=job_title).all()
    if not jobs:
        return jsonify({'error': 'No such job'}), HTTPStatus.NOT_FOUND

    results = []
    for job in jobs:
        if job.worker:
            results.append({
                'worker_id': job.worker.id,
                'worker_name': job.worker.name,
                'job_id': job.id,
                'job_title': job.title
            })
    return jsonify(results), HTTPStatus.OK

@people_bp.route('/jobid/<int:job_id>/workers', methods=['GET'])
@jwt_required_middleware()
def get_workers_for_jobid(job_id):
    job = Job.query.get(job_id)
    if not job or not job.worker:
        return jsonify({'error': 'No such job or worker'}), HTTPStatus.NOT_FOUND
    return jsonify({
        'worker_id': job.worker.id,
        'worker_name': job.worker.name,
        'job_id': job.id,
        'job_title': job.title
    }), HTTPStatus.OK

@people_bp.route('/workers/search', methods=['GET'])
@jwt_required_middleware()
def search_workers():
    # Get search term from query string: /api/people/workers/search?query=some_name
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Missing search query'}), HTTPStatus.BAD_REQUEST

    workers = Worker.query.filter(Worker.name.ilike(f'%{query}%')).all()

    results = [{
        'id': worker.id,
        'name': worker.name,
        'jobs': [job.title for job in worker.jobs]
    } for worker in workers]
    return jsonify(results), HTTPStatus.OK

