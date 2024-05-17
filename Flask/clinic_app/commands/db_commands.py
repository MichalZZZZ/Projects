import json
from pathlib import Path
from sqlalchemy.sql import text
from clinic_app import db
from clinic_app.models import Doctor, Specialty, User, Patient, TokenSetPassword, Hour, Reception, Submission, Visit
from clinic_app.commands import db_manage_bp


def load_json_data_test(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / 'json-test' / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@db_manage_bp.cli.group()
def db_manage():
    pass


@db_manage.command()
def add_data_test():
    """Add sample data to database"""
    try: 
        data_json = load_json_data_test('users.json')
        for item in data_json:
            list = User(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('specialty.json')
        for item in data_json:
            list = Specialty(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('hours.json')  
        for item in data_json:
            list = Hour(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('doctors.json')
        for item in data_json:
            list = Doctor(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('patients.json')
        for item in data_json:
            list = Patient(**item)
            db.session.add(list)
            db.session.commit()    

        data_json = load_json_data_test('tokensetpassword.json')  
        for item in data_json:
            list = TokenSetPassword(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('receptions.json')
        for item in data_json:
            list = Reception(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('submission.json')  
        for item in data_json:
            list = Submission(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data_test('visits.json')  
        for item in data_json:
            list = Visit(**item)
            db.session.add(list)
            db.session.commit()

        print('Data has been succesfully added to database')
    except Exception as exc:
        print(f'Unexpected error: {exc}')


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute(text('DELETE FROM Visits'))
        db.session.execute(text('ALTER SEQUENCE Visits_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Submissions'))
        db.session.execute(text('ALTER SEQUENCE Submissions_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Doctors'))
        db.session.execute(text('ALTER SEQUENCE Doctors_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Specialties'))
        db.session.execute(text('ALTER SEQUENCE Specialties_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Tokens'))
        db.session.execute(text('ALTER SEQUENCE Tokens_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Users'))
        db.session.execute(text('ALTER SEQUENCE Users_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Patients'))
        db.session.execute(text('ALTER SEQUENCE Patients_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Tokensetpassword'))
        db.session.execute(text('ALTER SEQUENCE Tokensetpassword_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Hours'))
        db.session.execute(text('ALTER SEQUENCE Hours_id_seq RESTART WITH 1'))
        db.session.execute(text('DELETE FROM Receptions'))
        db.session.execute(text('ALTER SEQUENCE Receptions_id_seq RESTART WITH 1'))
        db.session.commit()
        print('Data has been succesfully removed from database')
    except Exception as exc:
        print(f'Unexpected error: {exc}')





def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / 'json' / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@db_manage.command()
def add_data():
    """Add sample data to database"""
    try: 
        data_json = load_json_data('users.json')
        for item in data_json:
            list = User(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data('specialty.json')
        for item in data_json:
            list = Specialty(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data('hours.json')  
        for item in data_json:
            list = Hour(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data('doctors.json')
        for item in data_json:
            list = Doctor(**item)
            db.session.add(list)
            db.session.commit()

        data_json = load_json_data('patients.json')
        for item in data_json:
            list = Patient(**item)
            db.session.add(list)
            db.session.commit()    

        data_json = load_json_data('receptionist.json')
        for item in data_json:
            list = Reception(**item)
            db.session.add(list)
            db.session.commit() 

        # data_json = load_json_data('submissions.json')
        # for item in data_json:
        #     list = Submission(**item)
        #     db.session.add(list)
        #     db.session.commit() 

        # data_json = load_json_data('visit.json')
        # for item in data_json:
        #     list = Visit(**item)
        #     db.session.add(list)
        #     db.session.commit()

        print('Data has been succesfully added to database')
    except Exception as exc:
        print(f'Unexpected error: {exc}')
