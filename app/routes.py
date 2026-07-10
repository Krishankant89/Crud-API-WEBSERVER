from flask import Blueprint, jsonify, request

from app import db
from app.models import Student
from app.logger import logger

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1"
)

def _get_payload():
    json_data = request.get_json(silent=True)
    if isinstance(json_data, dict):
        return json_data

    if request.form:
        return request.form.to_dict()

    return None


# HEALTHCHECK
@api_bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "healthy"
    }), 200


# CREATE
@api_bp.route("/students", methods=["POST"])
def create_student():
    data = _get_payload()

    if not data:
        return jsonify({
            "error": "Request body required"
        }), 400

    required_fields = ["name", "email", "age"]
    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({
                "error": f"{field} is required"
            }), 400

    try:
        age = int(data["age"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "age must be a valid integer"
        }), 400

    # Modern 2.0 query style for checking duplicates
    existing_student = db.session.execute(
        db.select(Student).filter_by(email=data["email"])
    ).scalar_one_or_none()

    if existing_student:
        return jsonify({
            "error": "email already exists"
        }), 409

    student = Student(
        name=data["name"],
        email=data["email"],
        age=age
    )

    db.session.add(student)
    db.session.commit()

    logger.info(f"Student created {student.id}")

    return jsonify(student.to_dict()), 201


# GET ALL
@api_bp.route("/students", methods=["GET"])
def get_students():
    students = db.session.execute(db.select(Student)).scalars().all()
    return jsonify(
        [student.to_dict() for student in students]
    ), 200


# GET BY ID
@api_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify(student.to_dict()), 200


# UPDATE
@api_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    data = _get_payload()
    if not data:
        return jsonify({
            "error": "Request body required"
        }), 400

    # If email is changing, ensure it's not taken by someone else
    new_email = data.get("email")
    if new_email and new_email != student.email:
        existing_student = db.session.execute(
            db.select(Student).filter_by(email=new_email)
        ).scalar_one_or_none()
        
        if existing_student:
            return jsonify({
                "error": "email already exists"
            }), 409
        student.email = new_email

    if "name" in data and str(data["name"]).strip() == "":
        return jsonify({
            "error": "name cannot be empty"
        }), 400

    student.name = data.get("name", student.name)

    if "age" in data:
        try:
            student.age = int(data["age"])
        except (TypeError, ValueError):
            return jsonify({
                "error": "age must be a valid integer"
            }), 400

    db.session.commit()
    return jsonify(student.to_dict()), 200


# DELETE
@api_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Student deleted successfully"
    }), 200