import pytest
from mocks.create_mock_doctor_data import *
from mocks.create_mock_patient_data import *
from conftest import *


def test_show_all_doctor(client, sample_data):
    response = client.get('/api/doctors/show-all')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert len(response_data['doctors']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_record': 5,
            'current_page': '/api/doctors/show-all?page=1'
        }


def test_show_single_doctor(client, sample_data):
    response = client.get('/api/doctors/show-one/1')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['doctor']['id'] == 1
    assert response_data['doctor']['name'] == 'Marian'
    assert response_data['doctor']['last_name'] == 'Kowalski'
    assert response_data['doctor']['email']['email'] == 'okulista_przychodnia@wp.pl'
    assert response_data['doctor']['description'] == 'Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.'
    assert response_data['doctor']['specialty']['name'] == 'okulista'
    assert response_data['doctor']['seniority'] == '5 lat'
    assert response_data['doctor']['photo'] == 'https://cdn.pixabay.com/photo/2017/01/31/22/32/doctor-2027768_960_720.png'


def test_show_single_doctor_not_found(client, sample_data):
    response = client.get('/api/doctors/show-one/6')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'Not found.'


# testy do tworzenia profilu lekarza
@pytest.mark.parametrize("user_data, expected_status, expected_message", [
    (register_invalid_length_first_name_doctor, 400, {'name': ['Length must be between 2 and 255.']}),
    (register_invalid_length_last_name_doctor, 400, {'last_name': ['Length must be between 2 and 255.']}),
    (register_invalid_length_seniority_doctor, 400, {'seniority': ['Longer than maximum length 10.']}),
    (register_invalid_length_description_doctor, 400, {'description': ['Length must be between 2 and 255.']}),
    (register_invalid_length_photo_doctor, 400, {'photo': ['Length must be between 2 and 255.']}),
    (register_invalid_specialty_id_doctor, 404, 'Not found specialty.'),
    (register_invalid_role_user_id_doctor, 403, 'This user does not have permission to use this function.'),
    (register_not_found_user_id_doctor, 404, 'Not found user.'),
    (register_used_user_id_doctor, 409, 'This user is doctor.'),
    (register_mock_doctor_success, 201, 'Profile doctor created successfully.')
])
def test_creation_profile_doctor(client, user_data, expected_status, expected_message, sample_data, admin, token_admin):
    response = client.post('/api/doctors/create-profile', json=user_data, headers={'Authorization': f'Bearer {token_admin}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 201:
        assert response_data['success'] is True
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 404:
        assert response_data['success'] is False
    if expected_status == 409:
        assert response_data['success'] is False
    if expected_status == 403:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

# testy do tworzenia profilu lekarza - wymagane pola
def validate_required_field_doctor(client, sample_data, data, field_name, token_admin):
    data[field_name] = ''
    response = client.post('/api/doctors/create-profile', json=data, headers={'Authorization': f'Bearer {token_admin}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_registration_name_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_name_doctor, 'name', token_admin)

def test_registration_last_name_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_last_name_doctor, 'last_name', token_admin)

def test_registration_seniority_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_seniority_doctor, 'seniority', token_admin)

def test_registration_description_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_description_doctor, 'description', token_admin)

def test_registration_photo_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_photo_doctor, 'photo', token_admin)

def test_registration_specialty_id_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_specialty_id_doctor, 'specialty_id', token_admin)

def test_registration_user_id_doctor_required(client, sample_data, token_admin):
    validate_required_field_doctor(client, sample_data, register_no_user_id_doctor, 'user_id', token_admin)


# testy do podglądu grafiku lekarza dla pacjentów
@pytest.mark.parametrize("doctor_id, date, expected_status, expected_message, expected_hours_count", [
    (1, '21-11-2024', 200, 'True', 15),
    (6, '21-11-2024', 404, 'Not found doctor.', None),
    (1, '20-11-2023', 400, 'There is no such day.', None),
])
def test_show_hours_doctor(client, sample_data, token, doctor_id, date, expected_status, expected_message, expected_hours_count):
    response = client.get(f'/api/doctors/hours/{doctor_id}/{date}', headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response_data['success'] is True
        assert response_data['doctor']['id'] == doctor_id
        assert response_data['doctor']['name'] == 'Marian'
        assert response_data['doctor']['last_name'] == 'Kowalski'
        assert response_data['doctor']['email']['email'] == 'okulista_przychodnia@wp.pl'
        assert response_data['doctor']['specialty']['name'] == 'okulista'
        assert len(response_data['hours_available']) == expected_hours_count
    elif expected_status == 404:
        assert response_data['message'] == expected_message
        assert response_data['success'] is False
    elif expected_status == 400:
        assert response_data['message'] == expected_message
        assert response_data['success'] is False


# testy do podglądu karty lekarza
@pytest.mark.parametrize("doctor_id, expected_status, expected_message", [
    (2, 200, 'True'),
    (6, 404, 'Not found doctor.'),
])
def test_show_card_doctor(client, sample_data, token_receptionist, doctor_id, expected_message, expected_status):
    response = client.get(f'/api/doctors/show-card/{doctor_id}', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    if expected_status == 404:
        assert response_data['success'] is False
        assert response_data['message'] == expected_message
    if expected_status == 200:
        assert len(response_data['submissions']) == 3
        assert response_data['success'] is True

