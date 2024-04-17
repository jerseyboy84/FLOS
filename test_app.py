import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Student, Instructor

last_instructor_id = 6
last_student_id = 10


class TestCase(unittest.TestCase):
    """This class represents the FLOS project test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

#  ----------------------------------------------------------------
#  Tests related to allInstructors GET (tests 1-3)
#  ----------------------------------------------------------------

    def test_01_get_allInstructors_by_provost(self):
        res = self.client().get(
            '/allInstructors', headers={
             "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalInstructors'], 6)

    def test_02_get_allInstructors_by_student(self):
        res = self.client().get(
            '/allInstructors', headers={
             "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_03_get_allInstructors_by_expired(self):
        res = self.client().get(
            '/allInstructors', headers={
             "Authorization": "Bearer " + os.environ['EXPIRED_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

#  ----------------------------------------------------------------
#  Tests related to allStudents GET (tests 4-5)
#  ----------------------------------------------------------------

    def test_04_get_allStudents_by_provost(self):
        res = self.client().get(
            '/allStudents', headers={
             "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalStudents'], 10)

    def test_05_get_allInstructors_by_student(self):
        res = self.client().get(
            '/allStudents', headers={
             "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

#  ----------------------------------------------------------------
#  Tests related to instructorMatches GET (tests 6-9)
#  ----------------------------------------------------------------

    def test_06_get_instructorMatches_valid_id_by_provost(self):
        res = self.client().get(
            '/instructorMatches/5', headers={
             "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalMatchInstructors'], 2)

    def test_07_get_instructorMatches_invalid_id_by_provost(self):
        res = self.client().get(
            '/instructorMatches/999', headers={
             "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_08_get_instructorMatches_valid_id_by_student(self):
        res = self.client().get(
            '/instructorMatches/5', headers={
             "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalMatchInstructors'], 2)

    def test_09_get_instructorMatches_invalid_id_by_student(self):
        res = self.client().get(
            '/instructorMatches/999', headers={
             "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

#  ----------------------------------------------------------------
#  Tests related to instructor POST/PATCH/DELETE (tests 10-15)
#  ----------------------------------------------------------------

    def test_10_post_instructor_by_provost(self):
        res = self.client().post('/instructor', headers={
                "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
            json={
                'name': 'Random Babble',
                'teachLanguage': 'pigLatin',
                'fluentLanguage': 'Creole'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalInstructors'], 7)
        global last_instructor_id
        last_instructor_id = data['created']

    def test_11_patch_instructor_by_provost(self):
        global last_instructor_id
        res = self.client().patch('/instructor/' + str(last_instructor_id),
                                  headers={"Authorization": "Bearer " +
                                  os.environ['PROVOST_JWT']},
                                  json={
                                    'name': 'Random Babble',
                                    'teachLanguage': 'Creole',
                                    'fluentLanguage': 'Latin'
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['teachLanguage'], 'Creole')

    def test_12_delete_instructor_by_provost(self):
        global last_instructor_id
        res = self.client().delete('/instructor/' + str(last_instructor_id),
                                   headers={"Authorization": "Bearer " +
                                   os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalInstructors'], 6)

    def test_13_post_instructor_by_student(self):
        res = self.client().post('/instructor', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']},
            json={
                'name': 'Random Babble',
                'teachLanguage': 'pigLatin',
                'fluentLanguage': 'Creole'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_14_patch_instructor_by_student(self):
        res = self.client().patch('/instructor/1', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']},
            json={
                'name': 'Random Babble',
                'teachLanguage': 'Creole',
                'fluentLanguage': 'Latin'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_15_delete_instructor_by_student(self):
        res = self.client().delete('/instructor/1', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

#  ----------------------------------------------------------------
#  Tests related to student POST/PATCH/DELETE (tests 16-21)
#  ----------------------------------------------------------------

    def test_16_post_student_by_provost(self):
        res = self.client().post('/student', headers={
            "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
             json={
                'name': 'Pet Parrot',
                'studyLanguage': 'any',
                'nativeLanguage': 'none'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalStudents'], 11)
        global last_student_id
        last_student_id = data['created']

    def test_17_patch_student_by_provost(self):
        global last_student_id
        res = self.client().patch('/student/' + str(last_student_id), headers={
                "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
                json={
                'name': 'Pet Parrot',
                'studyLanguage': 'any',
                'nativeLanguage': 'parrot'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['nativeLanguage'], 'parrot')

    def test_18_delete_student_by_provost(self):
        global last_student_id
        res = self.client().delete(
            '/student/' + str(last_student_id), headers={
             "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalstudents'], 10)

    def test_19_post_student_by_student(self):
        res = self.client().post('/student', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']},
             json={
                'name': 'Pet Parrot',
                'studyLanguage': 'any',
                'nativeLanguage': 'none'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_20_patch_student_by_student(self):
        res = self.client().patch('/student/1', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']},
            json={
                'name': 'Pet Parrot',
                'studyLanguage': 'any',
                'nativeLanguage': 'parrot'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_21_delete_student_by_student(self):
        res = self.client().delete('/student/1', headers={
            "Authorization": "Bearer " + os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

#  ----------------------------------------------------------------
#  Tests related to bad client requests (tests 22-27)
#  ----------------------------------------------------------------

    def test_22_patch_instructor_by_provost_invalid_id(self):
        global last_instructor_id
        res = self.client().patch('/instructor/999', headers={
            "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
            json={
                'name': 'Random Babble',
                'teachLanguage': 'Creole',
                'fluentLanguage': 'Latin'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_23_delete_instructor_by_provost_invalid_id(self):
        res = self.client().delete('/instructor/999', headers={
            "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_24_patch_student_by_provost_invalid_id(self):
        res = self.client().patch('/student/999', headers={
                "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
                json={
                'name': 'Pet Parrot',
                'studyLanguage': 'any',
                'nativeLanguage': 'parrot'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_25_delete_student_by_provost_invalid_id(self):
        res = self.client().delete('/student/999', headers={
            "Authorization": "Bearer " + os.environ['PROVOST_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_26_delete_instructorMatches_by_student(self):
        res = self.client().delete('/instructorMatches/5', headers={
            "Authorization": "Bearer " +
            os.environ['STUDENT_JWT']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_27_post_student_by_provost_without_name(self):
        res = self.client().post('/student', headers={
            "Authorization": "Bearer " + os.environ['PROVOST_JWT']},
             json={
                'studyLanguage': 'any',
                'nativeLanguage': 'none'
                }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
