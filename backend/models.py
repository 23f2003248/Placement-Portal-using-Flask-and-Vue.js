from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(1000), nullable = False)
    role = db.Column(db.String(100), nullable = False) #admin/company/student
    is_active = db.Column(db.Boolean, default = True)

    def __repr__(self):
        return f"<{self.name}-{self.id}>"
    
class Student(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    branch = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)   
    resume = db.Column(db.String(100))

    user = db.relationship('User')

    def __repr__(self):
        return f"<Student-{self.student_id}>"

class Company(db.Model):
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_name = db.Column(db.String(300), nullable=False)
    hr_contact = db.Column(db.String(300), nullable=False) #mail
    website = db.Column(db.String(400), unique = True, nullable=False)
    approval_status = db.Column(db.String(100), default = 'pending', nullable=False) 

    user = db.relationship('User')

    def __repr__(self):
        return f"<{self.company_name}-{self.company_id}>"

class Drive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    job_desc = db.Column(db.String(1000), nullable=False)
    elig_branch = db.Column(db.String(50), nullable=False) 
    elig_year = db.Column(db.Integer, nullable=False)
    elig_cgpa = db.Column(db.Float, nullable=False) 
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(100), default = 'pending', nullable=False) #(Pending / Approved / Closed)

    company = db.relationship('Company')

    def __repr__(self):
        return f"<{self.drive_id}>"

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.drive_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(100), default='applied', nullable=False) # (applied / shortlisted / interview_scheduled / selected / rejected)
    interview_date = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
    db.UniqueConstraint('student_id', 'drive_id'),
    )

    student = db.relationship('Student')
    drive = db.relationship('Drive')

    def __repr__(self):
        return f"<{self.application_id}>"



