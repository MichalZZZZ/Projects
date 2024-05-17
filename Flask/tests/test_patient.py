import pytest
from mocks.register_mock_user_data import *
from mocks.create_mock_patient_data import *
from conftest import *

# def test_check_database_state(client, app, user, token, sample_data):
#     with app.app_context():
#         # Przykładowe zapytanie do bazy danych
#         patients_count = db.session.query(Patient).all()
#         for i in range(0 ,3):
#             print(patients_count[i].user_id)

#     assert patients_count == 3



def test_show_all_patients(client, sample_data, token_receptionist):
    response = client.get('/api/patients/show-all', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert len(response_data['patients']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_record': 5,
            'current_page': '/api/patients/show-all?page=1'
    }


def test_show_one_patient(client, sample_data, token_receptionist):
    response = client.get('/api/patients/show-one/1', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['patient']['first_name'] == 'Michal'
    assert response_data['patient']['last_name'] == 'Ziolkowski'
    assert response_data['patient']['pesel'] == '65082724332'
    assert response_data['patient']['phone_number'] == '888888888'
    assert response_data['patient']['address'] == 'ul. Sloneczna 54, 10-722 Olsztyn'
    assert response_data['patient']['user_id'] == 7
    assert response_data['treatment_history'] == []


def test_show_one_patient_not_found(client, sample_data, token_receptionist):
    response = client.get('/api/patients/show-one/10', headers={'Authorization': f'Bearer {token_receptionist}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == 'Not found patient.'


#testy do tworzenia profilu pacjenta
@pytest.mark.parametrize("user_data, expected_status, expected_message", [
    (register_invalid_length_first_name_user, 400, {'first_name': ['Length must be between 2 and 255.']}),
    (register_invalid_length_last_name_user, 400, {'last_name': ['Length must be between 2 and 255.']}),
    (register_invalid_pesel_user, 400, {'pesel': ['Invalid PESEL format.']}),
    (register_invalid_phone_number_user, 400, {'phone_number': ['Invalid phone number format.']}),
    (register_invalid_length_address_user, 400, {'address': ['Length must be between 3 and 255.']}),
    (register_mock_patient_success, 201, 'Profile created successfully.')
])
def test_creation_profile_patient(client, user_data, expected_status, expected_message, token):
    response = client.post('/api/patients/create', json=user_data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 201:
        assert response_data['success'] is True
    if expected_status == 400:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

#testy do tworzenia profilu pacjenta - gdy pesel lub numer telefonu juz istnieje 
@pytest.mark.parametrize("user_data, expected_status, expected_message", [
    (register_used_pesel_user, 409, 'This PESEL is already linked to the account.'),
    (register_used_phone_number_user, 409, 'Phone number already exists.')
])
def test_creation_profile_exists_pesel_or_phone(client, user_data, expected_status, expected_message, sample_data, token):

    response = client.post('/api/patients/create', json=user_data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 409:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

#testy do tworzenia profilu pacjenta - gdy pacjent juz ma profil
def test_creation_profile_exists_profile(client, token, sample_data):

    response = client.post('/api/patients/create', json=register_mock_patient_2, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'This PESEL is already linked to the account.'




#testy do tworzenia profilu pacjenta - wymagane pola
def validate_required_field_2(client, data, field_name, token):
    data[field_name] = '      '
    response = client.post('/api/patients/create', json=data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'
def test_registration_first_name_required(client, token):
    validate_required_field_2(client, register_no_first_name_user, 'first_name', token)

def test_registration_last_name_required(client, token):
    validate_required_field_2(client, register_no_last_name_user, 'last_name', token)

def test_registration_address_required(client, token):
    validate_required_field_2(client, register_no_address_user, 'address', token)



# testy do podgladu swojego profilu pacjenta
def test_show_my_profile(client, user, patient, token, sample_data):
    response = client.get('/api/patients/profile-me', headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    if response.status_code == 200:
        assert response_data['success'] is True
        assert response_data['patient']['first_name'] == patient['first_name']
        assert response_data['patient']['last_name'] == patient['last_name']
        assert response_data['patient']['pesel'] == patient['pesel']
        assert response_data['patient']['phone_number'] == patient['phone_number']
        assert response_data['patient']['user_id'] == patient['user_id']
    if response.status_code == 404:
        assert response_data['success'] is False
        assert response_data['message'] == "You don't have a patient profile."

# gdy uzytkownik nie poda tokenu
def test_show_my_profile_missing_token(client, user, sample_data):
    response = client.get('api/patients/profile-me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login or register'



#testy do aktualizacji numeru telefonu uzytkownika
def test_update_phone_number_user_not_profile(client, user, token):
    response = client.patch('/api/patients/update-phone', json={'phone_number': '666555444'}, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == "You don't have a patient profile."

update_phone_number_user_data = [
    (invalid_phone_number_update, 400, {'phone_number': ['Invalid phone number format.']}),
    (already_exists_phone_number_update, 409, 'This phone number already exists.'),
    (success_update_phone_number, 200, 'Your phone number has been updated.')
]
@pytest.mark.parametrize("user_data, expected_status, expected_message", update_phone_number_user_data)
def test_update_phone_number_user_with_profile(client, sample_data, user_data, expected_status, expected_message, token_patient):
    response = client.patch('/api/patients/update-phone', json=user_data, headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 409:
        assert response_data['success'] is False
    if expected_status == 200:
        assert response_data['success'] is True
    if expected_status == 400:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message


#testy do usuwania profilu pacjenta
@pytest.mark.parametrize("password_data, expected_status, expected_message", [
    (delete_account_user_bad_password, 400, 'Bad password.'),
    (delete_account_user_bad_confirm_password, 400, 'Passwords do not match.'),
    (delete_account_user_success, 200, 'Your profile has been deleted.')
])
def test_delete_patient_profile(client, password_data, expected_status, expected_message, sample_data, token_patient):
    response = client.delete('/api/patients/delete-profile', json=password_data, headers={'Authorization': f'Bearer {token_patient}'})
    response_data = response.get_json()
    print(response_data)
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 200:
        assert response_data['success'] is True
    if expected_status == 404:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

def test_delete_patient_no_profile(client, sample_data, token):
    response = client.delete('/api/patients/delete-profile', json=delete_account_user_success, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == "You dont have patient profile."