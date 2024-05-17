import pytest
from conftest import *
from mocks.create_mock_receptionist_data import *


def test_show_all_reception(client, sample_data):
    response = client.get('/api/reception/show-all')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert len(response_data['receptionists']) == 2


@pytest.mark.parametrize("user_data, expected_status, expected_message", [
    (register_invalid_length_first_name_receptionist, 400, {'name': ['Length must be between 2 and 255.']}),
    (register_invalid_length_last_name_receptionist, 400, {'last_name': ['Length must be between 2 and 255.']}),
    (register_invalid_phone_number_receptionist, 400, {'phone_number': ['Invalid phone number format.']}),
    (register_used_phone_number_receptionist, 409, 'Phone number already exists.'),
    (create_mock_receptionist_success, 201, 'Receptionist profile created successfully.'),
    (register_invalid_user_id_receptionist, 404, 'Not found user.'),
    (register_used_user_id_receptionist, 409, 'This user have a receptionist profile.'),
    (register_invalid_role_user_id_receptionist, 403, 'This user does not have permission to use this function.'),
])
def test_create_receptionist(client, user_data, expected_status, expected_message, sample_data, token_admin):
    response = client.post('/api/reception/create', json=user_data, headers={'Authorization': f'Bearer {token_admin}'})
    response_data = response.get_json()
    print(response_data)
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


def validate_required_field_receptionist(client, sample_data, data, field_name, token_admin):
    data[field_name] = ''
    response = client.post('/api/reception/create', json=data, headers={'Authorization': f'Bearer {token_admin}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_registration_name_receptionist_required(client, sample_data, token_admin):
    validate_required_field_receptionist(client, sample_data, register_no_name_receptionist, 'name', token_admin)

def test_registration_name_receptionist_required(client, sample_data, token_admin):
    validate_required_field_receptionist(client, sample_data, register_no_last_name_receptionist, 'last_name', token_admin)

def test_registration_name_receptionist_required(client, sample_data, token_admin):
    validate_required_field_receptionist(client, sample_data, register_no_user_id_receptionist, 'user_id', token_admin)