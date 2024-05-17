register_mock_patient = {
    'first_name': 'Adam',
    'last_name': 'Ziolkowski',
    'pesel': '78101342761',
    'phone_number': '009934093',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn',
    'user_id': 14
}

register_mock_patient_x = {
    'first_name': 'Adam',
    'last_name': 'Ziolkowski',
    'pesel': '84110722759',
    'phone_number': '123456122',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn',
    'user_id': 15
}

register_mock_patient_novisit = {
    'first_name': 'Adam',
    'last_name': 'Ziolkowski',
    'pesel': '68122792643',
    'phone_number': '123454436',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn',
    'user_id': 16
}

register_mock_patient_2 = {
    'first_name': 'Adam',
    'last_name': 'Ziolkowski',
    'pesel': '65082724332',
    'phone_number': '999888777',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_mock_patient_success = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '60110714691',
    'phone_number': '123456789',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_no_first_name_user = {
    'first_name': '',
    'last_name': 'Ziolkowski',
    'pesel': '00212704091',
    'phone_number': '534786997',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_no_last_name_user = {
    'first_name': 'Michał',
    'last_name': '',
    'pesel': '00212704091',
    'phone_number': '534786997',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_no_address_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '00212704091',
    'phone_number': '534786997',
    'address': ''
}

register_invalid_length_first_name_user = {
    'first_name': 'M',
    'last_name': 'Ziolkowski',
    'pesel': '96010527859',
    'phone_number': '111111111',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_invalid_length_last_name_user = {
    'first_name': 'Michał',
    'last_name': 'Z',
    'pesel': '96010527859',
    'phone_number': '111111111',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_invalid_pesel_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '96010527',
    'phone_number': '111111111',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_invalid_phone_number_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '96010527859',
    'phone_number': '7765546xP',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_invalid_length_address_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '96010527859',
    'phone_number': '776554678',
    'address': 'a'
}

register_used_pesel_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel':'65082724332',
    'phone_number': '888888888',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

register_used_phone_number_user = {
    'first_name': 'Michał',
    'last_name': 'Ziolkowski',
    'pesel': '85080622937',
    'phone_number': '999999999',
    'address': 'ul. Słoneczna 54, 10-722 Olsztyn'
}

invalid_phone_number_update = {
    'phone_number': '12345678'
}

already_exists_phone_number_update = {
    'phone_number': '123456123'
}

success_update_phone_number = {
    'phone_number': '987556001'
}