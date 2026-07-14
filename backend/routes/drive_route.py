from flask import Blueprint,request, jsonify
from models import Company, Drive, db, User
from flask_jwt_extended import get_jwt_identity, jwt_required
from extensions import cache
from datetime import datetime

drive_b = Blueprint('drive', __name__)    

@drive_b.route('/drive/register/', methods = ['POST'])
@jwt_required()
def drive_register():
    curr_user_mail = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_user_mail).first()
    curr_user_company = Company.query.filter_by(company_id=curr_user.id).first()
    if not curr_user_company:
        return jsonify({"error":"company not found."}),404
    if curr_user.role == 'company' and curr_user_company.approval_status == 'approved':
        data = request.get_json()
        if not data.get('job_title') or not data.get('job_desc') or not data.get('elig_branch') or not data.get('elig_year') or not data.get('elig_min_cgpa') or not data.get('application_deadline'):
           return jsonify({"error":"all fields required"}), 400
        
        # Parse application_deadline string to datetime object
        deadline_str = data.get('application_deadline')
        try:
            if 'T' in deadline_str:
                application_deadline = datetime.fromisoformat(deadline_str.replace('Z', ''))
            else:
                application_deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except Exception:
            return jsonify({"error": "invalid date format"}), 400

        new_drive = Drive(
            company_id = curr_user_company.company_id,
            job_title= data.get('job_title'),
            job_desc= data.get('job_desc'),
            elig_branch= data.get('elig_branch'),
            elig_year= int(data.get('elig_year')),
            elig_cgpa= float(data.get('elig_min_cgpa')),
            application_deadline= application_deadline,
            status= 'pending'
        )
        db.session.add(new_drive)
        db.session.commit()
        cache.clear()
        return jsonify({"message":"drive created successfully."}), 201
    return jsonify({"error":"not authorised."}), 403
   
@drive_b.route('/drive/all/', methods = ['GET'])
@cache.cached(timeout=300, key_prefix='admin_drives')
def drive_all():
    res=[]
    drives = Drive.query.filter_by(status = 'approved').all()
    for drive in drives:
        res.append({
            "drive_id": drive.drive_id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "job_desc":drive.job_desc,
            "elig_branch": drive.elig_branch,
            "elig_year":drive.elig_year,
            "elig_cgpa": drive.elig_cgpa,
            "elig_min_cgpa": drive.elig_cgpa,
            "application_deadline": drive.application_deadline.isoformat(),
            "status": drive.status
        })
    return jsonify(res)

@drive_b.route('/drive/all/admin/', methods = ['GET'])
@jwt_required()
@cache.cached(timeout=300)
def drive_all_admin():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_email).first()
    if curr_user.role != 'admin':
        return jsonify({"error": "not authorised"}), 403
    res=[]
    drives = Drive.query.all()
    for drive in drives:
        res.append({
            "drive_id": drive.drive_id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "job_desc":drive.job_desc,
            "elig_branch": drive.elig_branch,
            "elig_year":drive.elig_year,
            "elig_cgpa": drive.elig_cgpa,
            "elig_min_cgpa": drive.elig_cgpa,
            "application_deadline": drive.application_deadline.isoformat(),
            "status": drive.status
        })
    return jsonify(res)

@drive_b.route('/drive/company/', methods=['GET'])
@jwt_required()
def company_drives():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_email).first()

    if not curr_user or curr_user.role != 'company':
        return jsonify({"error": "not authorised"}), 403

    curr_company = Company.query.filter_by(company_id=curr_user.id).first()

    if not curr_company:
        return jsonify({"error": "company not found"}), 404

    drives = Drive.query.filter_by(company_id=curr_company.company_id).all()

    res = []

    for drive in drives:
        res.append({
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "job_desc": drive.job_desc,
            "elig_branch": drive.elig_branch,
            "elig_year": drive.elig_year,
            "elig_cgpa": drive.elig_cgpa,
            "elig_min_cgpa": drive.elig_cgpa,
            "application_deadline": drive.application_deadline.isoformat(),
            "status": drive.status
        })

    return jsonify(res), 200

@drive_b.route('/drive/<int:id>', methods = ['GET'])
def drive_fetch_one(id):
    drive = Drive.query.filter_by(drive_id = id).first()
    if not drive:
        return jsonify({"error":"no drive found."}), 404
    return jsonify({
        "drive_id": drive.drive_id,
        "job_title": drive.job_title,
        "job_desc":drive.job_desc,
        "elig_branch": drive.elig_branch,
        "elig_year":drive.elig_year,
        "elig_cgpa": drive.elig_cgpa,
        "elig_min_cgpa": drive.elig_cgpa,
        "application_deadline": drive.application_deadline.isoformat(),
        "status": drive.status
        })
    
@drive_b.route('/drive/update/<int:id>', methods= ['PUT'])
@jwt_required()
def drive_update(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    data = request.get_json()
    drive = Drive.query.filter_by(drive_id = id).first()

    if not drive:
        return jsonify({"error":"no drive found."}), 404
    
    if (drive.company_id == curr_user.id and curr_user.role == 'company') or curr_user.role == 'admin':
        if data.get('job_title'):
            drive.job_title = data.get('job_title')

        if data.get('job_desc'):
            drive.job_desc = data.get('job_desc')
        
        if data.get('elig_branch'):
            drive.elig_branch = data.get('elig_branch')

        if data.get('elig_year'):
            drive.elig_year = int(data.get('elig_year'))

        if data.get('elig_min_cgpa'):
            drive.elig_cgpa = float(data.get('elig_min_cgpa'))
        elif data.get('elig_cgpa'):
            drive.elig_cgpa = float(data.get('elig_cgpa'))

        if data.get('application_deadline'):
            deadline_str = data.get('application_deadline')
            try:
                if 'T' in deadline_str:
                    drive.application_deadline = datetime.fromisoformat(deadline_str.replace('Z', ''))
                else:
                    drive.application_deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except Exception:
                return jsonify({"error": "invalid date format"}), 400

        db.session.commit()
        cache.clear()
        return jsonify({"message":"changes made successfully."}),200
    return jsonify({"error":"user not authorised or does not exist."}),403

@drive_b.route('/drive/delete/<int:id>', methods = [ 'DELETE'])
@jwt_required()
def drive_del(id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    drive = Drive.query.filter_by(drive_id = id).first()
    if not drive:
        return jsonify({"error":"no drive found."}), 404
    if not curr_user:
        return jsonify({"error":"user not found"}),403
    if (curr_user.role == 'company' and curr_user.id == drive.company_id )or curr_user.role == 'admin':
        db.session.delete(drive)
        db.session.commit()
        cache.clear()
        return jsonify({"message":"drive deleted successfully."}),200
    return jsonify({"error":"user not authorised or does not exist."}),403


