from clinic_app import create_app, db
import pytest
from mocks.register_mock_user_data import register_mock_user, register_mock_admin, register_mock_user_patient, register_mock_user_receptionist, register_mock_user_doctor, register_mock_user_novisit
from mocks.create_mock_patient_data import register_mock_patient, register_mock_patient_x
from mocks.create_mock_doctor_data import register_mock_doctor
from mocks.create_mock_submission_data import submission_create_success
from mocks.create_mock_receptionist_data import create_mock_receptionist
from clinic_app.models import Patient, User, Token, TokenSetPassword
from clinic_app.commands.db_commands import add_data_test
import json
from clinic_app.utils import generate_reset_token



@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()
        db.session.commit()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin(client):
    client.post('/api/admin/add', json=register_mock_admin)
    return register_mock_admin


@pytest.fixture
def user(client):
    client.post('/api/auth/register', json=register_mock_user)
    return register_mock_user


@pytest.fixture
def user_patient(client):
    client.post('/api/auth/register', json=register_mock_user_patient)
    return register_mock_user_patient


@pytest.fixture
def token_patient(client, user_patient):
    response = client.post('api/auth/login', json={
        'username': user_patient['username'],
        'password': user_patient['password']
    })
    return response.get_json()['token']


@pytest.fixture
def user_patient_novisit(client):
    client.post('/api/auth/register', json=register_mock_user_novisit)
    return register_mock_user_novisit

@pytest.fixture
def token_patientnovisit(client, user_patient_novisit):
    response = client.post('api/auth/login', json={
        'username': user_patient_novisit['username'],
        'password': user_patient_novisit['password']
    })
    return response.get_json()['token']


@pytest.fixture
def patient(client, user):
    client.post('/api/patients/create', json=register_mock_patient)
    return register_mock_patient


@pytest.fixture
def doctor(client, user):
    client.post('/api/doctors/create', json=register_mock_doctor)
    return register_mock_doctor


@pytest.fixture
def user_doctor(client):
    client.post('/api/auth/register', json=register_mock_user_doctor)
    return register_mock_user_doctor

@pytest.fixture
def token_doctor(client, user_doctor):
    response = client.post('api/auth/login', json={
        'username': user_doctor['username'],
        'password': user_doctor['password']
    })
    return response.get_json()['token']


@pytest.fixture
def reception(client, user):
    client.post('/api/reception/create', json=create_mock_receptionist)
    return create_mock_receptionist


@pytest.fixture
def user_receptionist(client):
    client.post('/api/auth/register', json=register_mock_user_receptionist)
    return register_mock_user_receptionist

@pytest.fixture
def token_receptionist(client, user_receptionist):
    response = client.post('api/auth/login', json={
        'username': user_receptionist['username'],
        'password': user_receptionist['password']
    })
    return response.get_json()['token']


@pytest.fixture
def token(client, user):
    response = client.post('api/auth/login', json={
        'username': user['username'],
        'password': user['password']
    })
    return response.get_json()['token']


@pytest.fixture
def token_admin(client, admin):
    response = client.post('api/auth/login', json={
        'username': admin['username'],
        'password': admin['password']
    })
    return response.get_json()['token']


@pytest.fixture
def submission(client, patient, doctor):
    response = client.post('/api/submissions/create', json={submission_create_success})
    return response.get_json()


@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data_test)