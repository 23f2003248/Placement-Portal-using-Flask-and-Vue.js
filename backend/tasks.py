from celery_app import celery, flask_app
from flask import current_app
from models import db, Student, Drive, Application, User, Company
from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail 
import io, csv

@celery.task
def daily_reminder():
    with flask_app.app_context():
        deadline_tom = datetime.utcnow() + timedelta(hours = 24)
        upcoming_drives = Drive.query.filter(
            Drive.application_deadline <= deadline_tom,
            Drive.status == 'approved'
        ).all()
        eligible_std=set()

        for drive in upcoming_drives:
            students = Student.query.join(User).filter(
                User.is_active == True,
                Student.cgpa >= drive.elig_cgpa,
                Student.branch == drive.elig_branch,           
                Student.year >= drive.elig_year,
                ~Application.query.filter(
                    Application.drive_id == drive.drive_id,
                    Application.student_id == Student.student_id,
                    Application.status == 'applied'
                ).exists()
            ).all()
            for student in students:    
                eligible_std.add(student.user.email)
        if not eligible_std:
            return "no eligible students."
        
        for email in eligible_std:
            msg = Message(
                subject = "Daily Placement Drive Reminder",
                sender = "nehutipvt@gmail.com",
                recipients = [email]
            )
            msg.body = f"You have {len(upcoming_drives)} upcoming drives with deadlines in 24 hours. Login to apply!"
            try:
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

        print("daily reminder task running!")
        return "done"

@celery.task
def monthly_report():
    with flask_app.app_context():
        now = datetime.now()
        month = now.month
        year = now.year

        drives = Drive.query.filter(
            db.extract('month', Drive.application_deadline) == month,
            db.extract('year', Drive.application_deadline) == year
        )

        monthly_applications = Application.query.filter(
            db.extract('month', Application.application_date) == month,
            db.extract('year', Application.application_date) == year
        )

        total_drives = drives.count()
        total_applications = monthly_applications.count()
        total_std_approved = Application.query.filter_by(status='selected').count()
        total_std_rejected = Application.query.filter_by(status='rejected').count()
    
        data=[]

        for drive in drives:
            applications = Application.query.filter_by(drive_id = drive.drive_id)
            data.append({
                'company_name': drive.company.company_name,
                'job_title': drive.job_title,
                'total_applications': applications.count(),
                'selected_applications': applications.filter_by(status='selected').count()
            })

        rows = ""
        for d in data:
            rows += f"""
            <tr>
                <td>{d['company_name']}</td>
                <td>{d['job_title']}</td>
                <td>{d['total_applications']}</td>
                <td>{d['selected_applications']}</td>
            </tr>
            """
            
        html = f"""
        <h1>Monthly Placement Report - {month}/{year}</h1>
        <h2>Summary</h2>
        <p>Total Drives: {total_drives}</p>
        <p>Total Applications: {total_applications}</p>
        <p>Total Selected: {total_std_approved}</p>
        <p>Total Rejected: {total_std_rejected}</p>

        <h2>Drive Breakdown</h2>
        <table>
            <tr>
                <th>Company</th>
                <th>Job Title</th>
                <th>Applicants</th>
                <th>Selected</th>
            </tr>
            {rows}
        </table>
        """
        msg = Message(
            subject=f"Monthly Placement Report - {month}/{year}",
            sender="nehutipvt@gmail.com",
            recipients=["admin@admin.com"]
        )

        msg.html = html
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send monthly report email: {e}")

        print("monthly report task running!")
        return "done"

@celery.task
def export_csv(student_id):
    with flask_app.app_context():
        applications = Application.query.filter_by(student_id = student_id).all()
        user = User.query.filter_by(id = student_id).first()
        student_email = user.email
        data = []
        
        for app in applications:
            data.append({
                'student_id':student_id,
                'company_name': app.drive.company.company_name,
                'job_title': app.drive.job_title,
                'status': app.status,
                'date': app.application_date
            })

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Student Id', 'Company Name', 'Job Title', 'Status', 'Date of Application'])
        for d in data:
            writer.writerow(
                [d['student_id'], d['company_name'], d['job_title'], d['status'], d['date']]
            )
        csv_data = output.getvalue().encode('utf-8')

        msg = Message(
            subject = "Your Placement Application History",
            sender = 'nehutipvt@gmail.com',
            recipients= [student_email]
        )
        msg.attach(
            filename="report.csv",
            content_type="text/csv",
            data= csv_data
        )
        msg.body = "This is your monthly placement report."
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send CSV export email to {student_email}: {e}")

        print(f"exporting CSV for student {student_id}")
        return "done"