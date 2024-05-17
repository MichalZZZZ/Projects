register_mock_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 1
}

register_invalid_length_first_name_doctor = {
    "name": "M",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_invalid_length_last_name_doctor = {
    "name": "Marian",
    "last_name": "K",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_invalid_length_description_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "J",
    "photo": "doctor1.png",
    "user_id": 10
}

register_invalid_length_seniority_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat 5 lat 5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_invalid_length_photo_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "d",
    "user_id": 10
}

register_invalid_specialty_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 10,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_not_found_user_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 20
}

register_invalid_role_user_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 7
}

register_used_user_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 2
}

register_mock_doctor_success = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_name_doctor = {
    "name": "   ",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy. Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_last_name_doctor = {
    "name": "Marian",
    "last_name": "   ",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem, ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy.Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_seniority_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "   ",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem,ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy.Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_description_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "   ",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_photo_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem,ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy.Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "   ",
    "user_id": 10
}

register_no_specialty_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": "   ",
    "description": "Jestem doswiadczonym i empatycznym lekarzem,ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy.Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": 10
}

register_no_user_id_doctor = {
    "name": "Marian",
    "last_name": "Kowalski",
    "seniority": "5 lat",
    "specialty_id": 1,
    "description": "Jestem doswiadczonym i empatycznym lekarzem,ktory zawsze stara sie w pelni zrozumiec problemy swoich pacjentow i udzielic im jak najlepszej pomocy.Zajmuje sie chorobami oczu i specjalizuje sie w leczeniu chorob siatkowki.",
    "photo": "doctor1.png",
    "user_id": "   "
}