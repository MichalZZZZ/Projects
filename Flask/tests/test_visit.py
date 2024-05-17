import pytest
from mocks.register_mock_user_data import *
from mocks.create_mock_patient_data import *
from mocks.create_mock_doctor_data import *
from mocks.create_mock_submission_data import *
from mocks.create_mock_visits_data import *
from conftest import *


def test_show_all_visits(client, sample_data, token_doctor):
    response = client.get('/api/visits/show-all', headers={'Authorization': f'Bearer {token_doctor}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 3
    assert len(response_data['visits']) == 3
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_record': 3,
            'current_page': '/api/visits/show-all?page=1'
        }
    

# test do podgladu swoich wizyt pacjenta
def test_show_all_visits_me(client, sample_data, token_patient):
    response = client.get('/api/visits/show-all/me', headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 1
    assert len(response_data['visits']) == 1
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_record': 1,
            'current_page': '/api/visits/show-all/me?page=1'
        }
    
# gdy pacjent nie ma profilu pacjenta
def test_show_all_visis_me_no_profile(client, sample_data, token):
    response = client.get('/api/visits/show-all/me', headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'You dont have patient profile.'

# gdy pacjent nie ma wizyt
def test_show_all_visis_me_no_visits(client, sample_data, token_patientnovisit):
    response = client.get('/api/visits/show-all/me', headers={'Authorization': f'Bearer {token_patientnovisit}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'You dont have visits.'


# testy do tworzenia wizyty
@pytest.mark.parametrize("submission_id, data, expected_status, expected_message", [
    (15, visit_submission_not_exist, 404, 'Not found submission.'),
    (5, visit_submissions_created, 201, 'Visit created.'),
    (6, visit_submission_not_allowed, 403, 'You are not allowed to create a visit for this submission.'),
    (7, visit_submission_status_visited, 400, 'The submission is pending or has been rejected.'),
    (5, visit_submissions_validate_length_recommendations, 400, {'recommendations': ['Length must be between 2 and 255.']}),
    (5, visit_submissions_validate_length_drugs, 400, {'drugs': ['Length must be between 2 and 255.']}),
    (5, visit_submissions_validate_length_diagnosis, 400, {'diagnosis': ['Length must be between 2 and 255.']})
])
def test_create_visit(client, sample_data, token_doctor, submission_id, data, expected_status, expected_message):
    response = client.post(f'/api/visits/create/{submission_id}', json=data, headers={'Authorization': f'Bearer {token_doctor}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['message'] == expected_message
    if expected_status == 404:
        assert response_data['success'] is False
    if expected_status == 403:
        assert response_data['success'] is False
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 201:
        assert response_data['success'] is True

# testy do tworzenia wizyty - wymagane pola
def validate_required_field_visit(client, sample_data, data, field_name, token_doctor):
    data[field_name] = '   '
    response = client.post('/api/visits/create/5', json=data, headers={'Authorization': f'Bearer {token_doctor}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_create_submission_required_recommendations(client, sample_data, token_doctor):
    validate_required_field_visit(client, sample_data, visit_submissions_no_recommendations, 'recommendations', token_doctor)

def test_create_submission_required_drugs(client, sample_data, token_doctor):
    validate_required_field_visit(client, sample_data, visit_submissions_no_drugs, 'drugs', token_doctor)

def test_create_submission_required_diagnosis(client, sample_data, token_doctor):
    validate_required_field_visit(client, sample_data, visit_submissions_no_diagnosis, 'diagnosis', token_doctor)


