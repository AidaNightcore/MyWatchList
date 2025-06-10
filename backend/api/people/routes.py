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
        'worker': crew.job.worker.name,
        'job': crew.job.title
    } for crew in crew_members]), HTTPStatus.OK