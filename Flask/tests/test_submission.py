from flask import request
import pytest
from mocks.register_mock_user_data import *
from mocks.create_mock_patient_data import *
from mocks.create_mock_doctor_data import *
from mocks.create_mock_submission_data import *
from conftest import *


# testy do wyswietlania wszystkich zgloszen
def test_show_all_submissions(client, sample_data, token_receptionist):
    response = client.get('/api/submissions/show-all', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 5
    assert len(response_data['submissions']) == 5
    assert response_data['pagination'] == {
            'total_pages': 2,
            'total_record': 10,
            'current_page': '/api/submissions/show-all?page=1',
            'next_page': '/api/submissions/show-all?page=2'
        }


# testy do wyswietlania pojedynczego zgloszenia
@pytest.mark.parametrize("submission_id, expected_status, expected_message", [
    (15, 404, 'Not found submission.'),
    (1, 200, 'True'),
])
def test_show_single_submission(client, sample_data, token_receptionist, submission_id, expected_status, expected_message):
    response = client.get(f'/api/submissions/show/{submission_id}', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 404:
        assert response_data['success'] is False
        assert response_data['message'] == expected_message
    if expected_status == 200:
        assert response_data['success'] is True
        assert response_data['submission']['number'] == 1
        assert response_data['submission']['medications_used'] == 'asd'
        assert response_data['submission']['symptoms'] == 'bol glowy'
        assert response_data['submission']['day'] == '18-11-2024'
        assert response_data['submission']['hour'] == '16:00'
        assert response_data['submission']['status'] == 'accepted'


#testy do podgladu swoich zgloszen
def test_show_submission_patient(client, sample_data, token_patient):
    response = client.get('/api/submissions/show-all/me', headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert len(response_data['submissions']) == 3
    assert response_data['number_of_records'] == 3
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_record': 3,
            'current_page': '/api/submissions/show-all/me?page=1'
        }

# gdy pacjent nie ma profilu pacjenta
def test_show_submission_not_profile_patient(client, sample_data, token):
    response = client.get('/api/submissions/show-all/me', headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'You dont have patient profile.'

# gdy pacjent nie ma zgloszen
def test_show_all_visis_me_no_submission(client, sample_data, token_patientnovisit):
    response = client.get('/api/submissions/show-all/me', headers={'Authorization': f'Bearer {token_patientnovisit}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'You dont have submission.'



# testy do tworzenia zgloszenia  
# gdy uzytkownik nie ma profilu pacjenta
def test_create_submission_not_patient_profile(client, sample_data, token):
    response = client.post('/api/submissions/create', json=submission_create_success, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'You dont have patient profile.'

# gdy uzytkownik ma profil pacjenta
@pytest.mark.parametrize("submission_data, expected_status, expected_message", [
    (submission_create_not_found_doctor, 404, 'Doctor not found.'),
    (submission_create_at_least_1_hours_in_advance, 400, 'You must schedule the appointment at least 1 hours in advance.'),
    (submission_create_past_date_or_time, 400, 'You cannot choose a past date or time.'),
    (submission_create_invalid_hour, 400, "Valid hours are: ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']"),
    (submission_create_already_term_taken, 400, 'This term is already taken.'),
    (submission_create_no_medications_used, 400, {'medications_used': ['Length must be between 2 and 255.']}),
    (submission_create_no_symptoms, 400, {'symptoms': ['Length must be between 2 and 255.']}),
    (submission_create_not_valid_day, 400, {'day': ['Not a valid date.']}),
    (submission_create_not_valid_hour, 400, {'hour': ['Not a valid time.']}),
    (submission_create_success, 201, 'Submission created successfully.'),
])
def test_create_submission(client, sample_data, submission_data, expected_status, expected_message, token_patient):
    response = client.post('/api/submissions/create', json=submission_data, headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 404:
        assert response_data['success'] is False
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 201:
        assert response_data['success'] is True
    assert response_data['message'] == expected_message


# testy do tworzenia zgloszenia - wymagane pola
def validate_required_field_submission(client, sample_data, data, field_name, token_patient):
    data[field_name] = '   '
    response = client.post('/api/submissions/create', json=data, headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_create_submission_required_medications_used(client, sample_data, token_patient):
    validate_required_field_submission(client, sample_data, submission_create_no_medications_used, 'medications_used', token_patient)

def test_create_submission_required_symptoms(client, sample_data, token_patient):
    validate_required_field_submission(client, sample_data, submission_create_no_symptoms, 'symptoms', token_patient)


# testy do anulowania zgłoszenia
@pytest.mark.parametrize("submission_id, expected_status, expected_message", [
    (15, 404, 'Submission on 15 do not exists.'),
    (2, 403, 'This submission does not belong to you.'),
    (3, 400, 'You cannot cancel your submission 24 hours in advance.'),
    (4, 200, 'Your submission for 2024-11-09 at: 15:00 has been canceled.')
])
def test_canceled_submission(client, sample_data, submission_id, expected_status, expected_message, token_patient):
    response = client.delete(f'/api/submissions/cancel/{submission_id}', headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    print(response_data)
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 404:
        assert response_data['success'] is False
    if expected_status == 403:
        assert response_data['success'] is False
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 200:
        assert response_data['success'] is True
    assert response_data['message'] == expected_message


# testy do sprawdzania poprawnosci zgloszenia
@pytest.mark.parametrize("submission_id, data, expected_status, expected_message", [
    (15, change_status_submission, 404, 'Submission on 15 do not exists.'),
    (1, change_status_submission_2, 400, 'This submission has already been considered.'),
    (2, change_status_submission_3, 200, 'The submission status has been changed to: rejected.'),
])
def test_check_correctness_submission(client, submission_id, data, expected_status, expected_message, sample_data, token_receptionist):
    response = client.post(f'/api/submissions/check-correctness/{submission_id}', json=data, headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['message'] == expected_message
    if expected_status == 404:
        assert response_data['success'] is False
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 200:
        assert response_data['success'] is True