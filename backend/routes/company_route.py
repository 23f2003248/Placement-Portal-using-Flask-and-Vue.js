from flask import Blueprint, request, jsonify
from models import User, Company, db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from extensions import cache

company_b= Blueprint('company', __name__)

@company_b.route('/company/register/', methods = ['POST'])
def company_register():
    data = request.get_json()

    if not data.get('name') or not  data.get('email') or not data.get('password') or not data.get('hr_contact') or not data.get('website'):
        return jsonify({"error":"all fields are required."}), 400

    existing = User.query.filter_by(email=data.get('email')).first()
    if existing:
        return jsonify({"error":"email already registered."}), 400
    
    existing_website = Company.query.filter_by(website=data.get('website')).first()
    if existing_website:
        return jsonify({"error":"website already registered."}), 400
    
    new_user = User(
        name = data['name'],
        email = data['email'],
        password = generate_password_hash(data['password']),
        role = 'company',
        is_active= True
    )
    db.session.add(new_user)
    db.session.flush()

    new_company = Company(
        company_id = new_user.id,
        company_name = new_user.name,
        hr_contact = data['hr_contact'],
        website = data['website'],
        approval_status = 'pending'
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({"message": "new company registered successfully!"}), 202

@company_b.route('/company/all/', methods = ['GET'])
@cache.cached(timeout=300)
def fetch_company_all():
    companies = Company.query.all()
    res= []
    for company in companies:
        res.append({
            "id": company.user.id,
            "name": company.user.name,
            "email": company.user.email,
            "is_active": company.user.is_active,
            "hr_contact":company.hr_contact,
            "website":company.website,
            "approval_status": company.approval_status
        })
    return jsonify(res)

@company_b.route('/company/<int:id>/', methods = ['GET'])

def fetch_company_id(id):
    company = Company.query.filter_by(company_id = id).first()
    if not company:
        return jsonify({"error":"no company found"}),400

    return jsonify({
        "id": company.user.id,
        "name": company.user.name,
        "email": company.user.email,
        "is_active": company.user.is_active,
        "hr_contact":company.hr_contact,
        "website":company.website,
        "approval_status":company.approval_status
    })

@company_b.route('/company/update/<int:id>', methods = ['PUT'])
@jwt_required()
def company_update(id):
    current_user_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = current_user_email).first()
    if (curr_user.role == 'company' and curr_user.id == id) or curr_user.role == 'admin':
        data = request.get_json()
        company = Company.query.filter_by(company_id = id).first()
        if not company:
            return jsonify({"error":"no company found"}),400

        if data.get('name'):
            company.user.name=data.get('name')

        if data.get('email'):
            existing = User.query.filter_by(email=data.get('email')).first()
            if existing:
                return jsonify({"error":"email already exists."}),400
            company.user.email =data.get('email')


        if data.get('hr_contact'):
            company.hr_contact=data.get('hr_contact')

        if data.get('website'):
            existing = Company.query.filter_by(website=data.get('website')).first()
            if existing:
                return jsonify({"error":"website already exists."}),400
            company.website=data.get('website')


        if data.get('password'):
            company.user.password=generate_password_hash(data.get('password'))

        db.session.commit()
        cache.clear()
        return jsonify({"message":"company updated successfully."}),202
    return jsonify({"error":"You are not authorised."}),403
 
@company_b.route('/company/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def company_delete(id):
    current_user_email = get_jwt_identity()
    curr_user_ = User.query.filter_by(email = current_user_email).first()
    if curr_user_.role == 'admin':
        company = Company.query.filter_by(company_id = id).first()
        user = User.query.filter_by(id = id).first()
        if not company:
            return jsonify({"error":"no company found"}),400
        db.session.delete(company)
        db.session.delete(user)
        db.session.commit()
        cache.clear()
        return jsonify({"message":"company deleted successfully."}),202
    return jsonify({"error":"Admin access required."}),403




