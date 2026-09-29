from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db, Application, Drive, Company, Student
from datetime import datetime
from tasks import export_csv

app_b = Blueprint('application', __name__)

@app_b.route('/application/register', methods = ['POST'])
@jwt_required()
def application_register():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    if not curr_user:
        return jsonify({"error":"user not found"}), 404

    data = request.get_json()
    drive_id = data.get('drive_id')
    if not drive_id:
        return jsonify({"error":"drive_id is required."}), 400

    curr_std = Student.query.filter_by(student_id = curr_user.id).first()
    if not curr_std:
        return jsonify({"error":"student profile not found."}), 404

    drive = Drive.query.filter_by(drive_id=drive_id, status = 'approved').first()
    if not drive:
        return jsonify({"error":"drive not found or not approved!"}), 404
    
    existing_app = Application.query.filter_by(student_id=curr_std.student_id, drive_id=drive.drive_id).first()
    if existing_app:
        return jsonify({"error":"You have already applied for this drive."}), 400

    eligible_branches = [b.strip().upper() for b in drive.elig_branch.replace(',', ' ').split() if b.strip()]
    student_branch = curr_std.branch.strip().upper()

    if curr_user.role == 'student' and curr_std.cgpa >= drive.elig_cgpa and student_branch in eligible_branches and curr_std.year >= drive.elig_year:
        if datetime.utcnow() > drive.application_deadline:
            return jsonify({"error":"deadline has passed!"}),400
        
        new_app = Application(
            drive_id = drive.drive_id,
            student_id = curr_std.student_id,
            status = 'applied'
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"message":"application created successfully."}), 201
    return jsonify({"error":"You do not meet the eligibility criteria for this drive."}), 403

@app_b.route('/application/all', methods = ['GET'])
@jwt_required()
def application_fetch_all():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    if not curr_user:
        return jsonify({"error":"user not found"}), 404
    if curr_user.role == 'admin':
        apps = Application.query.all()
        if not apps:
            return jsonify([]), 200
        res = []
        for app in apps:
            res.append({
                'application_id': app.application_id,
                'student_id': app.student_id,
                'drive_id': app.drive.drive_id,
                'application_date': app.application_date.isoformat(),
                'status': app.status
            })
        return jsonify(res)
    return jsonify({"error":"user not authorised."}), 403

@app_b.route('/application/drive/<int:drive_id>', methods = ['GET'])
@jwt_required()
def application_fetch_company_drive_app(drive_id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_email).first()
    if not curr_user:
        return jsonify({"error":"no user found."}), 404
    
    drive = Drive.query.filter_by(drive_id = drive_id).first()
    if not drive:
        return jsonify({"error":"drive not found."}), 404

    # Enforce ownership: only the drive's company or the admin can view applications
    if curr_user.role == 'company' and drive.company_id != curr_user.id:
        return jsonify({"error": "not authorised to view applications for this drive."}), 403
    
    if (curr_user.role == 'company' and drive.company_id == curr_user.id) or curr_user.role == 'admin':
        apps = Application.query.filter_by(drive_id = drive_id).all()
        if not apps:
            return jsonify([]), 200
        res=[]
        for app in apps:
            res.append({
                'application_id': app.application_id,
                'student_id': app.student_id,
                'drive_id': app.drive.drive_id,
                'application_date': app.application_date.isoformat(),
                'status': app.status,
                'student_name': app.student.user.name,
                'email': app.student.user.email,
                'branch': app.student.branch,
                'cgpa': app.student.cgpa,
                'year': app.student.year,
                'resume': app.student.resume if app.student.resume else '',
                'interview_date': app.interview_date.isoformat() if app.interview_date else None
            })
        return jsonify(res)
    return jsonify({"error": "not authorised"}), 403
    
@app_b.route('/application/my/', methods = ['GET'])
@jwt_required()
def application_fetch_one_student():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email = curr_email).first()
    if not curr_user:
        return jsonify({"error":"no user found."}), 404
    curr_std = Student.query.filter_by(student_id = curr_user.id).first()
    if not curr_std:
        return jsonify({"error":"student profile not found."}), 404
    apps = Application.query.filter_by(student_id = curr_std.student_id).all()
    if not apps:
        return jsonify([]), 200
    res=[]
    for app in apps:
        res.append({
            'application_id': app.application_id,
            'student_id': app.student_id,
            'drive_id': app.drive.drive_id,
            'company_name': app.drive.company.company_name,
            'job_title': app.drive.job_title,
            'application_date': app.application_date.isoformat(),
            'status': app.status,
            'interview_date': app.interview_date.isoformat() if app.interview_date else None
        })
    return jsonify(res)

@app_b.route('/application/update/<int:app_id>', methods = ['PUT'])
@jwt_required()
def application_update(app_id):
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_email).first()
    if not curr_user:
        return jsonify({"error":"no user found."}), 404
    app = Application.query.filter_by(application_id = app_id).first()
    if not app:
        return jsonify({"error":"no application found."}), 404
    drive = app.drive
    if drive.company_id != curr_user.id:
        return jsonify({"error":"not authorised"}), 403
    
    if curr_user.role == 'company':
        data = request.get_json()
        if data.get('status'):
            status = data.get('status').lower()
            if status in ['applied', 'shortlisted', 'interview_scheduled', 'selected', 'rejected']:
                app.status = status

        if data.get('interview_date'):
            date_str = data.get('interview_date')
            try:
                if 'T' in date_str:
                    app.interview_date = datetime.fromisoformat(date_str.replace('Z', ''))
                else:
                    app.interview_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                app.status = 'interview_scheduled'
            except Exception:
                return jsonify({"error": "invalid interview date format"}), 400

        db.session.commit()
        return jsonify({"message":"updated successfully!"})
    return jsonify({"error":"not authorised!"}), 403

@app_b.route('/application/export/', methods = ['POST'])
@jwt_required()
def application_export():
    curr_email = get_jwt_identity()
    curr_user = User.query.filter_by(email=curr_email).first()
    if not curr_user:
        return jsonify({"error":"no user found."}), 404
    if curr_user.role == 'student':
        try:
            export_csv.delay(curr_user.id)
            return jsonify({"message": "Export started in background! You will receive an email shortly."}), 200
        except Exception as e:
            print(f"Warning: Celery/Redis connection failed ({e}). Running export task synchronously.")
            # Run task synchronously in the current thread/process
            try:
                export_csv(curr_user.id)
                return jsonify({"message": "Export completed synchronously! You will receive an email shortly."}), 200
            except Exception as se:
                return jsonify({"error": f"Export failed: {se}"}), 500
    return jsonify({"error":"not authorised!"}), 403


        
    
   



