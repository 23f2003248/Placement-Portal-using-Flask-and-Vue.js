from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import Student, User, db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from extensions import cache
import os
from werkzeug.utils import secure_filename

student_b= Blueprint( 'student', __name__)

@student_b.route('/student/register/', methods = ["POST"])
def create_student():
    data = request.get_json()

    if not data.get('name') or not data.get('email') or not data.get('password') or not data.get('branch') or not data.get('cgpa') or not data.get('year'):
        return jsonify ({"error" : "all fields req except resume"}), 400

    existing_mail= User.query.filter_by(email=data['email']).first()

    if not existing_mail:
        hashed_pass=generate_password_hash(data['password'])
        new_user = User (
            name = data['name'],
            email = data['email'],
            password = hashed_pass,
            role = 'student',
            is_active = True
        )
        db.session.add(new_user)
        db.session.flush()

        new_std = Student (
            student_id = new_user.id,
            branch = data['branch'],
            cgpa = data['cgpa'],
            year = data['year'],
            resume = data.get('resume') # wont crash if none
        )

        db.session.add(new_std)
        db.session.commit()
        return jsonify ({"message":"New student created in user", "student_id": new_user.id}), 201
    return jsonify ({"error" : "email already exists"}), 400

@student_b.route('/student/all/', methods = ['GET'])
@cache.cached(timeout=300)
def fetch_all_student():
    students = Student.query.all()
    res = []
    for student in students:
        res.append({
            "id" : student.user.id,
            "name" : student.user.name,
            "email" : student.user.email,
            "branch" : student.branch,
            "year" : student.year,
            "cgpa" : student.cgpa,
            "is_active" : student.user.is_active
        })
    return jsonify(res)
        
@student_b.route('/student/<int:id>', methods = ['GET'])    
def student_by_id(id):
    student = Student.query.filter_by(student_id = id).first()
    if not student:
        return jsonify({"error":"no student found"}), 404
    return jsonify({
        "student_id": student.user.id,
        "name" : student.user.name,
        "email" : student.user.email,
        "branch" : student.branch,
        "year" : student.year,
        "cgpa" : student.cgpa,
        "is_active" : student.user.is_active,
        "resume": student.resume
    })

@student_b.route('/student/update/<int:id>', methods=['PUT'])
@jwt_required()
def student_update(id):
    current_user_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = current_user_email).first()
    if (curr_user.role == 'student' and curr_user.id == id) or  curr_user.role =='admin':

        student = Student.query.filter_by(student_id=id).first()

        if not student:
            return jsonify({"error":"no student found"}), 404
        
        data = request.get_json()

        if data.get('name'):
            student.user.name = data.get('name')

        if data.get('email') and data.get('email') != student.user.email:
            existing = User.query.filter_by(email = data.get('email')).first()
            if existing:
                return jsonify ({"error" : "email already exists"}), 400
            student.user.email = data.get('email')

        if data.get('cgpa'):
            student.cgpa = data.get('cgpa')

        if data.get('branch'):
            student.branch = data.get('branch')

        if data.get('year'):
            student.year = data.get('year')

        if data.get('resume'):
            student.resume = data.get('resume')

        db.session.commit()    
        cache.clear()
        return jsonify({"message":"Student updated successfully."}), 200
    return jsonify({"error":"You are not authorised."}),403
    
@student_b.route('/student/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def student_del(id):
    current_user_email = get_jwt_identity()
    curr_user_ = User.query.filter_by(email = current_user_email).first()
    if not curr_user_.role == 'admin':
        return jsonify({"error":"Admin access required."}),403
    student = Student.query.filter_by(student_id = id).first()
    user = User.query.filter_by(id = id).first()
    if not student:
        return jsonify({"error":"no student found"}), 404
    db.session.delete(student)
    db.session.delete(user)
    db.session.commit()
    cache.clear()
    return jsonify({"message":"Student deleted successfully."}), 200

@student_b.route('/student/upload_resume', methods=['POST'])
@jwt_required()
def upload_resume():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    if not curr_user or curr_user.role != 'student':
        return jsonify({"error": "not authorised"}), 403
    
    student = Student.query.filter_by(student_id = curr_user.id).first()
    if not student:
        return jsonify({"error": "student profile not found."}), 404

    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(f"resume_{student.student_id}_{file.filename}")
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        resumes_dir = os.path.join(static_dir, 'resumes')
        os.makedirs(resumes_dir, exist_ok=True)
        
        filepath = os.path.join(resumes_dir, filename)
        file.save(filepath)
        
        student.resume = f"/static/resumes/{filename}"
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Resume uploaded successfully", "resume_url": student.resume}), 200
    return jsonify({"error": "File upload failed"}), 400
    

    




