expired_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoicGF0aWVudCIsImV4cCI6MTY5ODQzMDI2Nn0.WW9W-sfM9yMkM3Tx6iQMlsBXXPwVVue72RbNKwbdKM4'

register_mock_user_patient = {
    'id': 15,
    'username': 'testx',
    'email': 'testx@gmail.com',
    'password': '123456',
    'confirm_password': '123456'
    }

register_mock_user_receptionist = {
    'id': 11,
    'username': 'recepcja',
    'email': 'recepcja@gmail.com',
    'password': 'recepcja',
    'confirm_password': 'recepcja'
    }

register_mock_user_doctor = {
    'id': 2,
    'username': 'okulista',
	'email': 'okulista_przychodnia@wp.pl',
    'password': 'okulista_przychodnia',
    'confirm_password': 'okulista_przychodnia'
}

register_mock_user_novisit = {
    "id": 16,
    "username": "novisit",
    "password": "123456",
    'confirm_password': '123456',
	"email": "novisit@gmail.com",
}

register_mock_admin = {
    'username': 'admin',
    'password': 'admin123',
    'confirm_password': 'admin123',
    'email': 'admin@gmail.com'
}

register_mock_user = {
    'username': 'test',
    'email': 'test@gmail.com',
    'password': '123456',
    'confirm_password': '123456',
    }

register_no_username_user = register_mock_user_no_address = {k: v for k, v in register_mock_user.items() if k != 'username'}

register_no_password_user = register_mock_user_no_address = {k: v for k, v in register_mock_user.items() if k != 'password'}

register_no_confirm_password_user = {
    'username': 'test',
    'email': 'test@gmail.com',
    'password': '123456',
    'confirm_password': ' ',
}

register_successfuly_user = {
    'username': 'test2',
    'email': 'test2@gmail.com',
    'password': '123456',
    'confirm_password': '123456',
    }

register_invalid_length_username_user = {
    'username': 'te',
    'email': 'test10@gmail.com',
    'password': '123456',
    'confirm_password': '123456',
}

register_ivalid_email_user = {
    'username': 'testtest',
    'email': 'test10gmail.com',
    'password': '123456',
    'confirm_password': '123456',
}

register_invalid_length_password_user = {
    'username': 'testtest',
    'email': 'testtest@gmail.com',
    'password': '1234',
    'confirm_password': '1234',
}

register_used_username_user = {
    'username': 'test',
    'email': 'test2@gmail.com',
    'password': '123456',
    'confirm_password': '123456',
}

register_used_email_user = {
    'username': 'test2',
    'email': 'test@gmail.com',
    'password': '123456',
    'confirm_password': '123456',
}

invalid_password_user = {
    'username': 'testinvalid',
    'password': '1234567'
}

invalid_username_user = {
    'username': 'testinvalid',
    'password': '123456'
}

valid_user = {
    'username': 'test',
    'password': '123456'
}

bad_current_password_update_user = {
    'current_password': '1234567',
    'new_password': '123456',
    'confirm_new_password': '123456'
}

bad_new_password_update_user = {
    'current_password': '123456',
    'new_password': '123456',
    'confirm_new_password': '123456'
}

bad_confirm_password_update_user = {
    'current_password': '123456',
    'new_password': '1234567',
    'confirm_new_password': '123456'
}

good_new_password_update_user = {
    'current_password': '123456',
    'new_password': '1234567',
    'confirm_new_password': '1234567'
}

update_password_user_no_current_password = {
    "current_password": "      ",
    "new_password": "123456",
    "confirm_new_password": "123456"
}

update_password_user_no_new_password = {
    "current_password": "123456",
    "new_password": "      ",
    "confirm_new_password": "123456"
}

update_password_user_no_confirm_password = {
    "current_password": "123456",
    "new_password": "123456",
    "confirm_new_password": "      "
}

update_username_exists_user = {
    'new_username': 'test',
    'password': '123456'
}

update_username_user_bad_password = {
    'new_username': 'test2',
    'password': '1234567'
}

update_username_user = {
    'new_username': 'test2',
    'password': '123456'
}

register_no_username_update_user = {
    'new_username': '   ',
    'password': '123456'
}

register_no_password_update_user = {
    'new_username': 'test2',
    'password': '   '
}

contact_user_from_clinic_no_email = {
    'email': '    ',
    'subject': 'test',
    'message': 'test'
}

contact_user_from_clinic_no_subject = {
    'email': 'test@gmail.com',
    'subject': '    ',
    'message': 'test'
}

contact_user_from_clinic_no_message = {
    'email': 'test@gmail.com',
    'subject': 'test',
    'message': '    '
}

contact_user_from_clinic_success = {
    'email': 'test@gmail.com',
    'subject': 'test',
    'message': 'test'
}

delete_account_user_bad_password = {
    'password': '1234567',
    'confirm_password': '123456'
}

delete_account_user_bad_confirm_password = {
    'password': '123456',
    'confirm_password': '1234567'
}

delete_account_user_success = {
    'password': '123456',
    'confirm_password': '123456'
}
