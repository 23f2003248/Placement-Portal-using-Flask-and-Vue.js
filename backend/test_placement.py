import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING']=True
    with app.test_client() as client:
        yield client

def test_student_register(client):
    response = client.post('/student/register/', json = {
        'name':'John Doe',
        'email':'yahoo999999@gmail.com',
        'password':'password123',
        'branch': 'CSE',
        'cgpa': 8.5,
        'year': 4
    })
    print(response.json)
    assert response.status_code == 201
    assert 'student_id' in response.json

def test_suplicate_email_register(client):
    client.post('/student/register/',json={
        'name':'Nehuti',
        'email':'yahoo00@gmail.com',
        'password':'nehuti',
        'branch':'CSE',
        'cgpa':9.2,
        'year':4
    })
    response = client.post('/student/register/',json={
        'name':'Drishti',
        'email':'yahoo00@gmail.com',
        'password':'drishti',
        'branch':'CSE',
        'cgpa':9.2,
        'year':4
    })
    assert response.status_code == 400
    assert 'email already exists' in response.json['error']

def test_register_missing_fields(client):
    response = client.post('/student/register/', json = {
        'name':'Drishti',
        'email':'yahoo11@gmail.com',
        'password':'drishti',
        'cgpa':9.2,
        'year':4
    })
    assert response.status_code == 400
    assert 'all fields req except resume' in response.json['error']

def test_fetch_student(client):
    create_response = client.post('/student/register/',json={
        'name':'Nehuti',
        'email':'yahoo1111111@gmail.com',
        'password':'nehuti',
        'branch':'CSE',
        'cgpa':9.2,
        'year':4
    })
    print(create_response.json)
    student_id = create_response.json['student_id']
    response = client.get(f'/student/{student_id}')

    assert response.status_code== 200

def test_fetch_nonexis_student(client):
    response = client.get(f'/student/444')

    assert response.status_code== 404

def test_fetch_all_std(client):
    response = client.get('/student/all/')
    assert response.status_code == 200