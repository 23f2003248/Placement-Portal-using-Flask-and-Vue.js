from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Company, Drive, Student
from sqlalchemy import or_
from extensions import cache

admin_b = Blueprint('admin', __name__)

@admin_b.route('/admin/company/approve/<int:id>', methods = ['PUT'])
@jwt_required()
def admin_approve_company(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    curr_company = Company.query.filter_by(company_id = id).first()
    if not curr_company:
        return jsonify ({"error":"company not found."}), 404
    if curr_user.role == 'admin':
        data = request.get_json()
        status = data.get('status')
        if status not in ['approved', 'rejected']:
            return jsonify ({"error":"not valid status."}), 403
        curr_company.approval_status = status
        db.session.commit()
        cache.clear()
        return jsonify({"message":"status updated accordingly."}), 200
    return jsonify({"error":"not authorised!"}), 403

@admin_b.route('/admin/drive/approve/<int:id>', methods = ['PUT'])
@jwt_required()
def admin_approve_drive(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    curr_drive = Drive.query.filter_by(drive_id = id).first()
    if not curr_drive:
        return jsonify ({"error":"drive not found."}), 404
    if curr_user.role == 'admin':
        data = request.get_json()
        status = data.get('status')
        if status not in ['approved', 'rejected']:
            return jsonify ({"error":"not valid status."}), 403
        curr_drive.status = status
        db.session.commit()
        cache.clear()
        return jsonify({"message":"status updated accordingly."}), 200
    return jsonify({"error":"not authorised!"}), 403

@admin_b.route('/admin/student/blacklist/<int:id>', methods = ['PUT'])
@jwt_required()
def admin_blacklist_student(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    curr_std = Student.query.filter_by(student_id = id).first()
    if not curr_std:
        return jsonify ({"error":"student not found."}), 404
    if curr_user.role == 'admin':
        data = request.get_json() or {}
        # Support toggling or setting explicitly
        is_active = data.get('is_active', False)
        curr_std.user.is_active = is_active
        db.session.commit()
        cache.clear()
        action = "activated" if is_active else "blacklisted"
        return jsonify({"message": f"student {action} successfully."}), 200
    return jsonify({"error":"not authorised!"}), 403

@admin_b.route('/admin/company/blacklist/<int:id>', methods = ['PUT'])
@jwt_required()
def admin_blacklist_company(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    curr_company = Company.query.filter_by(company_id = id).first()
    if not curr_company:
        return jsonify ({"error":"company not found."}), 404
    if curr_user.role == 'admin':
        data = request.get_json() or {}
        # Support toggling or setting explicitly
        is_active = data.get('is_active', False)
        curr_company.user.is_active = is_active
        db.session.commit()
        cache.clear()
        action = "activated" if is_active else "blacklisted"
        return jsonify({"message": f"company {action} successfully!"}), 200
    return jsonify({"error":"not authorised!"}), 403

@admin_b.route('/admin/search/', methods = ['GET'])
@jwt_required()
def admin_search():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    if not curr_user:
        return jsonify ({"error":"user not found."}), 404
    if curr_user.role == 'admin':
        q = request.args.get('q')
        if not q:
            return jsonify([]),200
        students = Student.query.join(User).filter(
            or_(
                User.name.ilike(f'%{q}%'),
                User.email.ilike(f'%{q}%'),
                # User.id.like(f'%{q}%'),
                Student.branch.ilike(f'%{q}%'),
                # Student.year.like(f'%{q}%'),
                # Student.cgpa.like(f'%{q}%'),
                # User.is_active.ilike(f'%{q}%'),
                Student.resume.ilike(f'%{q}%'),
            )
        ).all()
        companies = Company.query.join(User).filter(
            or_(
                Company.company_name.ilike(f'%{q}%'),
                User.email.ilike(f'%{q}%'),
                # User.id.like(f'%{q}%'),
                Company.website.ilike(f'%{q}%'),
                Company.company_name.ilike(f'%{q}%'),
                Company.hr_contact.ilike(f'%{q}%'),
                # User.is_active.ilike(f'%{q}%'),
                Company.approval_status.ilike(f'%{q}%'),
                
            )
        ).all()
        res_std = []
        for student in students:
            res_std.append({
                'id': student.student_id,
                'name': student.user.name,
                'email': student.user.email,
                'branch': student.branch,
                'year': student.year,
                'cgpa': student.cgpa,
                'is_active': student.user.is_active,
                'resume': student.resume,
            })
        res_comp = []
        for company in companies:
            res_comp.append({
                'id': company.company_id,
                'name': company.company_name,
                'email': company.user.email,
                'hr_contact': company.hr_contact,
                'website': company.website,
                'approval_status': company.approval_status,
                'is_active': company.user.is_active
            })

        return jsonify({
            'students': res_std,
            'companies': res_comp
            }), 200
    return jsonify({"error":"not authorised!"}), 403
        

