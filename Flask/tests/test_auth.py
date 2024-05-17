import pytest, jwt
from mocks.register_mock_user_data import *
from conftest import *
from config import Config


def test_get_users(client, sample_data, token_admin, admin):
    response = client.get('/api/auth/users', headers={'Authorization': f'Bearer {token_admin}'})
    response_data = response.get_json()
    print(response_data)
    assert response.status_code == 200
    assert response_data['success'] is True
    assert len(response_data['users']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination'] == {
            'total_pages': 4,
            'total_record': 16,
            'current_page': '/api/auth/users?page=1',
            'next_page': '/api/auth/users?page=2'
    }



#testy do rejestracji uzytkownika
@pytest.mark.parametrize("user_data, expected_status, expected_message", [
    (register_ivalid_email_user, 400, 'Invalid email format.'),
    (register_invalid_length_password_user, 400, 'Password must be at least 6 characters.'),
    (register_used_username_user, 409, 'Username already exists.'),
    (register_used_email_user, 409, 'Email already exists.'),
    (register_successfuly_user, 201, 'User created successfully.')
])
def test_registration(client, user_data, expected_status, expected_message, user):
    response = client.post('/api/auth/register', json=user_data)
    response_data = response.get_json()
    print(response_data)
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 409:
        assert response_data['success'] is False
    if expected_status == 201:
        assert response_data['success'] is True
        assert response_data['token']
    if expected_status == 400:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

#testy do rejestracji uzytkownika - wymagane pola
def validate_required_field(client, data, field_name):
    data[field_name] = '      '
    response = client.post('/api/auth/register', json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_registration_username_required(client):
    validate_required_field(client, register_no_username_user, 'username')

def test_registration_password_required(client):
    validate_required_field(client, register_no_password_user, 'password')

def test_registration_confirm_password_required(client):
    validate_required_field(client, register_no_confirm_password_user, 'confirm_password')


#testy do logowania
login_test_data = [
    (invalid_password_user, 401, 'Invalid username or password.'),
    (invalid_username_user, 401, 'Invalid username or password.'),
    (valid_user, 200, '')
]
@pytest.mark.parametrize("user_data, expected_status, expected_message", login_test_data)
def test_login_user(client, user_data, expected_status, expected_message, user):
    response = client.post('/api/auth/login', json=user_data)
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 401:
        assert response_data['success'] is False
        assert response_data['message'] == expected_message
    else:
        assert response_data['success'] is True
        assert 'token' in response_data

def test_login_user_logged_in(client, user, token):
    response = client.post('/api/auth/login', json=valid_user,
                           headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'You are already logged in.'


#testy do wylogowania
def test_logout_succes(client, user, token):
    response = client.post('/api/auth/logout', headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] == 'True'
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['message'] == 'Logged out successfully.'

def test_logout_expired_token(client, user):
    response = client.post('/api/auth/logout', headers={'Authorization': f'Bearer {expired_token}'})
    response_data = response.get_json()
    assert response.status_code == 401
    assert response_data['success'] is False
    assert response.headers['Content-Type'] == 'application/json'
    # assert response_data['message'] == 'Your session has expired.'
    assert response_data['message'] == 'Expired token. Please login or register'

def test_logout_invalid_token(client, user, token):
    response = client.post('/api/auth/logout', headers={'Authorization': f'Bearer {token}1xc'})
    response_data = response.get_json()
    assert response.status_code == 401
    assert response_data['success'] is False
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['message'] == 'Invalid token. Please login or register'  



# testy do wyslania linku do resetowania hasla
remind_password_user_data = [
    ('', 400, 'Please enter your email address.'),
    ('testing@gmail.com', 404, 'This email is not associated with any account.'),
    ('test@gmail.com', 200, 'We have sent a password reset link to your email.')
]
@pytest.mark.parametrize("email, expected_status, expected_message", remind_password_user_data)
def test_send_email_reset_password(client, email, user, expected_status, expected_message):
    response = client.post('/api/auth/reset-password',
                           json={'email': email})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 200:
        assert response_data['success'] is True
    elif expected_status == 404:
        assert response_data['success'] is False
    else:
        assert response_data['success'] is False
    assert expected_message in response_data['message']

# testy do zmiany hasla uzytkownika - gdy uzytkownik zapomni hasła
def test_reset_password_bad_token(client, user):
    response = client.post(f'/api/auth/reset-password/{user["email"]}/oierjndsoicfnksdaklfn23i45rfsdfsdzf', json={'password': 'test123', 'confirm_password': 'test123'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Invalid or expired reset link.'

def test_reset_password_bad_email(client, user, sample_data):
    response = client.post(f'/api/auth/reset-password/bad@gmail.com/lFaE3QRFU7pxYU3nln7RRpF7kwndMDsJhSR4oz50GYM', json={'password': 'test123', 'confirm_password': 'test123'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Invalid email.'

def test_reset_password_bad_password(client, user, sample_data):
    response = client.post(f'/api/auth/reset-password/{user["email"]}/lFaE3QRFU7pxYU3nln7RRpF7kwndMDsJhSR4oz50GYM', json={'password': 'test123', 'confirm_password': 'test12'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Passwords do not match.'

def test_reset_password_success(client, user, sample_data):
    response = client.post(f'/api/auth/reset-password/{user["email"]}/lFaE3QRFU7pxYU3nln7RRpF7kwndMDsJhSR4oz50GYM', json={'password': 'test123', 'confirm_password': 'test123'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['message'] == 'Password has been changed successfully.'



#testy do zmiany hasla zalogowanego uzytkownika
update_password_test_data = [
    (bad_current_password_update_user, 400, 'Bad password.'),
    (bad_new_password_update_user, 400, 'Do not use the same password.'),
    (bad_confirm_password_update_user, 400, 'Passwords do not match.'),
    (good_new_password_update_user, 200, 'Password has been updated successfully.')
]
@pytest.mark.parametrize("user_data, expected_status, expected_message", update_password_test_data)
def test_update_password(client, user, token, user_data, expected_status, expected_message):
    response = client.put('/api/auth/update-password', json=user_data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'

    if expected_status == 200:
        assert response_data['success'] is True
    else:
        assert response_data['success'] is False

    assert expected_message in response_data['message']

#testy do zmiany hasła uzytkownika - wymagane pola
def validate_required_field_update_password(client, data, field_name, user, token):
    response = client.put('/api/auth/update-password', json=data,
                          headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_update_current_password_required(client, user, token):
    validate_required_field_update_password(client, update_password_user_no_current_password, 'current_password', user, token)

def test_update_new_password_required(client, user, token):
    validate_required_field_update_password(client, update_password_user_no_new_password, 'new_password', user, token)

def test_update_confirm_new_password_required(client, user, token):
    validate_required_field_update_password(client, update_password_user_no_confirm_password, 'confirm_new_password', user, token)



#testy do zmiany nazwy uzytkownika
update_username_test_data = [
    (update_username_exists_user, 409, 'Username already exists.'),
    (update_username_user_bad_password, 400, 'Bad password.'),
    (update_username_user, 200, 'Username has been updated successfully.')
]
@pytest.mark.parametrize("input_data, expected_status, expected_message", update_username_test_data)
def test_update_username(client, user, token, input_data, expected_status, expected_message):
    response = client.put('/api/auth/update-username', json=input_data,
                          headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    assert 'success' in response_data
    
    if expected_status == 200:
        assert response_data['success'] is True
    elif expected_status == 409:
        assert response_data['success'] is False
    else:
        assert response_data['success'] is False
    
    assert expected_message in response_data['message']

#testy do zmiany nazwy uzytkownika - wymagane pola
def validate_required_field_update_username(client, data, field_name, user, token):
    response = client.put('/api/auth/update-username', json=data,
                          headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'{field_name} is required.'

def test_update_username_required(client, user, token):
    validate_required_field_update_username(client, register_no_username_update_user, 'new_username', user, token)

def test_update_password_required(client, user, token):
    validate_required_field_update_username(client, register_no_password_update_user, 'password', user, token)




#testy do kontaktowania sie uzytkownika z klinika
contact_test_data = [
    (contact_user_from_clinic_no_email, 400, 'Please enter your email address.'),
    (contact_user_from_clinic_no_subject, 400, 'Please enter your subject.'),
    (contact_user_from_clinic_no_message, 400, 'Please enter your message.'),
    (contact_user_from_clinic_success, 200, 'Your message has been sent.')
]
@pytest.mark.parametrize("input_data, expected_status, expected_message", contact_test_data)
def test_validate_required_field_contact_username(client, input_data, expected_status, expected_message):
    response = client.post('/api/auth/contact', json=input_data)
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 400:
        assert response_data['success'] is False
    if expected_status == 200:
        assert response_data['success'] is True
    assert response_data['message'] == expected_message



#testy do usuwania konta uzytkownika
delete_user_account_data = [
    (delete_account_user_bad_password, 400, 'Bad password.'),
    (delete_account_user_bad_confirm_password, 400, 'Passwords do not match.'),
    (delete_account_user_success, 200, 'Account has been deleted successfully.')
]
@pytest.mark.parametrize("input_data, expected_status, expected_message", delete_user_account_data)
def test_delete_account(client, token, input_data, expected_status, expected_message, sample_data):
    response = client.delete('/api/auth/delete-account', json=input_data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.get_json()
    assert response.status_code == expected_status
    assert response.headers['Content-Type'] == 'application/json'
    if expected_status == 200:
        assert response_data['success'] is True
    else:
        assert response_data['success'] is False
    assert response_data['message'] == expected_message

# def test_delete_account_with_patient_profile(client, user_patient, token_patient, sample_data):
#     response = client.delete('/api/auth/delete-account', json=delete_account_user_success, headers={'Authorization': f'Bearer {token_patient}'})
#     response_data = response.get_json()
#     assert response.status_code == 409
#     assert response_data['success'] is False
#     assert response_data['message'] == 'You have a patient profile. Please delete it first.'